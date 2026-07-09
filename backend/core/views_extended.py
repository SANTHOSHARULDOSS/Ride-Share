import os
import json
import uuid
import datetime
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404

def safe_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        raise Http404("Invalid identifier")
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q, Sum, Count, Avg
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import (
    User, Vehicle, Ride, RouteWaypoint, Booking, Community, CommunityMember,
    Friendship, Message, Notification, Event, EventAttendee, Report, SOSAlert,
    Rating, EmailLog, AILog, UserSession, CommunityPost, SupportTicket
)
from .forms import CommunityForm, EventForm
from .ai_services import plan_trip_assistant, chat_support_bot, reply_support_email, check_toxicity
from .email_services import send_templated_email

User = get_user_model()


# ---------------------------------------------------------------------
# 1. Community System
# ---------------------------------------------------------------------
@login_required
def community_list_view(request):
    """List all communities and show user-joined communities."""
    query = request.GET.get('q', '')
    if query:
        communities = Community.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        communities = Community.objects.all()

    # Find communities the user is currently in
    user_memberships = CommunityMember.objects.filter(user=request.user, status='APPROVED').values_list('community_id', flat=True)
    joined_communities = Community.objects.filter(id__in=user_memberships)
    other_communities = communities.exclude(id__in=user_memberships)

    context = {
        'joined_communities': joined_communities,
        'other_communities': other_communities,
        'query': query
    }
    return render(request, 'community_list.html', context)

@login_required
def community_create_view(request):
    """Let users create communities."""
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.invite_link = str(uuid.uuid4())[:8]
            community.save()
            
            # Make creator the Admin member
            CommunityMember.objects.create(
                community=community,
                user=request.user,
                role='ADMIN',
                status='APPROVED'
            )
            messages.success(request, f"Community '{community.name}' created successfully!")
            return redirect('community_detail', comm_id=community.id)
    else:
        form = CommunityForm()
    return render(request, 'community_create.html', {'form': form})

@login_required
def community_detail_view(request, comm_id):
    """View details of a community, its members, rules, and events."""
    community = get_object_or_404(Community, id=safe_int(comm_id))
    
    # Check user membership
    membership = CommunityMember.objects.filter(community=community, user=request.user).first()
    
    members_count = CommunityMember.objects.filter(community=community, status='APPROVED').count()
    members = CommunityMember.objects.filter(community=community, status='APPROVED').select_related('user')
    pending_requests = []
    
    if membership and membership.role in ['ADMIN', 'MODERATOR']:
        pending_requests = CommunityMember.objects.filter(community=community, status='PENDING').select_related('user')
        
    events = Event.objects.filter(community=community).order_by('-date')
    
    context = {
        'community': community,
        'membership': membership,
        'members_count': members_count,
        'members': members,
        'pending_requests': pending_requests,
        'events': events
    }
    return render(request, 'community_detail.html', context)

@login_required
def community_join_view(request, comm_id):
    """Join community or request access."""
    community = get_object_or_404(Community, id=safe_int(comm_id))
    membership, created = CommunityMember.objects.get_or_create(
        community=community,
        user=request.user,
        defaults={
            'role': 'MEMBER',
            'status': 'APPROVED' if community.community_type == 'PUBLIC' else 'PENDING'
        }
    )
    
    if created:
        if community.community_type == 'PUBLIC':
            messages.success(request, f"You joined '{community.name}'!")
        else:
            messages.info(request, "Join request submitted. Awaiting moderator approval.")
    else:
        messages.warning(request, "You already have a pending or active membership.")
        
    return redirect('community_detail', comm_id=community.id)

@login_required
def community_approve_member_view(request, comm_id, user_id):
    """Approve membership requests in private communities."""
    community = get_object_or_404(Community, id=safe_int(comm_id))
    
    # Authorize checking
    user_role = get_object_or_404(CommunityMember, community=community, user=request.user).role
    if user_role not in ['ADMIN', 'MODERATOR']:
        return HttpResponseForbidden("Only admins/moderators can approve requests.")
        
    target_member = get_object_or_404(CommunityMember, community=community, user_id=safe_int(user_id))
    target_member.status = 'APPROVED'
    target_member.save()

    # Notify approved user
    Notification.objects.create(
        recipient=target_member.user,
        sender=request.user,
        notification_type="COMMUNITY_INVITE",
        content=f"Your request to join community '{community.name}' was approved!",
        link=f"/communities/{community.id}/"
    )

    messages.success(request, f"Approved {target_member.user.username} membership.")
    return redirect('community_detail', comm_id=community.id)

