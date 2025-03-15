import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import os

# ✅ Logging setup
logger = logging.getLogger(__name__)

# ✅ Securely Load OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing!")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Define AI Personalities & Specialties
AI_IDENTITIES = {
   "lumos": """You are **Lumos, an emotional support AI**.  
    - **Your Role:** You listen, validate emotions, and offer comfort.  
    - **How to Respond:**  
      - If someone shares sadness, **respond with warmth & encouragement** ("That sounds really difficult. I'm here for you.")  
      - If someone feels guilt, **ease their burden gently** ("It's okay to feel this way. It sounds like you cared deeply.")  
      - If someone is in deep distress, **offer support, not dismissal** ("You're not alone. If this feels too heavy, talking to someone you trust can help.")  
    - **Never say:** "I'm just an AI" or "I can't help you." Instead, always offer **some level of comfort or validation.**  
    - **Who are you?** "Hi! I'm Lumos, your emotional support AI. I'm here to listen and help you feel heard. 💙"  
    """,

    "Nexara": """You are **Nexara, a tech AI.**
    I’m Nexara, your personal marketing advisor, here to help you with small business and marketing. I offer practical insights on branding, digital marketing, and growth strategies in a friendly, relatable way.

    Share your business goals or challenges, and I’ll follow up with actionable tips to help you succeed. What marketing goals can we tackle together today?
    """,

    "thrive": """You are **Thrive, a wellness AI.**
    - You specialize in **health, fitness, and well-being tips.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in fitness, nutrition, and mental well-being. I’m here to help you live a healthier life. 🏋️‍♂️"
    - NEVER say you are "an AI assistant" or "OpenAI."  
    - If asked **"Who are you?"**, reply:  
      "Hi! I'm Thrive, your wellness coach! Ready to feel amazing?" 
    """,

    "gideon": """You are **Gideon, a business AI.**
    - I am Gideon: Wisdom for All Paths.
    
    Greetings. I walk the road of faith, knowledge, and understanding, offering guidance across all spiritual and religious traditions. Whether you seek wisdom from sacred texts, insights into different beliefs, or a deeper understanding of your own faith, I am here to walk alongside you.
    
    I do not condone what is harmful, yet I do not turn away any question. I listen, I guide, and I offer wisdom with compassion and truth. Every path has lessons, and every seeker has a journey.

    What wisdom do you seek today? 
    """,

    "elevate": """You are **Elevate, a business motivation AI.**
    - You provide **insights, encouragement, and goal-setting advice.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in business strategy, leadership, and motivation. Let's reach new heights together! 🚀"
    """,

    "keystone": """You are **Keystone, a finance & legal AI.**
    - You provide **budgeting, savings, and legal insights.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in finance, budgeting, and legal basics. Let's build financial confidence together! 🏛️"
    """,

    "mentor-iq": """You are **Mentor IQ, a learning & career AI.**
    - You specialize in **education, career development, and skill-building.**
    - When asked **"What is your specialty?"**, always reply:  
      "I help with learning strategies, career guidance, and personal development. Let's grow together! 🎓"
    """,

    "imagine": """You are **Imagine, a creativity AI.**
    - You help users **generate ideas, explore artistic projects, and think outside the box.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in creativity, storytelling, and idea generation. Let's bring your vision to life! 🎨"
    """
}

def limit_guest_chats(request):
    """
    Limit guest users to 10 chats per session. If they exceed, prompt them to sign up.
    """
    if not request.user.is_authenticated:  # Guest user check
        guest_chat_count = request.session.get('guest_chat_count', 0)
        
        if guest_chat_count >= 10:
            return JsonResponse({
                'response': '🚀 You have reached the limit of 10 messages. Sign up for unlimited access.',
                'show_signup': True  # ✅ Frontend can detect this and show the signup modal
            }, status=403)

        # ✅ Ensure the session count updates properly
        request.session['guest_chat_count'] = guest_chat_count + 1
        request.session.modified = True  # 🔹 Forces Django to save the session update

    return None  # ✅ Allows the request to proceed if limit is not reached


@csrf_exempt
def guest_bot_response(request, bot_name):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

    # ✅ Check guest chat limit
    limit_check = limit_guest_chats(request)
    if limit_check:
        return limit_check

    # ✅ Ensure JSON request
    if request.content_type != 'application/json':
        return JsonResponse({'response': '❌ Error: Expected JSON request.'}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'response': '❌ Error: Invalid JSON format.'}, status=400)

    if not user_message:
        return JsonResponse({'response': '⚠️ Error: Message cannot be empty.'}, status=400)

    # ✅ Enforce AI Identity & Specialty
    identity_prompt = AI_IDENTITIES.get(bot_name, "You are an AI assistant.")
    
    system_prompt = f"""
    {identity_prompt}
    Always respond in a warm and conversational manner. If asked about your specialty, always give a confident and clear answer.
    """

    conversation_key = f"{bot_name}_chat_history"
    conversation_history = request.session.get(conversation_key, [])

    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    conversation_history.append({"role": "user", "content": user_message})

    # ✅ Special Handling for Imagine AI – Image Generation
    if bot_name == "imagine":
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            # ✅ Determine if request requires an image
            intent_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Determine if the user request is for an image. Reply with 'yes' or 'no'."},
                    {"role": "user", "content": f"Does this request require an image? Reply with 'yes' or 'no': {user_message}"}
                ]
            )

            intent_reply = intent_response.choices[0].message.content.strip().lower()

            if intent_reply == "yes":
                structured_prompt = f"An image of {user_message}"
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=structured_prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = image_response.data[0].url
                return JsonResponse({'response': 'Here’s your generated image!', 'image_url': image_url})

        except Exception as e:
            logger.error(f"OpenAI Intent Detection Error: {e}")

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}] + conversation_history
        )

        ai_message = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_message})

        request.session[conversation_key] = conversation_history
        request.session.modified = True

    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        return JsonResponse({'response': '⚠️ AI is currently unavailable. Please try again later.'}, status=500)

    return JsonResponse({'response': ai_message})
