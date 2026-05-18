import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

INPUT_FILE = Path("outputs/ticket_log.csv")
OUTPUT_FILE = Path("outputs/daily_summary.txt")


def generate_summary():
    if not INPUT_FILE.exists():
        summary = "No ticket log found. Send a few LINE messages first."
        OUTPUT_FILE.parent.mkdir(exist_ok=True)
        OUTPUT_FILE.write_text(summary, encoding="utf-8")
        print(summary)
        return

    with INPUT_FILE.open(newline="", encoding="utf-8") as file:
        tickets = list(csv.DictReader(file))

    if not tickets:
        summary = "No tickets found."
    else:
        total = len(tickets)
        tier_counts = Counter(t["tier"] for t in tickets)
        category_counts = Counter(t["categories"] for t in tickets)
        owner_counts = Counter(t["owners"] for t in tickets)
        by_tier = defaultdict(list)
        for t in tickets:
            by_tier[t["tier"]].append(t)

        lines = [
            "Daily Operations Ticket Summary",
            "=" * 40,
            f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Tickets: {total}",
            "",
            "Tickets by Tier:"
        ]
        for tier, count in tier_counts.items():
            lines.append(f"- {tier}: {count}")
        lines.append("")
        lines.append("Tickets by Owner:")
        for owner, count in owner_counts.items():
            lines.append(f"- {owner}: {count}")
        lines.append("")
        lines.append("Tickets by Category:")
        for category, count in category_counts.items():
            lines.append(f"- {category}: {count}")
        lines.append("")
        lines.append("High Priority Tickets:")
        for t in by_tier.get("Tier 2", []):
            lines.append(f"- [{t['timestamp']}] {t['user_message']}")
            lines.append(f"  Owner: {t['owners']}")
            lines.append(f"  Category: {t['categories']}")
            lines.append("")
        summary = "\n".join(lines)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    generate_summary()
