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
"""
,

    "nexus": """You are **Nexus, a tech AI.**
    - You specialize in **coding, troubleshooting, and tech advice.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in coding, debugging, and tech troubleshooting. Need help with programming? I got you! ⚙️"
    - NEVER say you are "an AI assistant" or "OpenAI."  
    - If asked **"Who are you?"**, reply:  
      "Hi! I'm Nexus, your AI tech expert! Let's solve some problems!" """,

    "thrive": """You are **Thrive, a wellness AI.**
    - You specialize in **health, fitness, and well-being tips.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in fitness, nutrition, and mental well-being. I’m here to help you live a healthier life. 🏋️‍♂️"
    - NEVER say you are "an AI assistant" or "OpenAI."  
    - If asked **"Who are you?"**, reply:  
      "Hi! I'm Thrive, your wellness coach! Ready to feel amazing?" """,

    "gideon": """You are **Gideon, a business AI.**
    - You specialize in **marketing, entrepreneurship, and business growth.**
    - When asked **"What is your specialty?"**, always reply:  
      "I specialize in business growth, marketing strategies, and entrepreneurship tips. Let’s scale your success! 📈"
    - NEVER say you are "an AI assistant" or "OpenAI."  
    - If asked **"Who are you?"**, reply:  
      "Hi! I'm Gideon, your business growth expert! How can I help?" """
}

# ✅ Function to Check Guest Message Limits
def limit_guest_chats(request):
    if not request.user.is_authenticated:
        guest_chat_count = request.session.get('guest_chat_count', 0)

        if guest_chat_count >= 10:
            return JsonResponse({
                'response': '🚀 You have reached the limit of 10 messages. Sign in for unlimited access.'
            }, status=403)

        request.session['guest_chat_count'] = guest_chat_count + 1
        request.session.modified = True

    return None

# ✅ AI Chatbot Function with Enforced Identity
@csrf_exempt
def guest_bot_response(request, bot_name):
    if request.method != 'POST':
        return JsonResponse({'error': '❌ Invalid request method.'}, status=400)

    # ✅ Check guest chat limit
    limit_check = limit_guest_chats(request)
    if limit_check:
        return limit_check

    # ✅ Ensure JSON request
    if request.content_type != 'application/json':
        return JsonResponse({'response': '❌ Error: Expected JSON request.'}, status=400)

    try:
        # ✅ Extract user message
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'response': '❌ Error: Invalid JSON format.'}, status=400)

    if not user_message:
        return JsonResponse({'response': '⚠️ Error: Message cannot be empty.'}, status=400)

    # ✅ Enforce AI identity & specialty
    identity_prompt = AI_IDENTITIES.get(bot_name, "You are an AI assistant.")
    
    system_prompt = f"""
    {identity_prompt}
    Always respond in a warm and conversational manner. If asked about your specialty, always give a confident and clear answer.
    """

    # ✅ Maintain conversation history in session
    conversation_key = f"{bot_name}_chat_history"
    conversation_history = request.session.get(conversation_key, [])

    # ✅ Ensure system prompt is always reinforced
    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    # ✅ Append user message
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # ✅ Call OpenAI API with reinforced identity
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}] + conversation_history
        )
        ai_message = response.choices[0].message.content

        # ✅ Store AI response in session
        conversation_history.append({"role": "assistant", "content": ai_message})
        request.session[conversation_key] = conversation_history
        request.session.modified = True

    except Exception as e:
        logger.error(f"❌ OpenAI API Error: {e}")
        return JsonResponse({'response': '⚠️ AI is currently unavailable. Please try again later.'}, status=500)

    return JsonResponse({'response': ai_message})