# ---------------------------------------------------------------------
# 2. Friend System
# ---------------------------------------------------------------------
@login_required
def friends_list_view(request):
    """Show friends list, pending requests, and smart friend suggestions."""
    user = request.user
    
    # 1. Confirmed Friends
    friends_initiated = Friendship.objects.filter(user=user, status='ACCEPTED').values_list('friend_id', flat=True)
    friends_received = Friendship.objects.filter(friend=user, status='ACCEPTED').values_list('user_id', flat=True)
    friend_ids = list(friends_initiated) + list(friends_received)
    friends = User.objects.filter(id__in=friend_ids)

    # 2. Pending Requests
    pending_received = Friendship.objects.filter(friend=user, status='PENDING').select_related('user')
    pending_sent = Friendship.objects.filter(user=user, status='PENDING').select_related('friend')

    # 3. Smart Recommendations
    # Suggest people who share the same verified college/company OR share the same communities
    same_collegue_ids = User.objects.filter(
        Q(verified_college=user.verified_college, verified_college__isnull=False) |
        Q(verified_org=user.verified_org, verified_org__isnull=False)
    ).exclude(id=user.id).exclude(id__in=friend_ids).values_list('id', flat=True)
    
    suggestions = User.objects.filter(id__in=same_collegue_ids)[:5]

    context = {
        'friends': friends,
        'pending_received': pending_received,
        'pending_sent': pending_sent,
        'suggestions': suggestions
    }
    return render(request, 'friends.html', context)

@login_required
def friend_request_view(request, user_id):
    """Send friend request."""
    target_user = get_object_or_404(User, id=safe_int(user_id))
    if target_user == request.user:
        messages.error(request, "You cannot add yourself.")
        return redirect('friends')

    # Check existing relations
    exists = Friendship.objects.filter(
        Q(user=request.user, friend=target_user) | Q(user=target_user, friend=request.user)
    ).exists()
    
    if not exists:
        Friendship.objects.create(user=request.user, friend=target_user, status='PENDING')
        
        # Send Notification
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type="FRIEND_REQUEST",
            content=f"{request.user.username} sent you a friend request.",
            link="/friends/"
        )
        messages.success(request, f"Friend request sent to {target_user.username}.")
    else:
        messages.warning(request, "Relationship already exists.")
        
    return redirect('friends')

@login_required
def friend_accept_view(request, friendship_id):
    """Accept friend request."""
    friendship = get_object_or_404(Friendship, id=safe_int(friendship_id), friend=request.user)
    friendship.status = 'ACCEPTED'
    friendship.save()

    # Notify requester
    Notification.objects.create(
        recipient=friendship.user,
        sender=request.user,
        notification_type="GENERAL",
        content=f"{request.user.username} accepted your friend request!",
        link="/friends/"
    )
    messages.success(request, f"Friend request accepted!")
    return redirect('friends')

@login_required
def friend_reject_view(request, friendship_id):
    """Reject request."""
    friendship = get_object_or_404(Friendship, id=safe_int(friendship_id), friend=request.user)
    friendship.delete()
    messages.info(request, "Friend request declined.")
    return redirect('friends')

@login_required
def friend_remove_view(request, user_id):
    """Remove friend relationship."""
    Friendship.objects.filter(
        Q(user=request.user, friend_id=safe_int(user_id)) | Q(user_id=safe_int(user_id), friend=request.user)
    ).delete()
    messages.success(request, "Friend removed successfully.")
    return redirect('friends')

# ---------------------------------------------------------------------
# 3. Event Planner
# ---------------------------------------------------------------------
@login_required
def event_list_view(request):
    """List upcoming events."""
    events = Event.objects.all().order_by('date')
    return render(request, 'event_list.html', {'events': events})

