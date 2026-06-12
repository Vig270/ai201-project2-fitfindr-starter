# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

Description - This project is an AI-powered fashion assistant that helps users discover secondhand clothing listings and generate outfit ideas based on their existing wardrobe.

It uses a multi-tool agent architecture with a planning loop that decides which tool to call based on user input and intermediate results.


## What's Included

ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── tools.py                   # Core tool implementations
├── agent.py                   # Planning loop (agent logic)
├── app.py                     # Gradio UI
├── planning.md                # Design + architecture spec
└── requirements.txt

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

data/listings.json contains 40 secondhand fashion listings across categories like tops, bottoms, outerwear, shoes, and accessories.

Each listing includes:

- id
- title
- description
- category
- style_tags
- size
- condition
- price
- colors
- brand
- platform

The agent filters and ranks these listings based on user queries.

Examples use:
from utils.data_loader import load_listings

listings = load_listings()

## The Wardrobe Schema

The wardrobe represents the user’s existing clothing items.

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: structure definition for items
- `example_wardrobe`: sample wardrobe for testing
- `empty_wardrobe`: baseline empty user closet

Load an example wardrobe with:

from utils.data_loader import get_example_wardrobe

wardrobe = get_example_wardrobe()

How FitFindr Works (Agent Overview)

FitFindr uses a 3-step tool pipeline:

1. Search for matching clothing listings
2. Generate outfit suggestions using wardrobe context
3. Create a social-media-style “fit card” caption

The agent uses a planning loop that dynamically decides whether to continue or stop based on search results.


Tools Overview
1. search_listings(description, size, max_price)

Searches the dataset for items matching the user’s request.

- Filters by:
    - keywords (description)
    - size (optional)
    - max price (optional)
- Returns ranked list of matching listings

If no results are found, returns an empty list and stops the workflow.


2. suggest_outfit(new_item, wardrobe)

Generates outfit combinations using:

- selected listing (new item)
- user's wardrobe items

If wardrobe is empty, returns general styling advice instead of failing.





3. create_fit_card(outfit, new_item)

Creates a short social-media-style caption for the outfit.

Includes:

- item name
- price
- platform
- outfit vibe

Returns a 2–4 sentence “OOTD-style” caption.

If outfit is missing, returns a clear error message.


Planning Loop (Agent Logic)

The agent follows this execution flow:

1. Parse user query into:
- description
- size
- max_price

2. Call:
search_listings()

3. If no results:
    - set error message
    - STOP execution

4. Otherwise:
select top result

5. Call:
suggest_outfit()

6. Store outfit result

7. Call:
create_fit_card()

8. Return final session output to UI


State Management

The agent uses a session dictionary to pass data between tools:

session = {
    "parsed": {},
    "search_results": [],
    "selected_item": None,
    "outfit_suggestion": None,
    "fit_card": None,
    "error": None
}

Each tool writes to session state so that later tools do not need to recompute earlier results.


Error Handling
Tool	| Failure Case	| Behavior
search_listings | 	No matches found | 	Stop workflow and return error
suggest_outfit | 	Empty wardrobe | 	Return general styling advice
create_fit_card | 	Empty outfit input | 	Return error message


Example Failure Behavior
If no listings match the query:
    - The agent returns:
    - “No matching listings found. Try different keywords, size, or budget.”
The workflow stops immediately and does not call further tools.



1. Tool Implementation
I used ChatGPT to help design and debug the filtering logic in search_listings, especially keyword scoring and size matching.

2. Prompt Engineering
I used AI to refine prompts for:
suggest_outfit
create_fit_card
I adjusted prompts to ensure outputs are:
conversational
realistic (not marketing tone)
stylistically consistent with fashion/social media posts

## Where to Start

1. Read planning.md and complete all sections before writing any code. This defines the agent’s tools, planning loop, state flow, and failure handling.
2. Verify the dataset loads correctly by running: python utils/data_loader.py
This should print a sample listing and wardrobe items to confirm everything is wired properly.

3. Implement and test each tool in tools.py individually (Milestone 3) before connecting them to the agent loop. Each tool should be tested for both normal cases and failure cases using pytest:
python -m pytest tests/

4. Wire the tools into the planning loop in agent.py (Milestone 4) after all tools work in isolation. Ensure state flows correctly between steps and that the agent stops early on errors.

5. Run the full application using: python app.py
and test both success and failure paths through the Gradio interface.
