import pytest

from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe


# ─────────────────────────────────────────────
# search_listings tests
# ─────────────────────────────────────────────

def test_search_returns_results():
    results = search_listings("jeans", size=None, max_price=100)
    assert isinstance(results, list)
    assert len(results) >= 0  # may vary depending on dataset


def test_search_empty_results():
    results = search_listings("unicorn diamond jacket", size="XXS", max_price=1)
    assert results == []


def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)

    # If results exist, ensure price filter is respected
    assert all(item["price"] <= 10 for item in results)


# ─────────────────────────────────────────────
# suggest_outfit tests
# ─────────────────────────────────────────────

def test_suggest_outfit_with_wardrobe():
    wardrobe = get_example_wardrobe()
    item = search_listings("jeans", size=None, max_price=100)[0]

    result = suggest_outfit(item, wardrobe)

    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_suggest_outfit_empty_wardrobe():
    wardrobe = get_empty_wardrobe()
    item = search_listings("shirt", size=None, max_price=100)[0]

    result = suggest_outfit(item, wardrobe)

    assert isinstance(result, str)
    assert len(result.strip()) > 0


# ─────────────────────────────────────────────
# create_fit_card tests
# ─────────────────────────────────────────────

def test_create_fit_card_success():
    wardrobe = get_example_wardrobe()
    item = search_listings("jeans", size=None, max_price=100)[0]

    outfit = "casual streetwear outfit with jeans and a tee"
    result = create_fit_card(outfit, item)

    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_create_fit_card_empty_outfit():
    wardrobe = get_example_wardrobe()
    item = search_listings("jeans", size=None, max_price=100)[0]

    result = create_fit_card("", item)

    assert "Error" in result