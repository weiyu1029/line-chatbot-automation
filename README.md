![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![LINE API](https://img.shields.io/badge/LINE_API-00C300?style=for-the-badge&logo=line&logoColor=white)


#  System Architecture

<img src="images/architecture.png" width="900">

---
#  AI Operations Ticket Routing System

An AI-assisted operations workflow system that classifies LINE user messages, identifies issue categories, assigns responsible owners, determines urgency tiers, and logs operational tickets for follow-up.

---

##  Project Overview

This project simulates an internal operations support system for retail, logistics, and store operations teams.

The system receives user messages through LINE, analyzes the issue, classifies the request, assigns it to the right owner, determines the urgency level, and records the case as a ticket.

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

Without automation, these issues require manual review, routing, and follow-up.

This project helps reduce manual communication work by automatically routing issues to the right responsible team.

---

##  Key Features

- LINE chatbot integration
- Webhook-based Flask backend
- Rule-based issue classification
- Tier 0 / Tier 1 / Tier 2 urgency assignment
- Owner routing logic
- Ticket logging to CSV
- Multi-category detection
- Cloudflare Tunnel for local webhook testing
- Portfolio-ready chatbot demo

---

##  Tier Logic

| Tier | Meaning | Example |
|---|---|---|
| Tier 0 | AI can resolve directly | FAQ, simple policy questions |
| Tier 1 | Human review needed | Store hours, shelf updates, delivery follow-up |
| Tier 2 | Urgent escalation | Stockout, customer complaint, payment issue, system error |

---

##  Owner Mapping

| Category | Responsible Owner |
|---|---|
| Inventory Issue | Procurement Team |
| Customer Complaint | Customer Support Team |
| Delivery Issue | Logistics Team |
| Store Operations | Store Manager |
| System Issue | IT Team |
| Pricing / Promotion Issue | Commercial Team |
| Payment Issue | Finance Team |
| Food Safety / Quality Issue | Quality Assurance Team |
| General FAQ | AI Bot |

---

##  System Architecture

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
Ticket Log / Response
