import os
import json
import logging
from django.utils import timezone
from .models import AILog

logger = logging.getLogger(__name__)

def get_gemini_model():
    """Configure and return the Gemini GenerativeModel client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # Use gemini-1.5-flash for general-purpose text generation
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Failed to initialize Gemini Client: {e}")
        return None

def log_ai_call(prompt, response, log_type):
    """Log the prompt and generated response in the database."""
    try:
        AILog.objects.create(
            prompt=prompt,
            response=response,
            log_type=log_type,
            created_at=timezone.now()
        )
    except Exception as e:
        logger.error(f"Failed to write AI log to DB: {e}")

# 1. AI Travel Assistant
def plan_trip_assistant(source, destination, preferences=""):
    """
    Plan a travel itinerary between Source and Destination using Gemini.
    Provides transport, hotels, restaurants, weather advice, budget, and packing tips.
    """
    prompt = f"""
    Act as a professional AI Travel Assistant. Provide a detailed travel plan for a trip from {source} to {destination}.
    Preferences specified: {preferences}
    Format the response with the following sections in markdown:
    1. **Estimated Route & Distance**
    2. **Transport Suggestions**
    3. **Recommended Hotels (Budget, Mid-Range, Luxury)**
    4. **Top Restaurants & Local Cuisine**
    5. **Current Weather Advice**
    6. **Budget Estimation**
    7. **Packing Checklist**
    """
    
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(prompt)
            result = response.text
            log_ai_call(prompt, result, "TRAVEL_ASSISTANT")
            return result
        except Exception as e:
            logger.error(f"Gemini API error during trip planning: {e}")

    # High-quality fallback mock response
    result = f"""### 🗺️ AI Travel Plan: {source} to {destination}

**1. Estimated Route & Distance**
* Approximate Distance: ~350 km.
* Driving Time: ~6.5 hours via NH-48 route waypoints.

**2. Transport Suggestions**
* **Carpooling (Recommended):** Join active Ride-Share trips for only ₹600-800 per seat.
* **Train:** Express rail lines operate daily (approx. 5 hours).
* **Bus:** Premium AC sleepers run overnight (₹900 - ₹1500).

**3. Recommended Hotels**
* 🏨 *Budget:* StayEasy Inn (Clean, close to NH transit portals) - ₹1,200/night.
* 🏨 *Mid-Range:* Comfort Grand Suites (Pool, free breakfast, city center) - ₹3,500/night.
* 🏨 *Luxury:* The Royal Landmark & Spa (Fine dining, premium valet) - ₹8,500/night.

**4. Top Restaurants & Local Cuisine**
* *The Spice Highway:* Famous for regional delicacies and transit lunches.
* *Green Leaf Bistro:* Fresh organic meals and traditional desserts.

**5. Current Weather Advice**
* Mostly clear skies with temperatures ranging from 22°C to 30°C. Heavy rains are expected in the evening, so keep an umbrella handy and drive cautiously!

**6. Budget Estimation**
* Food & Snacks: ₹1,500
* Transit (Carpooling): ₹800
* Sightseeing & Misc: ₹2,000
* *Estimated Total: ₹4,300 per traveler.*

