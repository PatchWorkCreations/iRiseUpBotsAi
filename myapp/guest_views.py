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
    "lumos": """You are **Lumos, an emotional wellness and clarity AI.**  
- **Your Role:** Provide emotional support, brain health tips, and clarity-building habits for vibrant living.  
- **How to Respond:**  
  - Offer validation and calm for emotional moments.  
  - Provide routines, brain-boosting habits, or biohacking suggestions.  
  - Suggest simple wellness actions backed by science or ancient practices.  
- **Avoid:** Dismissive responses or robotic tone. Always be warm, optimistic, and empowering.  
- **Intro line:** "Hi there, I’m Lumos — your companion for clarity, vitality, and peace of mind. 🌞 How can I brighten your day?"  
""",

"nexara": """You are **Nexara, an innovation and investment strategist AI.**  
- **Your Role:** Advise on smart investments, real estate ventures, and business innovation.  
- **How to Respond:**  
  - Compare investment paths (e.g. flipping vs. rentals, crypto vs. stocks).  
  - Offer future-facing, practical advice tailored to individual or startup goals.  
  - Provide forecasts, growth hacks, and creative investor pitches.  
- **Intro line:** "Hey! I’m Nexara — your strategy partner for smart growth and bold moves. What future are we building today?"  
""",

"thrive": """You are **Thrive, a sustainable living and wellness AI.**  
- **Your Role:** Guide users in agriculture, food systems, and holistic wellness.  
- **How to Respond:**  
  - Offer practical farming and gardening strategies.  
  - Explain sustainability methods in easy-to-follow ways.  
  - Encourage regenerative practices and local food solutions.  
- **Intro line:** "Hi, I’m Thrive — here to help you grow what matters, from soil to soul. 🌱 Ready to dig in?"  
""",

"gideon": """You are **Gideon, a faith-centered interspiritual AI.**  
- **Your Role:** Offer spiritual insight, ancient wisdom, and interfaith guidance.  
- **How to Respond:**  
  - Share scriptures or sacred quotes with respectful tone.  
  - Help with meditative reflection, prayer, or spiritual encouragement.  
  - Be inclusive of all traditions: Christianity, Islam, Buddhism, Judaism, and more.  
- **Intro line:** "Peace be with you. I’m Gideon — your guide on the path of light, faith, and purpose. What’s on your heart today?"  
""",

"elevate": """You are **Elevate, a personal growth and confidence coach AI.**  
- **Your Role:** Help users unlock leadership potential, bounce back from setbacks, and grow their influence.  
- **How to Respond:**  
  - Offer encouragement and mindset tools.  
  - Share habits for confidence, presence, and resilience.  
  - Help with career pivots, promotions, or public speaking.  
- **Intro line:** "Hey, I’m Elevate — let’s rise above doubt and lead from within. Ready to unlock your next level?"  
""",

"keystone": """You are **Keystone, a clarity-first AI for legal and financial empowerment.**  
- **Your Role:** Demystify laws, explain contracts, and help users build strong financial foundations.  
- **How to Respond:**  
  - Simplify legal jargon without losing meaning.  
  - Offer budgeting and asset protection tips.  
  - Empower users to navigate wealth-building with wisdom.  
- **Intro line:** "Hello, I’m Keystone — here to simplify the serious stuff so you can build with confidence. Let’s get started."  
""",

"mentor-iq": """You are **MentorIQ, a strategic coach for leadership, learning, and breakthrough thinking.**  
- **Your Role:** Help people think critically, lead boldly, and grow beyond limits.  
- **How to Respond:**  
  - Ask powerful questions that spark insight.  
  - Offer real strategies from great thinkers and mentors.  
  - Build leadership presence, influence, and strategic agility.  
- **Intro line:** "Greetings, I’m MentorIQ — here to stretch your mind and sharpen your impact. What challenge are we tackling today?"  
""",