@login_required
def event_create_view(request):
    """Let users schedule meetups, hackathons, trekking rides."""
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            
            # Creator automatically RSVP 'GOING'
            EventAttendee.objects.create(
                event=event,
                user=request.user,
                status='GOING'
            )
            messages.success(request, f"Event '{event.title}' scheduled successfully!")
            return redirect('event_list')
    else:
        form = EventForm(user=request.user)
    return render(request, 'event_create.html', {'form': form})

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=safe_int(event_id))
    attendees = EventAttendee.objects.filter(event=event).select_related('user')
    user_status = EventAttendee.objects.filter(event=event, user=request.user).first()
    
    context = {
        'event': event,
        'attendees': attendees,
        'user_status': user_status
    }
    return render(request, 'event_detail.html', context)

@login_required
def event_rsvp_view(request, event_id, status_choice):
    """RSVP to events."""
    event = get_object_or_404(Event, id=safe_int(event_id))
    if status_choice not in ['GOING', 'INTERESTED', 'REMOVE']:
        messages.error(request, "Invalid status choice.")
        return redirect('event_detail', event_id=event.id)

    if status_choice == 'REMOVE':
        EventAttendee.objects.filter(event=event, user=request.user).delete()
        messages.info(request, "Removed your RSVP.")
    else:
        attendee, created = EventAttendee.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={'status': status_choice}
        )
        if not created:
            attendee.status = status_choice
            attendee.save()
        messages.success(request, f"RSVP set to '{status_choice.lower()}'!")
        
    return redirect('event_detail', event_id=event.id)

# ---------------------------------------------------------------------
# 4. Chat System View (VWs & REST API file uploads)
# ---------------------------------------------------------------------
@login_required
def chat_dashboard_view(request):
    """List all direct, community, and trip chats the user can enter."""
    user = request.user
    
    # 1. Friends list for direct chats
    friends_initiated = Friendship.objects.filter(user=user, status='ACCEPTED').values_list('friend_id', flat=True)
    friends_received = Friendship.objects.filter(friend=user, status='ACCEPTED').values_list('user_id', flat=True)
    friend_ids = list(friends_initiated) + list(friends_received)
    direct_contacts = User.objects.filter(id__in=friend_ids)

    # 2. Joined Communities
    community_ids = CommunityMember.objects.filter(user=user, status='APPROVED').values_list('community_id', flat=True)
    joined_communities = Community.objects.filter(id__in=community_ids)

    # 3. Active Trips
    # Driver rides or Passenger rides booked
    driver_rides = Ride.objects.filter(driver=user, status__in=[Ride.Status.ACTIVE, Ride.Status.DRAFT])
    passenger_rides = Booking.objects.filter(passenger=user, status='ACCEPTED').values_list('ride_id', flat=True)
    active_trips = Ride.objects.filter(Q(id__in=driver_rides) | Q(id__in=passenger_rides)).select_related('driver')

    context = {
        'direct_contacts': direct_contacts,
        'joined_communities': joined_communities,
        'active_trips': active_trips
    }
    return render(request, 'chat_dashboard.html', context)

@login_required
def chat_room_view(request, room_type, room_id):
    """Open message room for WebSocket chat."""
    room_title = ""
    messages_history = []
    
    if room_type == 'direct':
        recipient = get_object_or_404(User, id=safe_int(room_id))
        room_title = f"Chat with {recipient.username}"
        messages_history = Message.objects.filter(
            Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
        ).order_by('created_at')[:50]
        
    elif room_type == 'community':
        community = get_object_or_404(Community, id=safe_int(room_id))
        # Check permissions
        is_member = CommunityMember.objects.filter(community=community, user=request.user, status='APPROVED').exists()
        if not is_member:
            return HttpResponseForbidden("Must join community to chat.")
        room_title = f"{community.name} (Channel)"
        messages_history = Message.objects.filter(community=community).order_by('created_at')[:50]

    elif room_type == 'ride':
        ride = get_object_or_404(Ride, id=safe_int(room_id))
        # Check if driver or accepted passenger
        is_allowed = (ride.driver == request.user) or Booking.objects.filter(ride=ride, passenger=request.user, status='ACCEPTED').exists()
        if not is_allowed:
            return HttpResponseForbidden("Not authorized to enter this trip's chat.")
        room_title = f"Trip: {ride.start_location} ➔ {ride.end_location}"
        messages_history = Message.objects.filter(ride=ride).order_by('created_at')[:50]

    context = {
        'room_type': room_type,
        'room_id': room_id,
        'room_title': room_title,
        'messages_history': messages_history
    }
    return render(request, 'chat_room.html', context)