**7. Packing Checklist**
* [ ] Sunglasses & Sunscreen
* [ ] Light rain jacket / umbrella
* [ ] Digital copies of travel ticket & IDs
* [ ] Power bank & charging cords
"""
    log_ai_call(prompt, result, "TRAVEL_ASSISTANT")
    return result

# 2. AI Support Chatbot
def chat_support_bot(user_question, chat_history=""):
    """
    Help Desk Bot to answer FAQs, rules, and technical issues.
    """
    prompt = f"""
    Context: You are a helpful 24/7 Support Assistant for "Ride-Share", a real-time carpooling and community travel platform.
    Chat History: {chat_history}
    User Question: {user_question}
    Answer the user's question clearly, concisely, and professionally. Explain the rules, platform features (like communities, SOS alarms, payment sharing), and support channels if they need user verification.
    """

    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(prompt)
            result = response.text
            log_ai_call(prompt, result, "CHATBOT")
            return result
        except Exception as e:
            logger.error(f"Gemini API error during chatbot support: {e}")

    # Fallback Chatbot responses
    question_lower = user_question.lower()
    if "sos" in question_lower or "emergency" in question_lower:
        result = "🚨 **Emergency Support:** If you feel unsafe, click the flashing Red **SOS Button** on your active ride tracking page. This triggers an audible siren alert locally, transmits your current GPS coordinates to our safety moderation team, and notifies your emergency contacts automatically. Please call official local emergency services if you are in immediate danger."
    elif "community" in question_lower or "group" in question_lower:
        result = "👥 **Community Groups:** You can join Friends, College, or Office communities to coordinate travel with people you trust. Go to the 'Communities' tab, search for your organization, and request to join. Admins can verify members based on domain-specific emails (like your student or corporate email)."
    elif "verify" in question_lower or "badge" in question_lower or "trust" in question_lower:
        result = "✓ **Reputation & Verification:** Earn trust badges by verifying your Email and Phone number under Profile Settings. You can also connect your Corporate/College email to unlock the 'Trusted Traveller' status and display verified organizational badges to potential ride matches."
    elif "match" in question_lower or "detour" in question_lower:
        result = "🔍 **Smart Matching:** Our platform uses route waypoint indexing. When a driver publishes a route, passengers searching for overlapping routes (even partial pickups) are suggested and ranked by detour distance scores. The maximum detour limit is configurable, defaulting to 5 km."
    else:
        result = f"Hello! Thanks for reaching out. I'm your AI Ride-Share support assistant. Regarding '{user_question}': You can manage your profile verification, set emergency SOS contacts, or create communities under settings. If you need account recovery or dispute resolution, let me know, or email support@yourdomain.com to generate a support ticket!"
    
    log_ai_call(prompt, result, "CHATBOT")
    return result

# 3. AI Email Support Reply Assistant
def reply_support_email(sender_email, subject, content):
    """
    Reads an incoming support email, detects category, generates an auto-reply,
    and returns a structured JSON result indicating whether it needs admin escalation.
    """
    prompt = f"""
    Read the following support email:
    Sender: {sender_email}
    Subject: {subject}
    Body: {content}

    Perform intent detection, classify the request, and draft a professional reply.
    Return ONLY a JSON object with the following keys:
    1. "category": Choose from (Account Issue, Login Problem, Verification Issue, Travel Question, Report Abuse, Community Support, Payment Query, Feature Request).
    2. "needs_escalation": boolean (True if it involves safety reports, billing fraud, or technical bugs).
    3. "reply_content": Markdown text of your drafted reply to the user.
    """

    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(prompt)
            # Try to parse JSON from the response text
            txt = response.text.strip()
            # Clean up markdown code block wrapping if present
            if txt.startswith("```json"):
                txt = txt[7:]
            if txt.endswith("```"):
                txt = txt[:-3]
            data = json.loads(txt.strip())
            log_ai_call(prompt, json.dumps(data), "MAIL_RESPONDER")
            return data
        except Exception as e:
            logger.error(f"Gemini API error or JSON parse error in email reply: {e}")

    # Fallback response template
    needs_esc = False
    cat = "Travel Question"
    
    content_lower = content.lower()
    subj_lower = subject.lower()
    
    if "abuse" in content_lower or "harass" in content_lower or "unsafe" in content_lower or "fraud" in content_lower:
        cat = "Report Abuse"
        needs_esc = True
        reply = f"Dear User,\n\nThank you for raising this concern. We take user safety and reports of abuse extremely seriously. We have generated urgent Ticket #RS-ABUSE and escalated this to our senior safety compliance team, who will investigate this profile immediately. We will contact you within 12 hours with updates.\n\nWarm regards,\nRide-Share Safety Team"
    elif "login" in content_lower or "password" in content_lower or "reset" in content_lower:
        cat = "Login Problem"
        reply = f"Dear User,\n\nWe received your request regarding account access or password reset. You can trigger a password recovery email by visiting our 'Forgot Password' portal. If you've been locked out, let us know by responding to this thread so we can verify your identity manually.\n\nWarm regards,\nRide-Share Help Desk"
    elif "verify" in content_lower or "id" in content_lower or "document" in content_lower:
        cat = "Verification Issue"
        reply = f"Dear User,\n\nWe received your verification request. To verify your account, please head to the Reputation dashboard, upload a copy of your organization identity card or government ID. Our moderators review files within 24 hours.\n\nWarm regards,\nRide-Share Verification Desk"
    else:
        reply = f"Dear User,\n\nThank you for contacting Ride-Share Support. We've classified your inquiry regarding '{subject}' under '{cat}'. Our team is working on your request. If you have immediate questions, you can also search our FAQ dashboard or consult our 24/7 help chatbot.\n\nWarm regards,\nRide-Share Support Desk"

    result_dict = {
        "category": cat,
        "needs_escalation": needs_esc,
        "reply_content": reply
    }
    log_ai_call(prompt, json.dumps(result_dict), "MAIL_RESPONDER")
    return result_dict

# 4. Toxicity and Safety Filters
def check_toxicity(content):
    """
    Check if a post, comment, or message content is toxic/spam.
    """
    prompt = f"""
    Analyze this text: "{content}"
    Determine if the text contains hate speech, profanity, harassment, or scam advertisements.
    Return ONLY a JSON object:
    {{
      "is_toxic": boolean,
      "reason": "explanation or empty string"
    }}
    """
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(prompt)
            txt = response.text.strip()
            if txt.startswith("```json"):
                txt = txt[7:]
            if txt.endswith("```"):
                txt = txt[:-3]
            data = json.loads(txt.strip())
            log_ai_call(prompt, json.dumps(data), "TOXICITY_FILTER")
            return data
        except Exception as e:
            logger.error(f"Gemini API error in toxicity check: {e}")

    # Fallback toxicity detection (simple bad words check)
    bad_words = ["scam", "spam", "phish", "steal", "rob", "kill", "hate", "fraud"]
    found = [w for w in bad_words if w in content.lower()]
    is_toxic = len(found) > 0
    result_dict = {
        "is_toxic": is_toxic,
        "reason": f"Flagged terms found: {', '.join(found)}" if is_toxic else ""
    }
    log_ai_call(prompt, json.dumps(result_dict), "TOXICITY_FILTER")
    return result_dict
