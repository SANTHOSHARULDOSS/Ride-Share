import uuid
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.conf import settings

from .models import UserSession, Notification, EmailVerificationToken, PasswordResetToken
from .email_services import send_templated_email

User = get_user_model()


def record_login_session(request, user, remember_me=False):
    """
    Log device metadata and session key upon successful authentication.
    Applies custom session expiration based on 'Remember Me' preference.
    """
    if remember_me:
        request.session.set_expiry(1209600)  # 2 weeks
    else:
        request.session.set_expiry(0)  # Expire on browser close

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

    ua_lower = user_agent.lower()
    if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
        device = 'Mobile'
    elif 'tablet' in ua_lower or 'ipad' in ua_lower:
        device = 'Tablet'
    else:
        device = 'Desktop'

    UserSession.objects.filter(token=session_key).update(is_active=False)
    UserSession.objects.create(
        user=user,
        token=session_key,
        ip_address=ip,
        user_agent=user_agent[:255],
        device_type=device,
        is_active=True
    )


# ---------------------------------------------------------------------
# AJAX — Username Availability Check
# ---------------------------------------------------------------------
def check_username_view(request):
    """AJAX endpoint: checks if a username is available. Returns JSON."""
    username = request.GET.get('username', '').strip()
    if len(username) < 3:
        return JsonResponse({'available': False, 'message': 'Too short (min 3 chars)'})
    if len(username) > 30:
        return JsonResponse({'available': False, 'message': 'Too long (max 30 chars)'})
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({
        'available': not exists,
        'message': 'Available!' if not exists else 'Username already taken'
    })


# ---------------------------------------------------------------------
# Registration & Verification
# ---------------------------------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'PASSENGER')

        # Validation
        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                phone_number=phone
            )

            # Create DB-persisted verification token (24 hour expiry)
            token_str = str(uuid.uuid4())
            EmailVerificationToken.objects.create(
                user=user,
                token=token_str,
                expires_at=timezone.now() + datetime.timedelta(hours=24)
            )

            site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            verify_url = f"{site_url}/verify-email/?token={token_str}"

            send_templated_email(
                recipient_email=user.email,
                recipient_name=user.username,
                subject="Welcome to RideShare — Verify Your Email",
                email_type="VERIFICATION",
                context={
                    'action_text': 'Verify Email Address',
                    'action_url': verify_url,
                    'message_details': (
                        f"Your verification code is: <strong>{token_str[:8].upper()}</strong><br>"
                        "Or click the button above to verify automatically. Link expires in 24 hours."
                    )
                },
                personalize_with_ai=True
            )

            login(request, user, backend='core.auth_backends.EmailOrUsernameModelBackend')
            record_login_session(request, user)

            # Create welcome notification
            Notification.objects.create(
                recipient=user,
                notification_type='ADMIN_ANNOUNCEMENT',
                content=f"🎉 Welcome to RideShare, {user.username}! Verify your email to earn +50 reputation points.",
                link='/verify-email/'
            )

            messages.success(request, f"Account created! A verification link has been sent to {email}.")
            return redirect('verify_email_page')

        except IntegrityError:
            messages.error(request, "Username or Email already registered.")
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")

    return render(request, 'register.html')


@login_required
def verify_email_page(request):
    """Verify email via token from URL param or code input."""
    if request.user.is_email_verified:
        return redirect('dashboard')

    # Handle direct link click (token in URL)
    url_token = request.GET.get('token')
    if url_token:
        try:
            token_obj = EmailVerificationToken.objects.get(token=url_token, user=request.user)
            if token_obj.is_valid():
                token_obj.is_used = True
                token_obj.save()
                user = request.user
                user.is_email_verified = True
                user.reputation_points += 50
                user.save()
                Notification.objects.create(
                    recipient=user,
                    notification_type='ADMIN_ANNOUNCEMENT',
                    content="✓ Email verified! You earned +50 reputation points."
                )
                messages.success(request, "Email verified successfully! You're now a Trusted Traveller.")
                return redirect('dashboard')
            else:
                messages.error(request, "This verification link has expired or already been used.")
        except EmailVerificationToken.DoesNotExist:
            messages.error(request, "Invalid verification link.")

    # Handle manual code entry (first 8 chars of UUID token)
    if request.method == 'POST':
        code_entered = request.POST.get('code', '').strip().lower()
        # Find token where first 8 chars match
        pending_tokens = EmailVerificationToken.objects.filter(
            user=request.user, is_used=False
        )
        verified = False
        for token_obj in pending_tokens:
            if token_obj.is_valid() and token_obj.token[:8].lower() == code_entered:
                token_obj.is_used = True
                token_obj.save()
                user = request.user
                user.is_email_verified = True
                user.reputation_points += 50
                user.save()
                Notification.objects.create(
                    recipient=user,
                    notification_type='ADMIN_ANNOUNCEMENT',
                    content="✓ Email verified! You earned +50 reputation points."
                )
                messages.success(request, "Email verified! Welcome to RideShare.")
                return redirect('dashboard')
        if not verified:
            messages.error(request, "Invalid or expired verification code.")

    return render(request, 'verify_email.html')


