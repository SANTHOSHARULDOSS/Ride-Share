import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from .models import EmailLog
from .ai_services import get_gemini_model

logger = logging.getLogger(__name__)

def log_email_sent(recipient, subject, content, email_type):
    """Save record of sent email in database."""
    try:
        EmailLog.objects.create(
            recipient=recipient,
            subject=subject,
            content=content,
            email_type=email_type,
            created_at=timezone.now()
        )
    except Exception as e:
        logger.error(f"Failed to write Email log to DB: {e}")

def generate_ai_message(recipient_name, email_type, context_info=""):
    """Use Gemini to generate a personalized greeting or message segment for the email."""
    prompt = f"""
    Write a short, professional, friendly 2-sentence email paragraph for a user named {recipient_name}.
    Email Type: {email_type}
    Additional Context: {context_info}
    Do not include email headers or signatures, just the paragraph itself.
    """
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error during email personalization: {e}")
            
    # Fallback standard templates
    if email_type == "WELCOME":
        return f"Hi {recipient_name}, welcome to Ride-Share! We are thrilled to have you join our sustainable carpooling community. Start matching and save cost today!"
    elif email_type == "VERIFICATION":
        return f"Hi {recipient_name}, please verify your email address to confirm your identity and secure your Ride-Share profile."
    elif email_type == "RESET":
        return f"Hi {recipient_name}, we received a request to reset your password. If you didn't request this, you can ignore this email."
    elif email_type == "TRIP_INVITE":
        return f"Hi {recipient_name}, you have been invited to join a carpooling trip. Review the route waypoints and secure your seat!"
    elif email_type == "COMMUNITY_INVITE":
        return f"Hi {recipient_name}, you've been invited to join a trust-based travel community on our platform."
    else:
        return f"Hi {recipient_name}, thank you for using Ride-Share. Here is an update regarding your recent activity on our platform."

def send_templated_email(recipient_email, recipient_name, subject, email_type, context=None, personalize_with_ai=True):
    """
    Core function to format and send a multi-part HTML/Text email,
    saving the audit record in the database.
    """
    if context is None:
        context = {}
        
    context['name'] = recipient_name
    context['email_type'] = email_type

    # Personalized AI block
    if personalize_with_ai:
        ai_details = context.get('ai_context', '')
        ai_block = generate_ai_message(recipient_name, email_type, ai_details)
        context['ai_personalization'] = ai_block
    else:
        context['ai_personalization'] = ""

    # Simple inline styling HTML email template
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
            <div style="background-color: #4f46e5; color: white; padding: 15px; text-align: center; border-radius: 6px 6px 0 0;">
                <h2 style="margin: 0;">🚗 Ride-Share updates</h2>
            </div>
            <div style="padding: 20px;">
                <p>Hello <strong>{recipient_name}</strong>,</p>
                
                {f'<p style="background-color: #f3f4f6; border-left: 4px solid #4f46e5; padding: 10px; font-style: italic; color: #4b5563;">"{context["ai_personalization"]}"</p>' if context['ai_personalization'] else ''}
                
                {f'<p><strong>Verification Code / Link:</strong> <a href="{context["action_url"]}" style="background-color: #4f46e5; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; display: inline-block;">{context["action_text"]}</a></p>' if 'action_url' in context else ''}
                
                {f'<p>{context["message_details"]}</p>' if 'message_details' in context else ''}
                
                <p>If you have any questions or concerns, please visit our FAQ page or reply directly to this email to open a support ticket.</p>
                
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #9ca3af; text-align: center;">This is an automated notification from the Ride-Share platform. Please do not reply directly if this is a verification email.</p>
            </div>
        </body>
    </html>
    """
    
    text_content = strip_tags(html_content)
    
    # Setup mail sender settings
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'support@yourdomain.com')
    
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        
        # Log to DB
        log_email_sent(recipient_email, subject, text_content, email_type)
        logger.info(f"Successfully sent {email_type} email to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        # Even if sending fails, we log it locally for debugging/logs UI
        log_email_sent(recipient_email, f"[FAILED] {subject}", f"Error: {e}\n\nContent:\n{text_content}", email_type)
        return False
