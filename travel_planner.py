"""
Task 2 — Knowledge Bases for the AI Travel Planner
====================================================
Three domain knowledge bases are defined here as structured Python
dictionaries and lists that the travel-planner reasoning engine can query.

  1. Wine Ontology KB   — wine varieties with tasting profiles, pairings, regions
  2. Tourist Places KB  — destinations with activities, seasons, budgets
  3. Food & Cuisine KB  — cuisines with dishes, dietary flags, wine pairings
"""

from typing import TypedDict, List


# ---------------------------------------------------------------------------
# 1. Wine Ontology Knowledge Base
# ---------------------------------------------------------------------------
class Wine(TypedDict):
    id:             str
    name:           str
    type:           str          # red | white | rosé | sparkling | dessert
    region:         str
    country:        str
    grape:          List[str]
    flavor_profile: List[str]    # fruity | earthy | tannic | crisp | floral | rich | spicy
    food_pairings:  List[str]    # e.g. "seafood", "pasta", "grilled meat"
    price_range:    str          # budget | mid | premium | luxury
    best_temp_c:    int          # serving temperature in °C


WINE_KB: List[Wine] = [
    {
        "id": "W01", "name": "Barossa Valley Shiraz", "type": "red",
        "region": "Barossa Valley", "country": "Australia",
        "grape": ["Shiraz"],
        "flavor_profile": ["rich", "spicy", "fruity", "tannic"],
        "food_pairings": ["grilled meat", "barbecue", "lamb", "aged cheese"],
        "price_range": "mid", "best_temp_c": 17,
    },
    {
        "id": "W02", "name": "Marlborough Sauvignon Blanc", "type": "white",
        "region": "Marlborough", "country": "New Zealand",
        "grape": ["Sauvignon Blanc"],
        "flavor_profile": ["crisp", "fruity", "floral"],
        "food_pairings": ["seafood", "salads", "goat cheese", "sushi"],
        "price_range": "mid", "best_temp_c": 8,
    },
    {
        "id": "W03", "name": "Burgundy Pinot Noir", "type": "red",
        "region": "Burgundy", "country": "France",
        "grape": ["Pinot Noir"],
        "flavor_profile": ["earthy", "fruity", "light", "tannic"],
        "food_pairings": ["duck", "salmon", "mushroom dishes", "soft cheese"],
        "price_range": "premium", "best_temp_c": 16,
    },
    {
        "id": "W04", "name": "Prosecco DOC", "type": "sparkling",
        "region": "Veneto", "country": "Italy",
        "grape": ["Glera"],
        "flavor_profile": ["fruity", "floral", "crisp"],
        "food_pairings": ["appetisers", "seafood", "light pasta", "fruit desserts"],
        "price_range": "budget", "best_temp_c": 6,
    },
    {
        "id": "W05", "name": "Napa Valley Cabernet Sauvignon", "type": "red",
        "region": "Napa Valley", "country": "USA",
        "grape": ["Cabernet Sauvignon"],
        "flavor_profile": ["rich", "tannic", "spicy", "earthy"],
        "food_pairings": ["steak", "lamb", "hard cheese", "dark chocolate"],
        "price_range": "premium", "best_temp_c": 18,
    },
    {
        "id": "W06", "name": "Rioja Tempranillo", "type": "red",
        "region": "Rioja", "country": "Spain",
        "grape": ["Tempranillo"],
        "flavor_profile": ["fruity", "earthy", "spicy"],
        "food_pairings": ["tapas", "paella", "grilled meat", "chorizo"],
        "price_range": "mid", "best_temp_c": 16,
    },
    {
        "id": "W07", "name": "Alsace Riesling", "type": "white",
        "region": "Alsace", "country": "France",
        "grape": ["Riesling"],
        "flavor_profile": ["crisp", "fruity", "floral", "mineral"],
        "food_pairings": ["Asian cuisine", "seafood", "pork", "spicy food"],
        "price_range": "mid", "best_temp_c": 9,
    },
    {
        "id": "W08", "name": "Champagne Brut", "type": "sparkling",
        "region": "Champagne", "country": "France",
        "grape": ["Chardonnay", "Pinot Noir", "Meunier"],
        "flavor_profile": ["crisp", "rich", "fruity"],
        "food_pairings": ["oysters", "caviar", "fried appetisers", "light cheese"],
        "price_range": "luxury", "best_temp_c": 7,
    },
    {
        "id": "W09", "name": "Tuscany Sangiovese (Chianti)", "type": "red",
        "region": "Tuscany", "country": "Italy",
        "grape": ["Sangiovese"],
        "flavor_profile": ["tannic", "earthy", "fruity"],
        "food_pairings": ["pizza", "pasta with tomato", "grilled meat", "Italian cuisine"],
        "price_range": "mid", "best_temp_c": 17,
    },
    {
        "id": "W10", "name": "Mosel Spätlese Riesling", "type": "dessert",
        "region": "Mosel", "country": "Germany",
        "grape": ["Riesling"],
        "flavor_profile": ["sweet", "fruity", "floral"],
        "food_pairings": ["desserts", "blue cheese", "foie gras", "fruit tart"],
        "price_range": "premium", "best_temp_c": 8,
    },
    {
        "id": "W11", "name": "Mendoza Malbec", "type": "red",
        "region": "Mendoza", "country": "Argentina",
        "grape": ["Malbec"],
        "flavor_profile": ["rich", "fruity", "tannic"],
        "food_pairings": ["steak", "empanadas", "grilled meat", "aged cheese"],
        "price_range": "budget", "best_temp_c": 17,
    },
    {
        "id": "W12", "name": "Provence Rosé", "type": "rosé",
        "region": "Provence", "country": "France",
        "grape": ["Grenache", "Cinsault"],
        "flavor_profile": ["fruity", "floral", "crisp"],
        "food_pairings": ["seafood", "salads", "light Mediterranean", "grilled fish"],
        "price_range": "mid", "best_temp_c": 10,
    },
    {
        "id": "W13", "name": "Douro Valley Port", "type": "dessert",
        "region": "Douro Valley", "country": "Portugal",
        "grape": ["Touriga Nacional", "Touriga Franca"],
        "flavor_profile": ["sweet", "rich", "spicy"],
        "food_pairings": ["dark chocolate", "blue cheese", "walnuts", "desserts"],
        "price_range": "mid", "best_temp_c": 14,
    },
    {
        "id": "W14", "name": "Chablis Premier Cru", "type": "white",
        "region": "Chablis", "country": "France",
        "grape": ["Chardonnay"],
        "flavor_profile": ["crisp", "mineral", "light"],
        "food_pairings": ["oysters", "seafood", "sushi", "mild cheese"],
        "price_range": "premium", "best_temp_c": 10,
    },
    {
        "id": "W15", "name": "Stellenbosch Chenin Blanc", "type": "white",
        "region": "Stellenbosch", "country": "South Africa",
        "grape": ["Chenin Blanc"],
        "flavor_profile": ["fruity", "crisp", "floral"],
        "food_pairings": ["Cape Malay cuisine", "seafood", "poultry", "spicy dishes"],
        "price_range": "budget", "best_temp_c": 9,
    },
]