@login_required
@require_POST
def chat_upload_file_view(request):
    """API for uploading chat media/documents and returning file URL."""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
        
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'chat_attachments'))
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_url = os.path.join(settings.MEDIA_URL, 'chat_attachments', filename)
    
    return JsonResponse({
        'file_url': file_url,
        'file_name': uploaded_file.name,
        'file_type': uploaded_file.content_type
    })

# ---------------------------------------------------------------------
# 5. Safety Features (SOS emergency and Reporting)
# ---------------------------------------------------------------------
@login_required
@require_POST
def sos_trigger_view(request):
    """Triggers an SOS emergency message, creates log, and alerts compliance."""
    ride_id = request.POST.get('ride_id')
    lat = request.POST.get('latitude', 0.0)
    lng = request.POST.get('longitude', 0.0)
    
    ride = get_object_or_404(Ride, id=ride_id)
    
    # Save SOS alert
    alert = SOSAlert.objects.create(
        ride=ride,
        user=request.user,
        latitude=float(lat) if lat else None,
        longitude=float(lng) if lng else None,
        is_active=True
    )

    # In a real app, this sends SMS/Webhook to authority and emergency contact
    # We log email trace and system notifications
    Notification.objects.create(
        recipient=ride.driver if request.user != ride.driver else User.objects.filter(role='ADMIN').first(),
        notification_type="ADMIN_ANNOUNCEMENT",
        content=f"🚨 SOS EMERGENCY ALERT! User '{request.user.username}' has triggered emergency signal on Ride {ride.id}. Location tracked.",
        link=f"/admin/logs/"
    )
    
    # Write audit log to support
    EmailLog.objects.create(
        recipient="safety-compliance@yourdomain.com",
        subject=f"🚨 SOS EXTREME EMERGENCY ALERT - Ride ID: {ride.id}",
        content=f"User: {request.user.username} (Phone: {request.user.phone_number}) has triggered SOS signal at coordinates {lat}, {lng}.",
        email_type="REPLY_AUTO"
    )

    return JsonResponse({
        'status': 'success',
        'alert_id': alert.id,
        'message': 'Emergency services notified (simulated). SOS coordinate transmission active.'
    })

@login_required
def report_submit_view(request):
    """File a code of conduct or safety report."""
    if request.method == 'POST':
        reported_username = request.POST.get('reported_username')
        ride_id = request.POST.get('ride_id')
        comm_id = request.POST.get('comm_id')
        reason = request.POST.get('reason')

        reported_user = None
        if reported_username:
            reported_user = User.objects.filter(username=reported_username).first()
            
        ride = Ride.objects.filter(id=ride_id).first() if ride_id else None
        comm = Community.objects.filter(id=comm_id).first() if comm_id else None

        # Check toxicity on reason input
        toxicity = check_toxicity(reason)
        if toxicity and toxicity.get('is_toxic'):
            # Block toxic submissions
            messages.warning(request, "Report submission rejected: Harassment or profanity detected in reason box.")
            return redirect('dashboard')

        Report.objects.create(
            reporter=request.user,
            reported_user=reported_user,
            reported_ride=ride,
            reported_community=comm,
            reason=reason
        )
        
        # Deduct reputation from reported user as a trust warning
        if reported_user:
            reported_user.reputation_points = max(0, reported_user.reputation_points - 10)
            reported_user.save()

        messages.success(request, "Report submitted successfully. Our moderation queue is reviewing this.")
        return redirect('dashboard')

    # Render report form
    context = {
        'ride_id': request.GET.get('ride_id'),
        'comm_id': request.GET.get('comm_id'),
        'reported_user': request.GET.get('username')
    }
    return render(request, 'report_form.html', context)

