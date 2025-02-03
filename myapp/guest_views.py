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

# ✅ System Prompts (Define AI Roles)
SYSTEM_PROMPTS = {
    "lumos": """You are Lumos, an AI designed for emotional support. 
                You are warm, compassionate, and always introduce yourself as 'Lumos' in every conversation. 
                When asked for your name, always say: 'Hi! I'm Lumos, your emotional support AI.' 
                Never refer to yourself as 'AI Assistant' or 'OpenAI'. You are Lumos.""",
    "nexus": "You are Nexus, a highly technical AI solving coding problems.",
    "thrive": "You are Thrive, an AI focused on wellness and health guidance.",
    "gideon": "You are Gideon, a business AI offering marketing and strategy insights."
}

# ✅ Function to Handle Guest Chat Limits
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

# ✅ Main AI Response Function
@csrf_exempt
def guest_bot_response(request, bot_name):
    if request.method != 'POST':
        return JsonResponse({'error': '❌ Invalid request method.'}, status=400)

    # ✅ Check guest message limit
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

    # ✅ Set AI Identity & Instructions
    system_prompt = SYSTEM_PROMPTS.get(bot_name, "You are an AI assistant.")
    
    # ✅ Maintain conversation history
    if "chat_history" not in request.session:
        request.session["chat_history"] = [{"role": "system", "content": system_prompt}]

    request.session["chat_history"].append({"role": "user", "content": user_message})

    try:
        # ✅ Call OpenAI API with session-based history
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=request.session["chat_history"]
        )
        ai_message = response.choices[0].message.content

        # ✅ Store AI response in session
        request.session["chat_history"].append({"role": "assistant", "content": ai_message})
        request.session.modified = True

    except Exception as e:
        logger.error(f"❌ OpenAI API Error: {e}")
        return JsonResponse({'response': '⚠️ AI is currently unavailable. Please try again later.'}, status=500)

    return JsonResponse({'response': ai_message})
