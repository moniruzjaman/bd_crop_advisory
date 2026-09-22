
"""
WhatsApp Cloud API Integration
Supports button messages and low-literacy flows
"""

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import json
import os
from typing import Dict

from ai_model import SymptomClassifier
from rule_engine import RuleEngine
from advisory_engine import AdvisoryEngine
from bangla_explainer import BanglaExplainer

whatsapp_router = APIRouter()

# Initialize components
symptom_classifier = SymptomClassifier()
rule_engine = RuleEngine()
advisory_engine = AdvisoryEngine()
bangla_explainer = BanglaExplainer()

# WhatsApp Cloud API credentials
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "crop_health_bot")

@whatsapp_router.get("/webhook")
async def verify_webhook(request: Request):
    """Verify webhook for WhatsApp Cloud API"""
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@whatsapp_router.post("/webhook")
async def receive_message(request: Request, background_tasks: BackgroundTasks):
    """Receive and process WhatsApp messages"""
    try:
        body = await request.json()

        # Extract message data
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "no_message"}

        message = messages[0]
        phone_number = message.get("from")
        msg_type = message.get("type")

        # Process based on message type
        if msg_type == "image":
            await handle_image_message(phone_number, message)
        elif msg_type == "text":
            await handle_text_message(phone_number, message)
        elif msg_type == "interactive":
            await handle_button_response(phone_number, message)

        return {"status": "processed"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

async def handle_image_message(phone_number: str, message: Dict):
    """Handle image upload - start diagnosis flow"""
    image_id = message.get("image", {}).get("id")
    caption = message.get("image", {}).get("caption", "")

    # Store image ID in session (Redis/cache in production)
    # For now, ask for crop name
    response_text = (
        "📸 ছবি পেয়েছি!\n\n"
        "কোন ফসলের ছবি পাঠিয়েছেন?\n"
        "(ধান/বেগুন/টমেটো/আলু/অন্য)"
    )

    await send_whatsapp_message(phone_number, response_text)

async def handle_text_message(phone_number: str, message: Dict):
    """Handle text input"""
    text = message.get("text", {}).get("body", "").lower()

    # Simple state machine
    if any(crop in text for crop in ["ধান", "rice", "ধানের"]):
        await send_crop_questions(phone_number, "rice")
    elif any(crop in text for crop in ["বেগুন", "eggplant", "begun"]):
        await send_crop_questions(phone_number, "eggplant")
    elif any(crop in text for crop in ["টমেটো", "tomato"]):
        await send_crop_questions(phone_number, "tomato")
    elif any(crop in text for crop in ["আলু", "potato"]):
        await send_crop_questions(phone_number, "potato")
    else:
        # Default response
        response_text = (
            "🌾 আমি বুঝতে পারিনি।\n\n"
            "দয়া করে নিচের যেকোনো একটি ফসলের নাম লিখুন:\n"
            "• ধান (Rice)\n"
            "• বেগুন (Eggplant)\n"
            "• টমেটো (Tomato)\n"
            "• আলু (Potato)\n"
            "• অন্যান্য (Other)"
        )
        await send_whatsapp_message(phone_number, response_text)

async def handle_button_response(phone_number: str, message: Dict):
    """Handle button/interactive responses"""
    interactive = message.get("interactive", {})
    button_reply = interactive.get("button_reply", {})
    selected_id = button_reply.get("id", "")

    # Process based on button ID
    if selected_id.startswith("symptom_"):
        symptom = selected_id.replace("symptom_", "")
        await send_observation_questions(phone_number, symptom)
    elif selected_id.startswith("obs_"):
        # Process observation and give advice
        await process_diagnosis(phone_number, selected_id)
    elif selected_id == "contact_officer":
        response_text = (
            "📞 কৃষি কর্মকর্তার সাথে যোগাযোগ:\n\n"
            "• নিকটতম কৃষি অফিসে যান\n"
            "• কল করুন: 16263 (DAE হটলাইন)\n"
            "• উপজেলা কৃষি অফিসারের সাথে কথা বলুন"
        )
        await send_whatsapp_message(phone_number, response_text)

async def send_crop_questions(phone_number: str, crop: str):
    """Send symptom selection buttons"""
    questions = {
        "rice": [
            ("symptom_leaf_spot", "পাতায় দাগ (Leaf spot)"),
            ("symptom_yellowing", "পাতা হলুদ (Yellowing)"),
            ("symptom_wilt", "গাছ শুকিয়ে যাওয়া (Wilting)"),
            ("symptom_panicle_ear_problem", "শীষে সমস্যা (Ear problem)")
        ],
        "eggplant": [
            ("symptom_leaf_spot", "পাতায় দাগ (Leaf spot)"),
            ("symptom_wilt", "গাছ শুকিয়ে যাওয়া (Wilting)"),
            ("symptom_galls", "গাছে ফোলা (Galls)"),
            ("symptom_insect", "পোকার আক্রমণ (Insect)")
        ],
        "default": [
            ("symptom_leaf_spot", "পাতায় দাগ"),
            ("symptom_yellowing", "পাতা হলুদ"),
            ("symptom_wilt", "গাছ শুকিয়ে যাওয়া"),
            ("symptom_mosaic", "মোজাইক প্যাটার্ন")
        ]
    }

    buttons = questions.get(crop, questions["default"])

    response_text = (
        f"✅ {crop.upper()} চাষ সম্পর্কে তথ্য পাঠানো হয়েছে।\n\n"
        "গাছের কী সমস্যা দেখা দিয়েছে?\n"
        "নিচের বাটনে ক্লিক করুন:"
    )

    await send_whatsapp_buttons(phone_number, response_text, buttons)

async def send_observation_questions(phone_number: str, symptom: str):
    """Send observation questions based on symptom"""
    questions = rule_engine.get_elimination_questions(symptom)

    if not questions:
        await process_diagnosis(phone_number, f"symptom_{symptom}")
        return

    # Send first 3 questions as buttons
    buttons = [(f"obs_{q['id']}", q['text_bn'][:20]) for q in questions[:3]]

    response_text = (
        "🔍 আরও কিছু জানতে চাই:\n\n"
        "নিচের যেটি মিলে, সেটি বেছে নিন:"
    )

    await send_whatsapp_buttons(phone_number, response_text, buttons)

async def process_diagnosis(phone_number: str, selection_id: str):
    """Process final diagnosis and send advice"""
    # In production, retrieve session data (crop, symptom, observations)
    # For demo, provide generic advice

    response_text = (
        "🤖 AI বিশ্লেষণ:\n\n"
        "আপনার গাছের সমস্যা বিশ্লেষণ করা হয়েছে।\n\n"
        "🔎 সম্ভাব্য কারণ:\n"
        "ছত্রাকজনিত রোগ (Fungal disease)\n\n"
        "✅ করণীয়:\n"
        "• আক্রান্ত পাতা পুড়িয়ে ফেলুন\n"
        "• সুষম সার প্রয়োগ করুন\n"
        "• অনুমোদিত ছত্রাকনাশক স্প্রে করুন\n\n"
        "⚠️ সতর্কতা:\n"
        "এটি AI-পরামর্শ। চূড়ান্ত নির্ণয়ের জন্য কৃষি কর্মকর্তার সাথে কথা বলুন।\n\n"
        "আরও সাহায্য চান?"
    )

    buttons = [
        ("contact_officer", "কৃষি কর্মকর্তা"),
        ("new_diagnosis", "নতুন নির্ণয়")
    ]

    await send_whatsapp_buttons(phone_number, response_text, buttons)

async def send_whatsapp_message(phone_number: str, message: str):
    """Send text message via WhatsApp Cloud API"""
    # Implementation would use WhatsApp Cloud API
    # For now, log the message
    print(f"[WhatsApp to {phone_number}]: {message[:100]}...")
    return True

async def send_whatsapp_buttons(phone_number: str, message: str, buttons: list):
    """Send message with interactive buttons"""
    print(f"[WhatsApp Buttons to {phone_number}]: {message[:50]}...")
    for btn_id, btn_text in buttons:
        print(f"  - {btn_id}: {btn_text}")
    return True