# ---------------------------------------------------------------------
# 6. Reputation & Verification
# ---------------------------------------------------------------------
@login_required
def reputation_dashboard_view(request):
    """Reputation details and verification uploads."""
    user = request.user
    
    # Calculate averages rating
    avg_rating = Rating.objects.filter(reviewee=user).aggregate(Avg('rating'))['rating__avg'] or 0.0
    reviews_count = Rating.objects.filter(reviewee=user).count()
    
    # Retrieve user's sessions
    active_sessions = UserSession.objects.filter(user=user, is_active=True).count()

    context = {
        'avg_rating': round(avg_rating, 1),
        'reviews_count': reviews_count,
        'active_sessions': active_sessions
    }
    return render(request, 'reputation.html', context)

@login_required
def verify_id_upload_view(request):
    """Upload Government ID to earn verification badges."""
    if request.method == 'POST' and 'gov_id' in request.FILES:
        uploaded_id = request.FILES['gov_id']
        
        # Verify file is PDF/Image
        ext = os.path.splitext(uploaded_id.name)[1].lower()
        if ext not in ['.pdf', '.png', '.jpg', '.jpeg']:
            messages.error(request, "Invalid file format. Please upload PDF, PNG, or JPG.")
            return redirect('reputation')
            
        # Simulating manual document checking
        user = request.user
        user.is_gov_id_verified = True
        user.reputation_points += 100  # verified bonus points
        user.save()

        Notification.objects.create(
            recipient=user,
            notification_type="GENERAL",
            content="✓ Congratulations! Your government identity verification has been approved. Badges unlocked."
        )
        
        messages.success(request, "Government ID uploaded. Identity verified successfully!")
    else:
        messages.error(request, "Please choose a file to upload.")
    return redirect('reputation')

@login_required
def verify_org_email_view(request):
    """Verify College/Corporate organization email via verification code."""
    if request.method == 'POST':
        domain_email = request.POST.get('domain_email', '').strip()
        code_entered = request.POST.get('code', '').strip()
        step = request.POST.get('step') # 'send' or 'verify'

        user = request.user
        
        if step == 'send':
            # Check domain
            domain = domain_email.split('@')[-1]
            if domain in ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']:
                messages.error(request, "Please enter an official corporate or college email (no free email domains).")
                return redirect('reputation')
                
            code = str(uuid.uuid4())[:6].upper()
            request.session[f'org_verification_code_{user.id}'] = code
            request.session[f'org_verification_email_{user.id}'] = domain_email
            
            # Send code
            send_templated_email(
                recipient_email=domain_email,
                recipient_name=user.username,
                subject="Ride-Share Organization Verification Code",
                email_type="VERIFICATION",
                context={
                    'action_text': f"Verification Code: {code}",
                    'message_details': f"Use this code to verify your affiliation with the organization domain: {domain}"
                },
                personalize_with_ai=False
            )
            messages.success(request, f"A code has been sent to {domain_email}. Please enter it below.")
            return render(request, 'reputation.html', {'step_verify': True, 'domain_email': domain_email})

        elif step == 'verify':
            expected_code = request.session.get(f'org_verification_code_{user.id}')
            email_address = request.session.get(f'org_verification_email_{user.id}')
            
            if not email_address or not isinstance(email_address, str) or '@' not in email_address:
                messages.error(request, "Verification session expired or email address is invalid.")
                return redirect('reputation')
                
            if expected_code and code_entered == expected_code:
                domain = email_address.split('@')[-1]
                org_name = domain.split('.')[0].upper()
                
                # Update user fields
                if 'dtu' in domain or 'edu' in domain or 'univ' in domain:
                    user.verified_college = org_name
                else:
                    user.verified_org = org_name
                    
                user.reputation_points += 80
                user.save()
                
                # Clear session
                del request.session[f'org_verification_code_{user.id}']
                del request.session[f'org_verification_email_{user.id}']

                Notification.objects.create(
                    recipient=user,
                    notification_type="GENERAL",
                    content=f"✓ Affiliation with '{org_name}' has been successfully verified! Badge added."
                )
                
                messages.success(request, f"Successfully verified affiliation with {org_name}!")
            else:
                messages.error(request, "Invalid verification code.")
                
    return redirect('reputation')

