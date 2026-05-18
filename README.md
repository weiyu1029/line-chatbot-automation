#  AI Operations Ticket Routing System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![LINE API](https://img.shields.io/badge/LINE_API-00C300?style=for-the-badge&logo=line&logoColor=white)
![Automation](https://img.shields.io/badge/Workflow-Automation-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An operations workflow automation project that classifies LINE user messages, assigns issue severity tiers, routes cases to responsible teams, and logs tickets for follow-up.

---

##  Project Overview

This project simulates an internal operations support system for retail, logistics, and store operations teams.

The system receives unstructured messages through LINE, classifies the issue, assigns it to the right owner, determines the urgency level, and records the case as a ticket.

It was designed as a portfolio project to demonstrate chatbot integration, workflow automation, routing logic, and operations analytics thinking.

---

##  Business Problem

Operations teams often receive large volumes of unstructured messages from stores, customers, drivers, and internal teams.

Common issues include:

- Inventory shortages
- Customer complaints
- Delivery delays
- Store operation issues
- System errors
- Pricing or promotion problems
- Payment issues
- Product quality concerns

Without automation, these messages require manual review, routing, and follow-up. This project reduces manual coordination work by routing issues to the right responsible team automatically.

---

##  Key Features

- LINE chatbot integration
- Webhook-based Flask backend
- Rule-based issue classification
- Multi-category detection
- Tier 0 / Tier 1 / Tier 2 urgency assignment
- Owner routing logic
- Ticket logging to CSV
- Daily summary generation
- Cloudflare Tunnel for local webhook testing
- Portfolio-ready demo structure

---

##  Tier Logic

| Tier | Meaning | Example |
|---|---|---|
| Tier 0 | AI / automation can respond directly | FAQ, simple process questions |
| Tier 1 | Human review needed, not urgent | Store hours, shelf updates, delivery follow-up |
| Tier 2 | Urgent escalation | Stockout, customer complaint, payment issue, system error, food safety issue |

---

##  Owner Mapping

| Category | Responsible Owner | Tier |
|---|---|---|
| Inventory Issue | Procurement Team | Tier 2 |
| Customer Complaint | Customer Support Team | Tier 2 |
| Delivery Issue | Logistics Team | Tier 1 |
| Store Operations | Store Manager | Tier 1 |
| System Issue | IT Team | Tier 2 |
| Pricing / Promotion Issue | Commercial Team | Tier 1 |
| Payment Issue | Finance Team | Tier 2 |
| Food Safety / Quality Issue | Quality Assurance Team | Tier 2 |
| General FAQ | AI Bot | Tier 0 |

---

##  System Architecture

<img src="images/architecture.png" width="850">

```txt
LINE User Message
        ↓
LINE Messaging API
        ↓
Webhook URL
        ↓
Flask Backend
        ↓
Issue Classification Engine
        ↓
Tier Assignment
        ↓
Owner Routing
        ↓
Ticket Log + LINE Response
        ↓
Daily Summary
```

---

##  Demo

### LINE Chatbot Demo

> Add your screenshot here after testing the bot.

```md
<img src="images/demo_chatbot.png" width="420">
```

### Example Bot Output

```txt
 AI Operations Router

Message received:
"The store is out of milk and customers are complaining."

Classification:
Category: Customer Complaint | Inventory Issue | Store Operations
Responsible Owner: Customer Support Team | Procurement Team | Store Manager
Tier Level: Tier 2

 This issue requires urgent escalation.

Suggested Actions:
- Inventory Issue: Check inventory levels, confirm replenishment plan, and notify the store manager.
- Customer Complaint: Escalate to customer support and prepare service recovery communication.
- Store Operations: Route to the store manager for operational follow-up.

Ticket Status:
 Logged successfully
```

---

##  Tech Stack

- Python
- Flask
- LINE Messaging API
- Cloudflare Tunnel
- CSV logging
- Rule-based NLP classification

---

##  Repository Structure

```txt
ai-operations-ticket-router/
│
├── app.py
├── daily_summary.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
│
├── data/
│   ├── owner_mapping.csv
│   └── sample_messages.csv
│
├── outputs/
│   ├── ticket_log.csv          # generated locally
│   └── daily_summary.txt       # generated locally
│
└── images/
    ├── architecture.png
    └── demo_chatbot.png
```

---

##  Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env`

Copy `.env.example` to `.env` and add your own LINE credentials.

```bash
cp .env.example .env
open -e .env
```

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
```

### 3. Run Flask

```bash
python3 app.py
```

The backend runs on:

```txt
http://127.0.0.1:5050
```

### 4. Start Cloudflare Tunnel

```bash
cloudflared tunnel --url http://127.0.0.1:5050
```

### 5. Update LINE Webhook URL

```txt
https://your-cloudflare-url.trycloudflare.com/callback
```

---

##  Sample Test Messages

```txt
The store is out of milk and customers are complaining.
```

Expected classification:

```txt
Category: Inventory Issue + Customer Complaint + Store Operations
Owner: Procurement Team + Customer Support Team + Store Manager
Tier: Tier 2
```

```txt
The driver is late and the order has not arrived.
```

Expected classification:

```txt
Category: Delivery Issue
Owner: Logistics Team
Tier: Tier 1
```

```txt
系統無法登入，店長說訂單也沒辦法確認
```

Expected classification:

```txt
Category: System Issue + Store Operations
Owner: IT Team + Store Manager
Tier: Tier 2
```

---

##  Ticket Log

The system automatically logs every routed message into:

```txt
outputs/ticket_log.csv
```

Example schema:

```txt
timestamp,user_message,categories,owners,tier,matched_keywords
```

---

##  Daily Summary

Generate a summary report:

```bash
python3 daily_summary.py
```

Output:

```txt
outputs/daily_summary.txt
```

---

##  Security Notes

Do not commit `.env` or real API credentials to GitHub.

Use `.env.example` for placeholders only.

If a token is accidentally exposed, rotate it immediately in the LINE Developers Console or relevant API dashboard.

---

##  Future Improvements

- Add OpenAI-based intent classification
- Generate daily email summaries
- Build a Streamlit dashboard for ticket analytics
- Add ticket status tracking
- Add Google Sheets integration
- Deploy backend to Render or Railway
- Add authentication and admin interface
- Add Slack / email escalation for Tier 2 issues

---

##  Project Goal

The goal of this project is to demonstrate how chatbot automation and operations analytics can reduce manual routing work, improve response speed, and create structured operational data from unstructured messages.
