"""
🕵️  CEO / FOUNDER RESEARCH AGENT
OpenClaw-Inspired Autonomous Exploration
"""

from tools import search_web, extract_text, is_valid_content
from memory import add_to_memory, get_memory, clear_memory
import ollama
import json
import sys
import os


# ─────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"


C = Colors


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(f"\n{C.CYAN}{C.BOLD}AI Research Agent (OpenClaw Style){C.RESET}\n")


def status(msg, color=C.WHITE):
    print(f"{color}› {msg}{C.RESET}")


def success(msg):
    print(f"{C.GREEN}✔ {msg}{C.RESET}")


def warn(msg):
    print(f"{C.YELLOW}⚠ {msg}{C.RESET}")


def error(msg):
    print(f"{C.RED}✘ {msg}{C.RESET}")


# ─────────────────────────────────────────────
# AGENT LOGIC
# ─────────────────────────────────────────────

def planner(name):
    return [
        f"{name} early life and education",
        f"{name} companies and startups",
        f"{name} achievements and awards",
        f"{name} recent news",
    ]


# 🔥 STRICT ANALYZE (LOW HALLUCINATION)
def analyze(text):
    try:
        response = ollama.chat(
            model='phi3',
            messages=[
                {
                    'role': 'user',
                    'content': f"""
You are a factual AI researcher.

STRICT RULES:
- Only use the given text
- Do NOT guess or assume
- Do NOT add new names
- If information is missing, write "Not Available"

Return structured output:

Early Life:
Companies:
Achievements:

Text:
{text}
"""
                }
            ]
        )
        return response['message']['content']
    except:
        return "Analysis failed."


# 🔥 CLEAN OUTPUT (REMOVE WEAK RESPONSES)
def clean_output(text):
    if not text or len(text.strip()) < 50:
        return "Insufficient data found."
    return text


def run_agent(name):
    clear_memory()  # ✅ VERY IMPORTANT

    tasks = planner(name)

    for task in tasks:
        print(f"\n🔍 Searching: {task}")

        links = search_web(task)

        # 🔁 fallback
        if not links:
            warn("No links found, trying fallback...")
            links = search_web(f"{task} biography")

        for link in links[:2]:
            status(f"Visiting: {link}")

            content = extract_text(link)

            if not content or not is_valid_content(content):
                warn("Skipping bad content")
                continue

            print("🧠 Analyzing...")

            raw_insight = analyze(content)
            insight = clean_output(remove_citations(raw_insight))

            add_to_memory({
                "task": task,
                "source": link,
                "insight": insight
            })

            success("Insight stored")


def generate_output(name):
    memory = get_memory()

    if not memory:
        error("No data collected")
        return {}

    combined = "\n\n".join([m["insight"] for m in memory])

    # 🔥 STRICT FINAL SUMMARY (VERY IMPORTANT)
    final_summary = analyze(f"""
Create a clean and well-structured biography of {name}.

STRICT RULES:
- Do NOT merge sections incorrectly
- Do NOT repeat text
- Do NOT include citations like [1], [2]
- Use bullet points where needed
- Keep sections clearly separated

FORMAT:

### Early Life & Education
### Companies
### Achievements

ONLY use the given data.

DATA:
{combined[:4000]}
""")

    return {
        "Person": name,
        "Summary": final_summary,
        "Sources": list(set([m["source"] for m in memory]))
    }

def remove_citations(text):
    import re
    return re.sub(r"\[\d+\]", "", text)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    clear()
    banner()

    name = input("Enter Founder/CEO name: ")

    if not name:
        error("No input provided")
        sys.exit()

    run_agent(name)

    result = generate_output(name)

    print("\n✅ FINAL OUTPUT:\n")
    print(json.dumps(result, indent=4))

    with open("output.json", "w") as f:
        json.dump(result, f, indent=4)

    success("Saved to output.json")