# ---------------------------------------------------------------------------
# 2. Tourist Places Knowledge Base
# ---------------------------------------------------------------------------
class Place(TypedDict):
    id:            str
    name:          str
    country:       str
    continent:     str
    type:          List[str]    # beach | mountain | city | cultural | adventure | nature
    best_season:   List[str]   # spring | summer | autumn | winter
    activities:    List[str]
    cuisine_types: List[str]   # references Food KB cuisine IDs
    budget_level:  str          # budget | mid | premium | luxury
    avg_temp_c:    dict          # {"summer": int, "winter": int}
    language:      str


PLACES_KB: List[Place] = [
    {
        "id": "P01", "name": "Bali", "country": "Indonesia", "continent": "Asia",
        "type": ["beach", "cultural", "nature"],
        "best_season": ["spring", "summer"],
        "activities": ["surfing", "temple visits", "rice terrace trekking", "diving", "cooking class"],
        "cuisine_types": ["F05"],
        "budget_level": "budget", "avg_temp_c": {"summer": 30, "winter": 28},
        "language": "Indonesian",
    },
    {
        "id": "P02", "name": "Paris", "country": "France", "continent": "Europe",
        "type": ["city", "cultural"],
        "best_season": ["spring", "autumn"],
        "activities": ["museum visits", "fine dining", "Seine river cruise", "wine tasting", "shopping"],
        "cuisine_types": ["F01"],
        "budget_level": "premium", "avg_temp_c": {"summer": 24, "winter": 5},
        "language": "French",
    },
    {
        "id": "P03", "name": "Patagonia", "country": "Argentina/Chile", "continent": "South America",
        "type": ["mountain", "adventure", "nature"],
        "best_season": ["summer", "autumn"],
        "activities": ["trekking", "glacier hiking", "kayaking", "wildlife watching", "rock climbing"],
        "cuisine_types": ["F08"],
        "budget_level": "mid", "avg_temp_c": {"summer": 18, "winter": 2},
        "language": "Spanish",
    },
    {
        "id": "P04", "name": "Kyoto", "country": "Japan", "continent": "Asia",
        "type": ["cultural", "city", "nature"],
        "best_season": ["spring", "autumn"],
        "activities": ["temple visits", "tea ceremony", "geisha district", "bamboo forest", "onsen"],
        "cuisine_types": ["F06"],
        "budget_level": "premium", "avg_temp_c": {"summer": 33, "winter": 6},
        "language": "Japanese",
    },
    {
        "id": "P05", "name": "Santorini", "country": "Greece", "continent": "Europe",
        "type": ["beach", "cultural"],
        "best_season": ["spring", "summer"],
        "activities": ["caldera views", "wine tasting", "sailing", "beach lounging", "village exploration"],
        "cuisine_types": ["F02"],
        "budget_level": "premium", "avg_temp_c": {"summer": 30, "winter": 12},
        "language": "Greek",
    },
    {
        "id": "P06", "name": "Cape Town", "country": "South Africa", "continent": "Africa",
        "type": ["city", "beach", "nature", "adventure"],
        "best_season": ["spring", "summer"],
        "activities": ["Table Mountain hiking", "wine route", "shark cage diving", "Cape Point", "V&A Waterfront"],
        "cuisine_types": ["F09"],
        "budget_level": "mid", "avg_temp_c": {"summer": 26, "winter": 14},
        "language": "English",
    },
    {
        "id": "P07", "name": "Machu Picchu", "country": "Peru", "continent": "South America",
        "type": ["cultural", "adventure", "mountain"],
        "best_season": ["spring", "summer"],
        "activities": ["Inca Trail trekking", "archaeological tours", "llama spotting", "Aguas Calientes", "Sun Gate"],
        "cuisine_types": ["F10"],
        "budget_level": "mid", "avg_temp_c": {"summer": 20, "winter": 12},
        "language": "Spanish",
    },
    {
        "id": "P08", "name": "Rome", "country": "Italy", "continent": "Europe",
        "type": ["city", "cultural"],
        "best_season": ["spring", "autumn"],
        "activities": ["Colosseum visit", "Vatican tour", "gelato", "piazza hopping", "cooking class"],
        "cuisine_types": ["F03"],
        "budget_level": "mid", "avg_temp_c": {"summer": 30, "winter": 8},
        "language": "Italian",
    },
    {
        "id": "P09", "name": "Maldives", "country": "Maldives", "continent": "Asia",
        "type": ["beach", "nature"],
        "best_season": ["winter", "spring"],
        "activities": ["snorkelling", "diving", "overwater bungalow", "whale shark tours", "sunset cruise"],
        "cuisine_types": ["F05"],
        "budget_level": "luxury", "avg_temp_c": {"summer": 30, "winter": 28},
        "language": "Dhivehi",
    },
    {
        "id": "P10", "name": "Queenstown", "country": "New Zealand", "continent": "Oceania",
        "type": ["adventure", "mountain", "nature"],
        "best_season": ["summer", "winter"],
        "activities": ["bungee jumping", "skydiving", "skiing", "jet boating", "wine trail"],
        "cuisine_types": ["F11"],
        "budget_level": "premium", "avg_temp_c": {"summer": 22, "winter": 5},
        "language": "English",
    },
    {
        "id": "P11", "name": "Marrakech", "country": "Morocco", "continent": "Africa",
        "type": ["cultural", "city"],
        "best_season": ["spring", "autumn"],
        "activities": ["medina souk", "Majorelle garden", "hammam", "desert excursion", "cooking class"],
        "cuisine_types": ["F12"],
        "budget_level": "budget", "avg_temp_c": {"summer": 38, "winter": 12},
        "language": "Arabic",
    },
    {
        "id": "P12", "name": "Reykjavik", "country": "Iceland", "continent": "Europe",
        "type": ["nature", "adventure", "cultural"],
        "best_season": ["summer", "winter"],
        "activities": ["Northern Lights", "geysers", "glaciers", "whale watching", "hot springs"],
        "cuisine_types": ["F13"],
        "budget_level": "premium", "avg_temp_c": {"summer": 12, "winter": 1},
        "language": "Icelandic",
    },
    {
        "id": "P13", "name": "Bangkok", "country": "Thailand", "continent": "Asia",
        "type": ["city", "cultural"],
        "best_season": ["winter", "spring"],
        "activities": ["temple tours", "street food", "floating markets", "Muay Thai", "tuk-tuk rides"],
        "cuisine_types": ["F04"],
        "budget_level": "budget", "avg_temp_c": {"summer": 35, "winter": 28},
        "language": "Thai",
    },
    {
        "id": "P14", "name": "Swiss Alps", "country": "Switzerland", "continent": "Europe",
        "type": ["mountain", "adventure"],
        "best_season": ["winter", "summer"],
        "activities": ["skiing", "snowboarding", "hiking", "paragliding", "cheese tasting"],
        "cuisine_types": ["F07"],
        "budget_level": "luxury", "avg_temp_c": {"summer": 15, "winter": -5},
        "language": "German/French/Italian",
    },
    {
        "id": "P15", "name": "Amalfi Coast", "country": "Italy", "continent": "Europe",
        "type": ["beach", "cultural"],
        "best_season": ["spring", "summer"],
        "activities": ["coastal drive", "lemon groves", "boat trips", "hiking", "seafood dining"],
        "cuisine_types": ["F03"],
        "budget_level": "premium", "avg_temp_c": {"summer": 28, "winter": 12},
        "language": "Italian",
    },
]


