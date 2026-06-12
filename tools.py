"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:

    listings = load_listings()
    description_tokens = set(description.lower().split())

    results = []

    for item in listings:
        # price filter
        if max_price is not None and item["price"] > max_price:
            continue

        # size filter (case-insensitive partial match like "S/M")
        if size is not None:
            if size.lower() not in item["size"].lower():
                continue

        # scoring (keyword overlap)
        text_blob = (
            item["title"] + " " +
            item["description"] + " " +
            " ".join(item["style_tags"])
        ).lower()

        score = sum(1 for token in description_tokens if token in text_blob)

        if score > 0:
            results.append((score, item))

    # sort by relevance
    results.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in results]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    client = _get_groq_client()

    items = wardrobe.get("items", [])

    # Case 1: empty wardrobe
    if not items:
        prompt = f"""
You are a fashion stylist.

A user just found this thrift item:
- Name: {new_item['title']}
- Description: {new_item['description']}
- Price: ${new_item['price']}

The user has NO wardrobe items.

Give general styling advice:
- what this item pairs well with
- outfit vibe
- 1–2 outfit ideas using generic clothing pieces
Keep it concise and practical.
"""
    else:
        wardrobe_text = "\n".join([
            f"- {i['name']} ({i['category']}, colors: {i['colors']})"
            for i in items
        ])

        prompt = f"""
You are a fashion stylist.

NEW ITEM:
- {new_item['title']}
- {new_item['description']}
- Category: {new_item['category']}

USER WARDROBE:
{wardrobe_text}

Task:
Suggest 1–2 complete outfits using ONLY wardrobe items plus the new item.
Be specific about combinations and styling.
Keep it conversational and aesthetic.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    client = _get_groq_client()

    if not outfit or outfit.strip() == "":
        return "Error: Cannot generate fit card because outfit suggestion is missing."

    prompt = f"""
You are writing a viral outfit caption for TikTok/Instagram.

RULES:
- 2–4 sentences max
- casual, aesthetic, slightly informal
- mention item name, price, platform ONCE each
- include outfit vibe
- do NOT sound like marketing copy
- make it feel like a real post
- vary wording each time

NEW ITEM:
- Name: {new_item['title']}
- Price: ${new_item['price']}
- Platform: {new_item['platform']}

OUTFIT:
{outfit}

Write the caption:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )

    return response.choices[0].message.content