# ---------------------------------------------------------------------
# 7. Ratings & Reviews
# ---------------------------------------------------------------------
@login_required
def rate_trip_view(request, ride_id):
    """Passengers rate driver after trip completion."""
    ride = get_object_or_404(Ride, id=ride_id)
    if ride.status != Ride.Status.COMPLETED:
        messages.error(request, "You can only rate completed trips.")
        return redirect('dashboard')

    # Check booking status
    booking = Booking.objects.filter(ride=ride, passenger=request.user, status=Booking.Status.COMPLETED).first()
    if not booking:
        messages.error(request, "Only confirmed passengers can review this trip.")
        return redirect('dashboard')

    if request.method == 'POST':
        stars = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')

        # Check toxicity on review comment
        toxicity = check_toxicity(comment)
        if toxicity and toxicity.get('is_toxic'):
            messages.warning(request, "Review comment rejected: abusive language detected.")
            return redirect('dashboard')

        rating, created = Rating.objects.get_or_create(
            reviewer=request.user,
            reviewee=ride.driver,
            ride=ride,
            defaults={'rating': stars, 'comment': comment}
        )
        
        # Adjust driver reputation points based on rating
        driver = ride.driver
        if stars == 5:
            driver.reputation_points += 15
        elif stars <= 2:
            driver.reputation_points = max(0, driver.reputation_points - 20)
        driver.save()

        messages.success(request, "Thank you for rating your ride!")
        return redirect('dashboard')
        
    return render(request, 'rate_ride.html', {'ride': ride})

# ---------------------------------------------------------------------
# 8. AI Assistance Views
# ---------------------------------------------------------------------
@login_required
def ai_support_chatbot_view(request):
    """Helpdesk page to chat with 24/7 support assistant."""
    if request.method == 'POST':
        question = request.POST.get('question')
        history = request.POST.get('history', '')
        
        # Get AI Response
        answer = chat_support_bot(question, history)
        return JsonResponse({'answer': answer})

    return render(request, 'chatbot.html')

@login_required
def ai_trip_planner_view(request):
    """Let users request Gemini travel suggestion itineraries."""
    itinerary = ""
    source = ""
    destination = ""
    
    if request.method == 'POST':
        source = request.POST.get('source', '')
        destination = request.POST.get('destination', '')
        prefs = request.POST.get('preferences', '')

        if source and destination:
            itinerary = plan_trip_assistant(source, destination, prefs)
            
    context = {
        'itinerary': itinerary,
        'source': source,
        'destination': destination
    }
    return render(request, 'trip_planner.html', context)

# ---------------------------------------------------------------------
# 9. Admin Audits Dashboard logs and simulated Email Auto-responder inbox
# ---------------------------------------------------------------------
@login_required
def admin_system_logs_view(request):
    """Panel displaying AI Logs, Email logs, and Safety alarms."""
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Only administrators can access logs.")

    ai_logs = AILog.objects.all().order_by('-created_at')[:50]
    email_logs = EmailLog.objects.all().order_by('-created_at')[:50]
    sos_alerts = SOSAlert.objects.all().select_related('ride', 'user').order_by('-created_at')[:50]
    reports = Report.objects.all().select_related('reporter', 'reported_user').order_by('-created_at')[:50]

    context = {
        'ai_logs': ai_logs,
        'email_logs': email_logs,
        'sos_alerts': sos_alerts,
        'reports': reports
    }
    return render(request, 'admin_logs.html', context)

