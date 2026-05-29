{
  "nodes": [
    {
      "id": "france",
      "label": "Country",
      "name": "France",
      "continent": "Europe"
    },
    {
      "id": "italy",
      "label": "Country",
      "name": "Italy",
      "continent": "Europe"
    },
    {
      "id": "japan",
      "label": "Country",
      "name": "Japan",
      "continent": "Asia"
    },
    {
      "id": "indonesia",
      "label": "Country",
      "name": "Indonesia",
      "continent": "Asia"
    },
    {
      "id": "argentina",
      "label": "Country",
      "name": "Argentina",
      "continent": "South America"
    },
    {
      "id": "greece",
      "label": "Country",
      "name": "Greece",
      "continent": "Europe"
    },
    {
      "id": "nz",
      "label": "Country",
      "name": "New Zealand",
      "continent": "Oceania"
    },
    {
      "id": "paris",
      "label": "City",
      "name": "Paris",
      "type": "city"
    },
    {
      "id": "kyoto",
      "label": "City",
      "name": "Kyoto",
      "type": "cultural"
    },
    {
      "id": "rome",
      "label": "City",
      "name": "Rome",
      "type": "city"
    },
    {
      "id": "bali",
      "label": "City",
      "name": "Bali",
      "type": "beach"
    },
    {
      "id": "santorini",
      "label": "City",
      "name": "Santorini",
      "type": "beach"
    },
    {
      "id": "mendoza",
      "label": "City",
      "name": "Mendoza",
      "type": "wine region"
    },
    {
      "id": "queenstown",
      "label": "City",
      "name": "Queenstown",
      "type": "adventure"
    },
    {
      "id": "florence",
      "label": "City",
      "name": "Florence",
      "type": "cultural"
    },
    {
      "id": "tuscany",
      "label": "City",
      "name": "Tuscany",
      "type": "wine region"
    },
    {
      "id": "burgundy",
      "label": "City",
      "name": "Burgundy",
      "type": "wine region"
    },
    {
      "id": "french_cuisine",
      "label": "Cuisine",
      "name": "French Cuisine"
    },
    {
      "id": "italian_cuisine",
      "label": "Cuisine",
      "name": "Italian Cuisine"
    },
    {
      "id": "japanese_cuisine",
      "label": "Cuisine",
      "name": "Japanese Cuisine"
    },
    {
      "id": "balinese_cuisine",
      "label": "Cuisine",
      "name": "Balinese Cuisine"
    },
    {
      "id": "greek_cuisine",
      "label": "Cuisine",
      "name": "Greek Cuisine"
    },
    {
      "id": "champagne_brut",
      "label": "Wine",
      "name": "Champagne Brut",
      "type": "sparkling"
    },
    {
      "id": "burgundy_pn",
      "label": "Wine",
      "name": "Burgundy Pinot Noir",
      "type": "red"
    },
    {
      "id": "chablis",
      "label": "Wine",
      "name": "Chablis Premier Cru",
      "type": "white"
    },
    {
      "id": "chianti",
      "label": "Wine",
      "name": "Chianti Classico",
      "type": "red"
    },
    {
      "id": "prosecco",
      "label": "Wine",
      "name": "Prosecco DOC",
      "type": "sparkling"
    },
    {
      "id": "mendoza_malbec",
      "label": "Wine",
      "name": "Mendoza Malbec",
      "type": "red"
    },
    {
      "id": "marlborough_sb",
      "label": "Wine",
      "name": "Marlborough Sauvignon Blanc",
      "type": "white"
    },
    {
      "id": "rioja",
      "label": "Wine",
      "name": "Rioja Tempranillo",
      "type": "red"
    },
    {
      "id": "wine_tasting",
      "label": "Activity",
      "name": "Wine Tasting",
      "type": "food_drink"
    },
    {
      "id": "cooking_class",
      "label": "Activity",
      "name": "Cooking Class",
      "type": "food_drink"
    },
    {
      "id": "museum_visit",
      "label": "Activity",
      "name": "Museum Visit",
      "type": "cultural"
    },
    {
      "id": "temple_visit",
      "label": "Activity",
      "name": "Temple Visit",
      "type": "cultural"
    },
    {
      "id": "beach_relax",
      "label": "Activity",
      "name": "Beach Relaxation",
      "type": "leisure"
    },
    {
      "id": "surfing",
      "label": "Activity",
      "name": "Surfing",
      "type": "adventure"
    },
    {
      "id": "hiking",
      "label": "Activity",
      "name": "Hiking",
      "type": "adventure"
    },
    {
      "id": "bungee_jumping",
      "label": "Activity",
      "name": "Bungee Jumping",
      "type": "adventure"
    },
    {
      "id": "fine_dining",
      "label": "Activity",
      "name": "Fine Dining",
      "type": "food_drink"
    },
    {
      "id": "snorkelling",
      "label": "Activity",
      "name": "Snorkelling",
      "type": "adventure"
    }
  ],
  "edges": [
    {
      "from": "paris",
      "relation": "locatedIn",
      "to": "france"
    },
    {
      "from": "kyoto",
      "relation": "locatedIn",
      "to": "japan"
    },
    {
      "from": "rome",
      "relation": "locatedIn",
      "to": "italy"
    },
    {
      "from": "bali",
      "relation": "locatedIn",
      "to": "indonesia"
    },
    {
      "from": "santorini",
      "relation": "locatedIn",
      "to": "greece"
    },
    {
      "from": "mendoza",
      "relation": "locatedIn",
      "to": "argentina"
    },
    {
      "from": "queenstown",
      "relation": "locatedIn",
      "to": "nz"
    },
    {
      "from": "florence",
      "relation": "locatedIn",
      "to": "italy"
    },
    {
      "from": "tuscany",
      "relation": "locatedIn",
      "to": "italy"
    },
    {
      "from": "burgundy",
      "relation": "locatedIn",
      "to": "france"
    },
    {
      "from": "paris",
      "relation": "hasCuisine",
      "to": "french_cuisine"
    },
    {
      "from": "rome",
      "relation": "hasCuisine",
      "to": "italian_cuisine"
    },
    {
      "from": "florence",
      "relation": "hasCuisine",
      "to": "italian_cuisine"
    },
    {
      "from": "kyoto",
      "relation": "hasCuisine",
      "to": "japanese_cuisine"
    },
    {
      "from": "bali",
      "relation": "hasCuisine",
      "to": "balinese_cuisine"
    },
    {
      "from": "santorini",
      "relation": "hasCuisine",
      "to": "greek_cuisine"
    },
    {
      "from": "champagne_brut",
      "relation": "producedIn",
      "to": "burgundy"
    },
    {
      "from": "burgundy",
      "relation": "produces",
      "to": "champagne_brut"
    },
    {
      "from": "burgundy_pn",
      "relation": "producedIn",
      "to": "burgundy"
    },
    {
      "from": "burgundy",
      "relation": "produces",
      "to": "burgundy_pn"
    },
    {
      "from": "chablis",
      "relation": "producedIn",
      "to": "burgundy"
    },
    {
      "from": "burgundy",
      "relation": "produces",
      "to": "chablis"
    },
    {
      "from": "chianti",
      "relation": "producedIn",
      "to": "tuscany"
    },
    {
      "from": "tuscany",
      "relation": "produces",
      "to": "chianti"
    },
    {
      "from": "prosecco",
      "relation": "producedIn",
      "to": "rome"
    },
    {
      "from": "rome",
      "relation": "produces",
      "to": "prosecco"
    },
    {
      "from": "mendoza_malbec",
      "relation": "producedIn",
      "to": "mendoza"
    },
    {
      "from": "mendoza",
      "relation": "produces",
      "to": "mendoza_malbec"
    },
    {
      "from": "marlborough_sb",
      "relation": "producedIn",
      "to": "queenstown"
    },
    {
      "from": "queenstown",
      "relation": "produces",
      "to": "marlborough_sb"
    },
    {
      "from": "rioja",
      "relation": "producedIn",
      "to": "paris"
    },
    {
      "from": "paris",
      "relation": "produces",
      "to": "rioja"
    },
    {
      "from": "champagne_brut",
      "relation": "pairsWith",
      "to": "french_cuisine"
    },
    {
      "from": "burgundy_pn",
      "relation": "pairsWith",
      "to": "french_cuisine"
    },
    {
      "from": "chablis",
      "relation": "pairsWith",
      "to": "french_cuisine"
    },
    {
      "from": "chablis",
      "relation": "pairsWith",
      "to": "japanese_cuisine"
    },
    {
      "from": "chianti",
      "relation": "pairsWith",
      "to": "italian_cuisine"
    },
    {
      "from": "prosecco",
      "relation": "pairsWith",
      "to": "italian_cuisine"
    },
    {
      "from": "mendoza_malbec",
      "relation": "pairsWith",
      "to": "balinese_cuisine"
    },
    {
      "from": "marlborough_sb",
      "relation": "pairsWith",
      "to": "japanese_cuisine"
    },
    {
      "from": "paris",
      "relation": "offers",
      "to": "wine_tasting"
    },
    {
      "from": "paris",
      "relation": "offers",
      "to": "museum_visit"
    },
    {
      "from": "paris",
      "relation": "offers",
      "to": "fine_dining"
    },
    {
      "from": "kyoto",
      "relation": "offers",
      "to": "temple_visit"
    },
    {
      "from": "kyoto",
      "relation": "offers",
      "to": "cooking_class"
    },
    {
      "from": "bali",
      "relation": "offers",
      "to": "surfing"
    },
    {
      "from": "bali",
      "relation": "offers",
      "to": "beach_relax"
    },
    {
      "from": "bali",
      "relation": "offers",
      "to": "cooking_class"
    },
    {
      "from": "santorini",
      "relation": "offers",
      "to": "beach_relax"
    },
    {
      "from": "santorini",
      "relation": "offers",
      "to": "wine_tasting"
    },
    {
      "from": "queenstown",
      "relation": "offers",
      "to": "bungee_jumping"
    },
    {
      "from": "queenstown",
      "relation": "offers",
      "to": "hiking"
    },
    {
      "from": "tuscany",
      "relation": "offers",
      "to": "wine_tasting"
    },
    {
      "from": "tuscany",
      "relation": "offers",
      "to": "cooking_class"
    },
    {
      "from": "mendoza",
      "relation": "offers",
      "to": "wine_tasting"
    }
  ]
}