@login_required
def resend_verification_view(request):
    """Resend verification email with a new token."""
    user = request.user
    if user.is_email_verified:
        return redirect('dashboard')

    # Invalidate old tokens
    EmailVerificationToken.objects.filter(user=user, is_used=False).update(is_used=True)

    token_str = str(uuid.uuid4())
    EmailVerificationToken.objects.create(
        user=user,
        token=token_str,
        expires_at=timezone.now() + datetime.timedelta(hours=24)
    )

    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    verify_url = f"{site_url}/verify-email/?token={token_str}"

    sent = send_templated_email(
        recipient_email=user.email,
        recipient_name=user.username,
        subject="RideShare — New Email Verification Link",
        email_type="VERIFICATION",
        context={
            'action_text': 'Verify Email Address',
            'action_url': verify_url,
            'message_details': f"Your new code is: <strong>{token_str[:8].upper()}</strong>. Expires in 24 hours."
        }
    )

    if sent:
        messages.success(request, f"New verification link sent to {user.email}.")
    else:
        messages.warning(request, f"Could not send email (SMTP not configured). Your code is: {token_str[:8].upper()}")
    return redirect('verify_email_page')


# ---------------------------------------------------------------------
# Forgot Password Flow (DB-persisted tokens, 1hr expiry)
# ---------------------------------------------------------------------
def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)

            # Invalidate old reset tokens
            PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

            token_str = str(uuid.uuid4())
            PasswordResetToken.objects.create(
                user=user,
                token=token_str,
                expires_at=timezone.now() + datetime.timedelta(hours=1)
            )

            site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            reset_url = f"{site_url}/reset-password/?token={token_str}"

            sent = send_templated_email(
                recipient_email=user.email,
                recipient_name=user.username,
                subject="RideShare — Reset Your Password",
                email_type="RESET",
                context={
                    'action_text': 'Reset Password',
                    'action_url': reset_url,
                    'message_details': f"Code: <strong>{token_str[:8].upper()}</strong>. This link expires in 1 hour."
                },
                personalize_with_ai=True
            )

            if sent:
                messages.success(request, f"Password reset link sent to {email}.")
            else:
                messages.warning(request, f"Email not configured. Reset code: {token_str[:8].upper()}")

            return redirect(f'/reset-password/?token={token_str}')

        except User.DoesNotExist:
            # Security: don't reveal if email exists
            messages.success(request, "If that email exists in our system, a reset link has been sent.")

    return render(request, 'forgot_password.html')


def reset_password_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    url_token = request.GET.get('token') or request.POST.get('token', '')

    if request.method == 'POST':
        code_entered = request.POST.get('code', '').strip().lower()
        new_password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'reset_password.html', {'token': url_token})

        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return render(request, 'reset_password.html', {'token': url_token})

        # Try to find token by full UUID or by short code
        token_obj = None
        if url_token:
            try:
                token_obj = PasswordResetToken.objects.get(token=url_token)
            except PasswordResetToken.DoesNotExist:
                pass

        if not token_obj:
            # Try matching by short code
            for t in PasswordResetToken.objects.filter(is_used=False):
                if t.token[:8].lower() == code_entered and t.is_valid():
                    token_obj = t
                    break

        if token_obj and token_obj.is_valid():
            user = token_obj.user
            user.set_password(new_password)
            user.save()
            token_obj.is_used = True
            token_obj.save()
            messages.success(request, "Password reset successfully! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid or expired reset code. Please request a new one.")

    return render(request, 'reset_password.html', {'token': url_token})


# ---------------------------------------------------------------------
# Google Sign-In (OAuth Simulation)
# ---------------------------------------------------------------------
def google_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    email = request.GET.get('email', 'google_passenger@gmail.com')
    name = email.split('@')[0].replace('.', '_')

    try:
        user = User.objects.get(email=email)
        messages.success(request, f"Signed in with Google: {email}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=name,
            email=email,
            password=str(uuid.uuid4()),
            role='DRIVER' if 'driver' in name else 'PASSENGER',
            is_email_verified=True
        )
        user.reputation_points = 150
        user.save()
        Notification.objects.create(
            recipient=user,
            notification_type='ADMIN_ANNOUNCEMENT',
            content=f"🎉 Welcome {user.username}! Your Google account is verified (+150 reputation)."
        )
        messages.success(request, f"Registered via Google SSO: {email}")

    login(request, user, backend='core.auth_backends.EmailOrUsernameModelBackend')
    record_login_session(request, user)
    return redirect('dashboard')


# ---------------------------------------------------------------------
# Change Password (for authenticated users)
# ---------------------------------------------------------------------
@login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('profile')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('profile')

        if len(new_password) < 6:
            messages.error(request, "New password must be at least 6 characters.")
            return redirect('profile')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep user logged in
        messages.success(request, "Password changed successfully!")
        return redirect('profile')

    return redirect('profile')


# ---------------------------------------------------------------------
# Active Session Management
# ---------------------------------------------------------------------
@login_required
def sessions_view(request):
    sessions = UserSession.objects.filter(user=request.user, is_active=True)
    return render(request, 'sessions.html', {
        'sessions': sessions,
        'current_token': request.session.session_key
    })


@login_required
@require_POST
def terminate_session_view(request, session_id):
    session_record = get_object_or_404(UserSession, id=session_id, user=request.user)
    session_record.is_active = False
    session_record.save()

    if session_record.token == request.session.session_key:
        logout(request)
        messages.success(request, "Your current session was terminated.")
        return redirect('landing')

    try:
        from django.contrib.sessions.models import Session
        Session.objects.filter(session_key=session_record.token).delete()
    except Exception:
        pass

    messages.success(request, "Device session terminated successfully.")
    return redirect('sessions')