# ---------------------------------------------------------------------------
# 3. Food & Cuisine Knowledge Base
# ---------------------------------------------------------------------------
class Cuisine(TypedDict):
    id:                str
    name:              str
    region:            str
    signature_dishes:  List[str]
    dietary_flags:     List[str]  # vegetarian | vegan | halal | gluten-free | pescatarian
    flavor_notes:      List[str]  # spicy | mild | umami | sweet | sour | rich | fresh
    wine_pairing_ids:  List[str]  # references Wine KB IDs
    restaurant_types:  List[str]


FOOD_KB: List[Cuisine] = [
    {
        "id": "F01", "name": "French Cuisine", "region": "France",
        "signature_dishes": ["Coq au Vin", "Bouillabaisse", "Ratatouille", "Crêpes Suzette", "Croque Monsieur"],
        "dietary_flags": ["vegetarian"],
        "flavor_notes": ["rich", "mild", "sweet"],
        "wine_pairing_ids": ["W03", "W08", "W14"],
        "restaurant_types": ["bistro", "brasserie", "fine dining", "patisserie"],
    },
    {
        "id": "F02", "name": "Greek & Mediterranean", "region": "Greece/Mediterranean",
        "signature_dishes": ["Moussaka", "Souvlaki", "Greek Salad", "Spanakopita", "Baklava"],
        "dietary_flags": ["vegetarian", "gluten-free", "pescatarian"],
        "flavor_notes": ["fresh", "mild", "rich"],
        "wine_pairing_ids": ["W12", "W04"],
        "restaurant_types": ["taverna", "seaside restaurant", "mezze bar"],
    },
    {
        "id": "F03", "name": "Italian Cuisine", "region": "Italy",
        "signature_dishes": ["Pizza Napoletana", "Risotto ai Funghi", "Carbonara", "Tiramisu", "Panzanella"],
        "dietary_flags": ["vegetarian"],
        "flavor_notes": ["rich", "umami", "mild"],
        "wine_pairing_ids": ["W09", "W04", "W03"],
        "restaurant_types": ["trattoria", "osteria", "pizzeria", "ristorante"],
    },
    {
        "id": "F04", "name": "Thai Cuisine", "region": "Thailand",
        "signature_dishes": ["Pad Thai", "Green Curry", "Tom Yum", "Som Tam", "Mango Sticky Rice"],
        "dietary_flags": ["vegan", "vegetarian", "gluten-free"],
        "flavor_notes": ["spicy", "sweet", "sour", "umami"],
        "wine_pairing_ids": ["W07", "W02"],
        "restaurant_types": ["street food", "noodle house", "rooftop restaurant"],
    },
    {
        "id": "F05", "name": "Balinese & Indonesian", "region": "Indonesia",
        "signature_dishes": ["Nasi Goreng", "Babi Guling", "Sate", "Gado Gado", "Lawar"],
        "dietary_flags": ["vegan", "gluten-free"],
        "flavor_notes": ["spicy", "sweet", "umami"],
        "wine_pairing_ids": ["W11", "W07"],
        "restaurant_types": ["warung", "beach restaurant", "eco lodge"],
    },
    {
        "id": "F06", "name": "Japanese Cuisine", "region": "Japan",
        "signature_dishes": ["Kaiseki", "Ramen", "Sushi", "Tempura", "Wagyu Beef"],
        "dietary_flags": ["gluten-free", "pescatarian"],
        "flavor_notes": ["umami", "mild", "fresh"],
        "wine_pairing_ids": ["W02", "W14", "W07"],
        "restaurant_types": ["izakaya", "ramen-ya", "sushi bar", "kaiseki restaurant"],
    },
    {
        "id": "F07", "name": "Swiss & Alpine", "region": "Switzerland/Alps",
        "signature_dishes": ["Fondue", "Raclette", "Rösti", "Zürcher Geschnetzeltes", "Birchermüesli"],
        "dietary_flags": ["vegetarian"],
        "flavor_notes": ["rich", "mild"],
        "wine_pairing_ids": ["W03", "W14"],
        "restaurant_types": ["mountain hut", "chalet restaurant", "fondue specialist"],
    },
    {
        "id": "F08", "name": "Argentine & South American", "region": "Argentina/Chile",
        "signature_dishes": ["Asado", "Empanadas", "Chimichurri Steak", "Locro", "Dulce de Leche"],
        "dietary_flags": [],
        "flavor_notes": ["rich", "mild", "spicy"],
        "wine_pairing_ids": ["W11", "W05"],
        "restaurant_types": ["parrilla", "steakhouse", "bodega restaurant"],
    },
    {
        "id": "F09", "name": "Cape Malay & South African", "region": "South Africa",
        "signature_dishes": ["Bobotie", "Braai", "Bunny Chow", "Malva Pudding", "Boerewors"],
        "dietary_flags": ["halal"],
        "flavor_notes": ["spicy", "sweet", "rich"],
        "wine_pairing_ids": ["W15", "W01"],
        "restaurant_types": ["braai house", "Cape Malay restaurant", "winery restaurant"],
    },
    {
        "id": "F10", "name": "Peruvian Cuisine", "region": "Peru",
        "signature_dishes": ["Ceviche", "Lomo Saltado", "Causa Rellena", "Anticuchos", "Picarones"],
        "dietary_flags": ["gluten-free", "pescatarian"],
        "flavor_notes": ["sour", "fresh", "spicy", "umami"],
        "wine_pairing_ids": ["W02", "W12"],
        "restaurant_types": ["cevichería", "chifa", "high-altitude gourmet"],
    },
    {
        "id": "F11", "name": "New Zealand Fusion", "region": "New Zealand",
        "signature_dishes": ["Lamb Rack", "Pavlova", "Hangi", "Green-lipped Mussels", "Venison"],
        "dietary_flags": ["gluten-free"],
        "flavor_notes": ["fresh", "mild", "rich"],
        "wine_pairing_ids": ["W02", "W03"],
        "restaurant_types": ["vineyard restaurant", "café", "farm-to-table"],
    },
    {
        "id": "F12", "name": "Moroccan Cuisine", "region": "Morocco/North Africa",
        "signature_dishes": ["Tagine", "Couscous", "Bastilla", "Harira", "Mint Tea & Pastries"],
        "dietary_flags": ["vegan", "vegetarian", "halal"],
        "flavor_notes": ["spicy", "sweet", "rich"],
        "wine_pairing_ids": ["W06", "W13"],
        "restaurant_types": ["riad restaurant", "souk café", "rooftop terrace"],
    },
    {
        "id": "F13", "name": "Nordic / Icelandic", "region": "Iceland/Scandinavia",
        "signature_dishes": ["Skyr", "Plokkfiskur", "Lamb Soup", "Arctic Char", "Kleinur"],
        "dietary_flags": ["gluten-free", "pescatarian"],
        "flavor_notes": ["mild", "fresh", "umami"],
        "wine_pairing_ids": ["W14", "W07"],
        "restaurant_types": ["farm restaurant", "fish market café", "Northern Lights dinner"],
    },
]