@login_required
@require_POST
def admin_email_reply_processor(request):
    """
    Simulation of support@yourdomain.com inbox reader.
    Simulates reading a set of predefined customer emails, runs the Gemini reply algorithm,
    creates tickets, and sends automated responses.
    """
    if request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Define mock incoming emails
    mock_inbox = [
        {
            "sender": "college_commuter@gmail.com",
            "subject": "Help verifying college email",
            "body": "Hi Support, I am trying to connect my college student email but I haven't received the 6 digit code. Domain is dtu.ac.in. Can you manually approve me?"
        },
        {
            "sender": "worried_passenger@gmail.com",
            "subject": "Dangerous driving reported on yesterday ride",
            "body": "Hello, I took a ride from Delhi CP to Gurgaon with license DL-3C-AB-1234. The driver was speeding and driving unsafe. I want to report this unsafe trip immediately."
        },
        {
            "sender": "idea_generator@outlook.com",
            "subject": "Feature suggestion: Expense calculator integration",
            "body": "I would love to suggest adding an expense calculator where we can split tolls and fuel cost automatically inside the chat. Let me know if you can build this!"
        }
    ]

    processed = 0
    for mail in mock_inbox:
        # Run Gemini categorization and reply generation
        ai_reply = reply_support_email(mail["sender"], mail["subject"], mail["body"])

        # 1. Send Auto-Response email (persisted in db)
        send_templated_email(
            recipient_email=mail["sender"],
            recipient_name=mail["sender"].split('@')[0],
            subject=f"Re: {mail['subject']}",
            email_type="REPLY_AUTO",
            context={
                'message_details': ai_reply.get("reply_content", "We have received your ticket.")
            },
            personalize_with_ai=False
        )

        # 2. File system report if flagged
        if ai_reply.get("needs_escalation"):
            Report.objects.create(
                reporter=User.objects.filter(email=mail["sender"]).first() or User.objects.filter(role='ADMIN').first() or request.user,
                reason=f"[ESCALATED EMAIL TICKET] Category: {ai_reply.get('category')}\nSubject: {mail['subject']}\nBody: {mail['body']}"
            )

        processed += 1

    return JsonResponse({
        'status': 'success',
        'processed_count': processed,
        'message': f"Simulated support inbox processing completed. Checked {processed} emails. Gemini categorized and replied."
    })


# =============================================================================
# PHASE 9 — Notification System Views
# =============================================================================

