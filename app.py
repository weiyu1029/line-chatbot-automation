from flask import Flask, request
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from datetime import datetime
import os
import csv

load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

TICKET_LOG_FILE = "outputs/ticket_log.csv"

CATEGORY_RULES = {
    "Inventory Issue": {
        "keywords": [
            "out of stock", "stockout", "no stock", "inventory", "replenish", "restock", "shortage",
            "缺貨", "沒貨", "補貨", "庫存", "斷貨", "商品不足", "缺品", "牛奶沒了", "milk is out"
        ],
        "owner": "Procurement Team",
        "tier": "Tier 2",
        "action": "Check inventory levels, confirm replenishment plan, and notify the store manager."
    },
    "Customer Complaint": {
        "keywords": [
            "complaint", "complain", "angry", "refund", "bad experience", "customer is upset", "customers are complaining",
            "客訴", "抱怨", "退款", "生氣", "投訴", "顧客不滿", "負評", "服務不好"
        ],
        "owner": "Customer Support Team",
        "tier": "Tier 2",
        "action": "Escalate to customer support and prepare service recovery communication."
    },
    "Delivery Issue": {
        "keywords": [
            "delivery", "late", "driver", "delay", "not arrived", "shipment", "配送", "延遲", "外送",
            "司機", "遲到", "送錯", "沒送到", "物流", "到貨延誤"
        ],
        "owner": "Logistics Team",
        "tier": "Tier 1",
        "action": "Check delivery status and follow up with the logistics team."
    },
    "Store Operations": {
        "keywords": [
            "store", "store manager", "shelf", "staff", "opening hours", "店", "門市", "店長",
            "貨架", "員工", "營業時間", "排班", "陳列", "門店", "櫃位", "現場"
        ],
        "owner": "Store Manager",
        "tier": "Tier 1",
        "action": "Route to the store manager for operational follow-up."
    },
    "System Issue": {
        "keywords": [
            "system", "bug", "error", "login", "crash", "cannot access", "系統", "錯誤", "當機",
            "無法登入", "頁面壞掉", "不能用", "系統異常"
        ],
        "owner": "IT Team",
        "tier": "Tier 2",
        "action": "Escalate to IT for troubleshooting and system status check."
    },
    "Pricing or Promotion Issue": {
        "keywords": [
            "price", "pricing", "discount", "promotion", "coupon", "價格", "折扣", "促銷",
            "優惠券", "活動", "標價", "價格錯誤", "折價", "特價"
        ],
        "owner": "Commercial Team",
        "tier": "Tier 1",
        "action": "Verify pricing or promotion setup with the commercial team."
    },
    "Payment Issue": {
        "keywords": [
            "payment", "paid", "charged", "card", "transaction", "invoice", "付款", "刷卡", "交易",
            "發票", "收款", "扣款", "信用卡", "付款失敗", "重複扣款"
        ],
        "owner": "Finance Team",
        "tier": "Tier 2",
        "action": "Review payment records and escalate to finance if needed."
    },
    "Food Safety or Quality Issue": {
        "keywords": [
            "expired", "spoiled", "quality", "broken", "damaged", "unsafe", "過期", "壞掉", "品質",
            "破損", "食品安全", "發霉", "異味", "不新鮮", "受損"
        ],
        "owner": "Quality Assurance Team",
        "tier": "Tier 2",
        "action": "Escalate immediately to QA and remove affected items if necessary."
    },
    "General FAQ": {
        "keywords": [
            "how to", "what is", "where", "when", "policy", "流程", "規則", "怎麼", "如何",
            "哪裡", "什麼時候", "政策", "說明"
        ],
        "owner": "AI Bot",
        "tier": "Tier 0",
        "action": "Provide standard guidance directly."
    }
}

TIER_PRIORITY = {"Tier 0": 0, "Tier 1": 1, "Tier 2": 2}


def detect_categories(message):
    text = message.lower()
    matched_results = []
    for category, rule in CATEGORY_RULES.items():
        matched_keywords = [keyword for keyword in rule["keywords"] if keyword.lower() in text]
        if matched_keywords:
            matched_results.append({
                "category": category,
                "owner": rule["owner"],
                "tier": rule["tier"],
                "action": rule["action"],
                "matched_keywords": matched_keywords
            })
    if not matched_results:
        matched_results.append({
            "category": "Unclassified General Inquiry",
            "owner": "AI Bot",
            "tier": "Tier 0",
            "action": "Provide a general response and monitor if human follow-up is needed.",
            "matched_keywords": []
        })
    return matched_results


def choose_highest_tier(results):
    return max((item["tier"] for item in results), key=lambda tier: TIER_PRIORITY[tier])


def build_reply(user_message, results):
    highest_tier = choose_highest_tier(results)
    categories = " | ".join(sorted(set(r["category"] for r in results)))
    owners = " | ".join(sorted(set(r["owner"] for r in results)))
    actions = "\n".join(f"- {r['category']}: {r['action']}" for r in results)

    urgency_note = {
        "Tier 2": "🚨 This issue requires urgent escalation.",
        "Tier 1": "⚠️ This issue needs human review.",
        "Tier 0": "✅ This looks like a Tier 0 issue that can be handled directly."
    }[highest_tier]

    return f"""🤖 AI Operations Router

Message received:
\"{user_message}\"

Classification:
Category: {categories}
Responsible Owner: {owners}
Tier Level: {highest_tier}

{urgency_note}

Suggested Actions:
{actions}

Ticket Status:
✅ Logged successfully
"""


def save_ticket(user_message, results):
    os.makedirs(os.path.dirname(TICKET_LOG_FILE), exist_ok=True)
    file_exists = os.path.isfile(TICKET_LOG_FILE)
    highest_tier = choose_highest_tier(results)
    categories = " | ".join(sorted(set(r["category"] for r in results)))
    owners = " | ".join(sorted(set(r["owner"] for r in results)))
    matched_keywords = " | ".join(",".join(r["matched_keywords"]) for r in results if r["matched_keywords"])

    with open(TICKET_LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "user_message", "categories", "owners", "tier", "matched_keywords"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_message,
            categories,
            owners,
            highest_tier,
            matched_keywords
        ])


@app.route("/", methods=["GET"])
def home():
    return "AI Operations Router is running!", 200


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    except Exception as e:
        print("Webhook error:", e)
        return "Internal Server Error", 500
    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    results = detect_categories(user_message)
    save_ticket(user_message, results)
    reply_text = build_reply(user_message, results)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