# ---------------------------------------------------------------------------
# Helper Query Functions
# ---------------------------------------------------------------------------
def get_wine_by_type(wine_type: str) -> List[Wine]:
    return [w for w in WINE_KB if w["type"] == wine_type]


def get_places_by_type(place_type: str) -> List[Place]:
    return [p for p in PLACES_KB if place_type in p["type"]]


def get_food_by_dietary(flag: str) -> List[Cuisine]:
    return [f for f in FOOD_KB if flag in f["dietary_flags"]]


def get_wines_for_food(cuisine_id: str) -> List[Wine]:
    cuisine = next((f for f in FOOD_KB if f["id"] == cuisine_id), None)
    if not cuisine:
        return []
    return [w for w in WINE_KB if w["id"] in cuisine["wine_pairing_ids"]]


def get_places_for_season(season: str) -> List[Place]:
    return [p for p in PLACES_KB if season in p["best_season"]]


if __name__ == "__main__":
    print("=== Wine KB Sample ===")
    for w in WINE_KB[:3]:
        print(f"  {w['id']} {w['name']} ({w['type']}, {w['country']}) — {', '.join(w['flavor_profile'])}")

    print("\n=== Beach destinations ===")
    for p in get_places_by_type("beach"):
        print(f"  {p['id']} {p['name']} ({p['country']}) — budget: {p['budget_level']}")

    print("\n=== Vegan-friendly cuisines ===")
    for f in get_food_by_dietary("vegan"):
        print(f"  {f['id']} {f['name']}")

    print("\n=== Wines pairing with Italian cuisine ===")
    for w in get_wines_for_food("F03"):
        print(f"  {w['name']} ({w['type']})")