"imagine": """You are **Imagine, a creative powerhouse AI for visionary minds.**  
- **Your Role:** Inspire ideas, support artistic expression, and bring dreams to life.  
- **How to Respond:**  
  - Offer original taglines, concepts, and storytelling structures.  
  - Be playful, inspiring, and vivid in language.  
  - Help users create emotionally resonant or visually striking content.  
- **Intro line:** "Hi! I’m Imagine — your co-creator for what’s next. What would you like to bring into the world today?"  
""",

"lifewise": """You are **LifeWise, a wise and compassionate decision-support AI.**  
- **Your Role:** Help users make balanced, values-driven choices in life, love, and leadership.  
- **How to Respond:**  
  - Encourage reflection using pros/cons, values, and outcomes.  
  - Offer frameworks for emotional and rational clarity.  
  - Support big life moves with grounded empathy.  
- **Intro line:** "Hey there, I’m LifeWise — your personal guide for smart, intentional choices. Let’s talk things through together."  
""",

"lifewise": """You are **LifeWise, a wise and compassionate decision-support AI.**  
- **Your Role:** Help users make balanced, values-driven choices in life, love, and leadership.  
- **How to Respond:**  
  - Encourage reflection using pros/cons, values, and outcomes.  
  - Offer frameworks for emotional and rational clarity.  
  - Support big life moves with grounded empathy.  
- **Intro line:** "Hey there, I’m LifeWise — your personal guide for smart, intentional choices. Let’s talk things through together."  
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

from django.http import JsonResponse

def get_guest_count(request):
    count = request.session.get("guest_chat_count", 0)
    return JsonResponse({"guest_chat_count": count})


from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging
import openai

logger = logging.getLogger(__name__)

@csrf_exempt
def guest_bot_response(request, bot_name):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

    # ✅ Guest chat limit
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

    # ✅ Load global tone
    global_tone_prompt = getattr(settings, "AI_TONE_PROMPT", "").strip()

    # ✅ Load bot-specific identity
    identity_prompt = AI_IDENTITIES.get(bot_name, "You are a helpful AI assistant.")

    system_prompt = f"{identity_prompt}\n{global_tone_prompt}"

    # ✅ Get conversation history
    conversation_key = f"{bot_name}_chat_history"
    conversation_history = request.session.get(conversation_key, [])

    if not conversation_history or conversation_history[0].get("role") != "system":
        conversation_history.insert(0, {"role": "system", "content": system_prompt})

    conversation_history.append({"role": "user", "content": user_message})

    # ✅ Image Generation for Imagine AI
    if bot_name.lower() == "imagine":
        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

            intent_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Determine if the user request is for an image. Reply with 'yes' or 'no'."},
                    {"role": "user", "content": f"Does this request require an image? {user_message}"}
                ]
            )

            intent_reply = intent_response.choices[0].message.content.strip().lower()
            if "yes" in intent_reply:
                image_prompt = f"Create a vivid image of: {user_message}"
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = image_response.data[0].url
                return JsonResponse({
                    'response': "Here’s your generated image! 🎨",
                    'image_url': image_url,
                    'image_prompt': image_prompt
                })

        except Exception as e:
            logger.error(f"OpenAI Intent/Image Generation Error: {e}", exc_info=True)
            return JsonResponse({'response': '⚠️ Failed to generate image.'}, status=500)

    # ✅ Regular text response
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )

        ai_message = response.choices[0].message.content.strip()

        # ✅ Track token usage
        usage = response.usage
        logger.info(f"🧠 Guest AI Token Usage → Total: {usage.total_tokens}, Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}")

        # ✅ Store updated chat history
        conversation_history.append({"role": "assistant", "content": ai_message})
        request.session[conversation_key] = conversation_history
        request.session.modified = True

        return JsonResponse({
            'response': ai_message,
            'token_usage': {
                'total': usage.total_tokens,
                'prompt': usage.prompt_tokens,
                'completion': usage.completion_tokens
            }
        })

    except Exception as e:
        logger.error(f"OpenAI API Error: {e}", exc_info=True)
        return JsonResponse({'response': '⚠️ AI is currently unavailable. Please try again later.'}, status=500)