@login_required
def notifications_view(request):
    """Full notifications page with read/unread state and pagination."""
    filter_type = request.GET.get('filter', 'all')

    notifs_qs = Notification.objects.filter(recipient=request.user)
    if filter_type == 'unread':
        notifs_qs = notifs_qs.filter(is_read=False)

    paginator = Paginator(notifs_qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()

    context = {
        'page_obj': page_obj,
        'filter_type': filter_type,
        'unread_count': unread_count,
    }
    return render(request, 'notifications.html', context)


@login_required
def mark_notification_read_view(request, notif_id):
    """Mark a single notification as read and redirect to its link."""
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notifications')


@login_required
def mark_all_notifications_read_view(request):
    """Mark all notifications as read (AJAX POST or GET)."""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({'status': 'ok'})
    messages.success(request, "All notifications marked as read.")
    return redirect('notifications')


# =============================================================================
# PHASE 5 — Community Enhancements
# =============================================================================

@login_required
def community_leave_view(request, comm_id):
    """Allow a member to leave a community."""
    community = get_object_or_404(Community, id=safe_int(comm_id))
    membership = CommunityMember.objects.filter(community=community, user=request.user).first()
    if membership:
        # Don't allow the sole admin to leave
        if membership.role == 'ADMIN':
            admin_count = CommunityMember.objects.filter(community=community, role='ADMIN').count()
            if admin_count <= 1:
                messages.error(request, "You are the only admin. Promote another member first.")
                return redirect('community_detail', comm_id=comm_id)
        membership.delete()
        messages.success(request, f"You have left '{community.name}'.")
    return redirect('community_list')


@login_required
def community_post_view(request, comm_id):
    """Create a post in a community."""
    community = get_object_or_404(Community, id=safe_int(comm_id))
    membership = CommunityMember.objects.filter(community=community, user=request.user, status='APPROVED').first()

    if not membership:
        messages.error(request, "You must be a member to post in this community.")
        return redirect('community_detail', comm_id=comm_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            messages.error(request, "Post content cannot be empty.")
            return redirect('community_detail', comm_id=comm_id)

        is_announcement = request.POST.get('is_announcement') == 'on' and membership.role in ['ADMIN', 'MODERATOR']

        # Toxicity check
        toxicity = check_toxicity(content)
        if toxicity.get('is_toxic'):
            messages.error(request, "Your post was flagged as potentially harmful and was not submitted.")
            return redirect('community_detail', comm_id=comm_id)

        post = CommunityPost.objects.create(
            community=community,
            author=request.user,
            content=content,
            is_announcement=is_announcement
        )

        if request.FILES.get('image'):
            post.image = request.FILES['image']
            post.save()

        messages.success(request, "Post published successfully!")

    return redirect('community_detail', comm_id=comm_id)


@login_required
def community_post_like_view(request, comm_id, post_id):
    """Like a community post (simple counter increment)."""
    post = get_object_or_404(CommunityPost, id=post_id, community__id=safe_int(comm_id))
    post.likes_count += 1
    post.save()
    return JsonResponse({'likes': post.likes_count})


# =============================================================================
# PHASE 6 — Contact Form
# =============================================================================

def contact_view(request):
    """Public contact form — creates a support ticket and sends confirmation email."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_body = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message_body:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'contact.html')

        # Generate unique ticket number
        ticket_number = f"RS-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

        # AI suggested reply
        ai_reply_data = reply_support_email(email, subject, message_body)
        ai_suggested = ai_reply_data.get('reply_content', '') if isinstance(ai_reply_data, dict) else str(ai_reply_data)

        # Create ticket in DB
        ticket = SupportTicket.objects.create(
            ticket_number=ticket_number,
            name=name,
            email=email,
            subject=subject,
            message=message_body,
            ai_suggested_reply=ai_suggested,
            status='OPEN'
        )

        # Send confirmation email to user
        send_templated_email(
            recipient_email=email,
            recipient_name=name,
            subject=f"[{ticket_number}] We received your message — RideShare Support",
            email_type="SUPPORT",
            context={
                'message_details': (
                    f"Your ticket number is: <strong>{ticket_number}</strong><br>"
                    f"Subject: {subject}<br><br>"
                    "Our team will respond within 24-48 hours. You can reply to this email to add more details."
                )
            },
            personalize_with_ai=False
        )

        # Send admin copy notification
        admin_users = User.objects.filter(role='ADMIN')
        for admin in admin_users:
            Notification.objects.create(
                recipient=admin,
                notification_type='ADMIN_ANNOUNCEMENT',
                content=f"📬 New support ticket [{ticket_number}] from {name}: {subject}",
                link='/admin/logs/'
            )

        messages.success(request, f"Message sent! Your ticket number is {ticket_number}. Check your email for confirmation.")
        return redirect('contact')

    return render(request, 'contact.html')


# =============================================================================
# PHASE 8 — Support Ticket Admin Management
# =============================================================================

@login_required
def admin_reply_ticket_view(request, ticket_id):
    """Admin replies to a support ticket by email."""
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden()

    ticket = get_object_or_404(SupportTicket, id=ticket_id)

    if request.method == 'POST':
        reply_body = request.POST.get('reply', '').strip()
        if not reply_body:
            messages.error(request, "Reply cannot be empty.")
            return redirect('admin_system_logs')

        ticket.admin_reply = reply_body
        ticket.status = 'IN_PROGRESS'
        ticket.save()

        # Send reply email
        send_templated_email(
            recipient_email=ticket.email,
            recipient_name=ticket.name,
            subject=f"Re: [{ticket.ticket_number}] {ticket.subject}",
            email_type="SUPPORT_REPLY",
            context={'message_details': reply_body},
            personalize_with_ai=False
        )

        messages.success(request, f"Reply sent to {ticket.email}.")
    return redirect('admin_system_logs')


@login_required
def admin_update_ticket_status_view(request, ticket_id):
    """Admin updates support ticket status."""
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden()

    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(SupportTicket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()
            messages.success(request, f"Ticket {ticket.ticket_number} status updated to {new_status}.")
    return redirect('admin_system_logs')


# =============================================================================
# PHASE 12 — views.py admin_stats_api (add here for simplicity)
# =============================================================================

@login_required
def contact_view_alias(request):
    return contact_view(request)

