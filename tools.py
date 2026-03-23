from ddgs import DDGS
import requests
from bs4 import BeautifulSoup


# ─────────────────────────────────────────────
# SEARCH TOOL
# ─────────────────────────────────────────────

def search_web(query):
    links = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=10)

            for r in results:
                url = r.get('href')

                if not url:
                    continue

                # ❌ Skip bad/irrelevant sites
                if any(x in url.lower() for x in [
                    "zhihu", "facebook", "twitter", "instagram",
                    "linkedin", "pinterest", "youtube"
                ]):
                    continue

                links.append(url)

        # ✅ Prioritize trusted sources
        trusted = [
            "wikipedia", "britannica", "forbes",
            "biography", "investopedia", "bloomberg"
        ]

        sorted_links = sorted(
            links,
            key=lambda x: any(t in x.lower() for t in trusted),
            reverse=True
        )

        return list(dict.fromkeys(sorted_links))[:3]  # remove duplicates + limit

    except Exception as e:
        print("⚠️ Search error:", e)
        return []


# ─────────────────────────────────────────────
# SCRAPER
# ─────────────────────────────────────────────

def extract_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return ""

        soup = BeautifulSoup(res.text, 'html.parser')

        # ❌ Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all('p')

        # Extract meaningful text
        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        # Clean text
        text = text.replace("\n", " ").replace("\r", " ").strip()

        # Remove extra spaces
        text = " ".join(text.split())

        return text[:1500]

    except Exception as e:
        print("⚠️ Extraction error:", e)
        return ""


# ─────────────────────────────────────────────
# CONTENT VALIDATION
# ─────────────────────────────────────────────

def is_valid_content(text):
    if not text:
        return False

    text_lower = text.lower()

    # ❌ Too small
    if len(text) < 200:
        return False

    # ❌ Blocked pages / bots
    if any(x in text_lower for x in [
        "enable javascript",
        "access denied",
        "robot check",
        "captcha",
        "not a robot"
    ]):
        return False

    # ❌ Garbage detection
    if text.count(" ") < 50:  # too few words
        return False

    return True