"""
Task 2 — AI Travel Planner
============================
A knowledge-based reasoning engine that generates personalised tour plans,
food recommendations, wine pairings, and cost assessments.

The planner uses forward-chaining rule-based inference over the three
knowledge bases defined in knowledge_base.py.

Usage:
    python travel_planner.py
    — or run plan_trip() programmatically.
"""

from knowledge_base import (
    WINE_KB, PLACES_KB, FOOD_KB,
    get_places_by_type, get_places_for_season,
    get_food_by_dietary, get_wines_for_food,
)
from typing import List, Dict, Optional
import textwrap


# ---------------------------------------------------------------------------
# Cost Model  (USD per person per day)
# ---------------------------------------------------------------------------
BUDGET_COSTS = {
    "budget":  {"accommodation": 30,  "meals": 20,  "activities": 15, "transport": 10},
    "mid":     {"accommodation": 80,  "meals": 50,  "activities": 40, "transport": 25},
    "premium": {"accommodation": 200, "meals": 100, "activities": 80, "transport": 60},
    "luxury":  {"accommodation": 500, "meals": 200, "activities": 150, "transport": 100},
}

ACTIVITIES_PER_DAY = 2


# ---------------------------------------------------------------------------
# Reasoning Engine
# ---------------------------------------------------------------------------
class TravelPlanner:
    """
    Knowledge-based AI travel planner.

    Reasoning approach:
      - Forward chaining: user preferences → matching KB entities → itinerary
      - Constraint propagation: dietary restrictions filter food, season filters
        destinations, budget filters everything
    """

    def __init__(self):
        self.wines  = WINE_KB
        self.places = PLACES_KB
        self.foods  = FOOD_KB

    # ------------------------------------------------------------------ #
    # 1. Destination Matching (KB Inference)
    # ------------------------------------------------------------------ #
    def find_destinations(
        self,
        preferred_types: List[str],
        season: Optional[str],
        budget: Optional[str],
        max_results: int = 5,
    ) -> List[dict]:
        """
        Infer best destinations from preferences.

        Rules applied:
          R1: destination.type must overlap with preferred_types
          R2: if season is given, destination.best_season must include it
          R3: if budget is given, budget_level must match or be cheaper
        """
        budget_rank = {"budget": 0, "mid": 1, "premium": 2, "luxury": 3}

        results = []
        for place in self.places:
            # R1: type match
            type_score = len(set(place["type"]) & set(preferred_types))
            if type_score == 0:
                continue

            # R2: season match
            if season and season not in place["best_season"]:
                continue

            # R3: budget match (accept same or cheaper)
            if budget:
                if budget_rank.get(place["budget_level"], 99) > budget_rank.get(budget, 99):
                    continue

            results.append({"place": place, "score": type_score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

    # ------------------------------------------------------------------ #
    # 2. Food & Restaurant Recommendation
    # ------------------------------------------------------------------ #
    def recommend_food(
        self,
        cuisine_ids: List[str],
        dietary_restrictions: List[str],
    ) -> List[dict]:
        """
        Recommend cuisines and dishes matching dietary needs.

        Rule: cuisine must satisfy ALL dietary restrictions listed.
        """
        recs = []
        for cuisine in self.foods:
            if cuisine["id"] not in cuisine_ids:
                continue
            # Check dietary restrictions
            if dietary_restrictions:
                satisfies = all(d in cuisine["dietary_flags"] for d in dietary_restrictions)
                if not satisfies and dietary_restrictions:
                    # Partial match — flag it
                    satisfied_flags = [d for d in dietary_restrictions if d in cuisine["dietary_flags"]]
                    missing = [d for d in dietary_restrictions if d not in cuisine["dietary_flags"]]
                    recs.append({"cuisine": cuisine, "match": "partial",
                                 "satisfied": satisfied_flags, "missing": missing})
                    continue
            recs.append({"cuisine": cuisine, "match": "full", "satisfied": dietary_restrictions, "missing": []})
        return recs

    # ------------------------------------------------------------------ #
    # 3. Wine Pairing
    # ------------------------------------------------------------------ #
    def pair_wines(self, cuisine_ids: List[str], budget: Optional[str]) -> List[dict]:
        """
        Select wines that pair with the given cuisine, filtered by budget.
        """
        budget_rank = {"budget": 0, "mid": 1, "premium": 2, "luxury": 3}
        seen = set()
        wines = []
        for cid in cuisine_ids:
            for w in get_wines_for_food(cid):
                if w["id"] in seen:
                    continue
                seen.add(w["id"])
                if budget and budget_rank.get(w["price_range"], 99) > budget_rank.get(budget, 99):
                    continue
                wines.append(w)
        return wines[:4]

    # ------------------------------------------------------------------ #
    # 4. Cost Assessment
    # ------------------------------------------------------------------ #
    def estimate_cost(self, budget_level: str, duration_days: int, num_people: int) -> dict:
        """Estimate total trip cost per person and group."""
        costs = BUDGET_COSTS.get(budget_level, BUDGET_COSTS["mid"])
        daily_pp = sum(costs.values())
        total_pp = daily_pp * duration_days
        total    = total_pp * num_people
        return {
            "budget_level":   budget_level,
            "duration_days":  duration_days,
            "num_people":     num_people,
            "daily_per_person": daily_pp,
            "total_per_person": total_pp,
            "group_total":      total,
            "breakdown":        costs,
        }

    # ------------------------------------------------------------------ #
    # 5. Day-by-Day Itinerary Generation
    # ------------------------------------------------------------------ #
    def generate_itinerary(
        self,
        place: dict,
        duration_days: int,
        dietary_restrictions: List[str],
        budget: str,
    ) -> List[dict]:
        """
        Generate a day-by-day itinerary for the chosen destination.
        """
        activities = place["activities"]
        cuisine_ids = place["cuisine_types"]

        # Get food options
        food_recs = self.recommend_food(cuisine_ids, dietary_restrictions)
        cuisine = food_recs[0]["cuisine"] if food_recs else None

        # Get wine pairings
        wines = self.pair_wines(cuisine_ids, budget)

        itinerary = []
        act_idx = 0
        for day in range(1, duration_days + 1):
            day_activities = []
            for _ in range(ACTIVITIES_PER_DAY):
                day_activities.append(activities[act_idx % len(activities)])
                act_idx += 1

            evening_wine = wines[(day - 1) % len(wines)] if wines else None

            itinerary.append({
                "day":          day,
                "activities":   day_activities,
                "breakfast":    f"Local {place['name']} breakfast",
                "lunch":        cuisine["signature_dishes"][(day - 1) % len(cuisine["signature_dishes"])] if cuisine else "Local lunch",
                "dinner":       cuisine["signature_dishes"][(day) % len(cuisine["signature_dishes"])] if cuisine else "Local dinner",
                "wine_pairing": evening_wine["name"] if evening_wine else None,
                "restaurant":   cuisine["restaurant_types"][0] if cuisine else "Local restaurant",
            })

        return itinerary

    # ------------------------------------------------------------------ #
    # 6. Full Plan Generation
    # ------------------------------------------------------------------ #
    def plan_trip(
        self,
        preferred_types:      List[str],
        season:               str,
        duration_days:        int,
        budget_level:         str,
        num_people:           int,
        dietary_restrictions: List[str],
    ) -> dict:
        """
        Main entry point. Returns a complete personalised tour plan.
        """
        # Step 1: Find matching destinations
        matches = self.find_destinations(preferred_types, season, budget_level)
        if not matches:
            return {"error": "No destinations found for the given preferences."}

        top_place = matches[0]["place"]

        # Step 2: Recommend food
        food_recs = self.recommend_food(top_place["cuisine_types"], dietary_restrictions)

        # Step 3: Wine pairings
        wines = self.pair_wines(top_place["cuisine_types"], budget_level)

        # Step 4: Cost assessment
        costs = self.estimate_cost(budget_level, duration_days, num_people)

        # Step 5: Day-by-day itinerary
        itinerary = self.generate_itinerary(top_place, duration_days, dietary_restrictions, budget_level)

        return {
            "destination":           top_place,
            "alternative_destinations": [m["place"]["name"] for m in matches[1:]],
            "food_recommendations":  food_recs,
            "wine_pairings":         wines,
            "cost_assessment":       costs,
            "itinerary":             itinerary,
        }


# ---------------------------------------------------------------------------
# Pretty-Print Helpers
# ---------------------------------------------------------------------------
def print_plan(plan: dict):
    if "error" in plan:
        print(f"Error: {plan['error']}")
        return

    dest   = plan["destination"]
    costs  = plan["cost_assessment"]

    print("\n" + "=" * 70)
    print(f"  PERSONALISED TOUR PLAN")
    print("=" * 70)
    print(f"  Destination  : {dest['name']}, {dest['country']}")
    print(f"  Type         : {', '.join(dest['type'])}")
    print(f"  Language     : {dest['language']}")
    print(f"  Budget Level : {dest['budget_level']}")
    print(f"  Activities   : {', '.join(dest['activities'])}")
    print()

    alts = plan.get("alternative_destinations", [])
    if alts:
        print(f"  Alternative destinations: {', '.join(alts)}")
    print()

    print("  COST ASSESSMENT")
    print("  " + "-" * 40)
    print(f"  Duration       : {costs['duration_days']} days")
    print(f"  Travellers     : {costs['num_people']} person(s)")
    print(f"  Daily/person   : USD {costs['daily_per_person']}")
    print(f"  Total/person   : USD {costs['total_per_person']}")
    print(f"  GROUP TOTAL    : USD {costs['group_total']}")
    print(f"  Breakdown      : Accommodation ${costs['breakdown']['accommodation']}"
          f"  Meals ${costs['breakdown']['meals']}"
          f"  Activities ${costs['breakdown']['activities']}"
          f"  Transport ${costs['breakdown']['transport']} (per person/day)")
    print()

    print("  FOOD RECOMMENDATIONS")
    print("  " + "-" * 40)
    for fr in plan["food_recommendations"]:
        c = fr["cuisine"]
        flag = "Full match" if fr["match"] == "full" else f"Partial (missing: {', '.join(fr['missing'])})"
        print(f"  {c['name']} ({c['region']}) — {flag}")
        print(f"    Dishes  : {', '.join(c['signature_dishes'][:3])}")
        print(f"    Flavours: {', '.join(c['flavor_notes'])}")
        print(f"    Venue   : {c['restaurant_types'][0]}")
    print()

    print("  WINE PAIRINGS FOR DINNER")
    print("  " + "-" * 40)
    for w in plan["wine_pairings"]:
        print(f"  {w['name']} ({w['type']}, {w['country']}) — {w['price_range']}")
        print(f"    Pairings: {', '.join(w['food_pairings'][:3])}")
        print(f"    Serve at: {w['best_temp_c']}°C")
    print()

    print("  DAY-BY-DAY ITINERARY")
    print("  " + "-" * 40)
    for day in plan["itinerary"]:
        print(f"  Day {day['day']}:")
        print(f"    Activities : {', '.join(day['activities'])}")
        print(f"    Breakfast  : {day['breakfast']}")
        print(f"    Lunch      : {day['lunch']}")
        print(f"    Dinner     : {day['dinner']} at {day['restaurant']}")
        if day["wine_pairing"]:
            print(f"    Wine       : {day['wine_pairing']}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------
def interactive_planner():
    planner = TravelPlanner()

    print("\n" + "=" * 60)
    print("  AI TRAVEL PLANNER — Interactive Mode")
    print("=" * 60)

    print("\nDestination types: beach, mountain, city, cultural, adventure, nature")
    raw_types = input("Preferred types (comma-separated, e.g. beach,cultural): ").strip()
    preferred_types = [t.strip() for t in raw_types.split(",") if t.strip()]

    print("Season: spring | summer | autumn | winter")
    season = input("Travel season (leave blank to skip): ").strip().lower() or None

    duration = int(input("Duration in days (e.g. 5): ").strip() or 5)

    print("Budget: budget | mid | premium | luxury")
    budget = input("Budget level (default: mid): ").strip().lower() or "mid"

    num_people = int(input("Number of travellers (default: 2): ").strip() or 2)

    print("Dietary options: vegetarian, vegan, halal, gluten-free, pescatarian")
    raw_diet = input("Dietary restrictions (comma-separated, leave blank for none): ").strip()
    dietary = [d.strip() for d in raw_diet.split(",") if d.strip()]

    plan = planner.plan_trip(
        preferred_types      = preferred_types or ["city", "cultural"],
        season               = season,
        duration_days        = duration,
        budget_level         = budget,
        num_people           = num_people,
        dietary_restrictions = dietary,
    )

    print_plan(plan)


def run_example_plans():
    planner = TravelPlanner()

    examples = [
        {
            "label":              "Beach + cultural trip, summer, mid budget, vegetarian",
            "preferred_types":    ["beach", "cultural"],
            "season":             "summer",
            "duration_days":      7,
            "budget_level":       "mid",
            "num_people":         2,
            "dietary_restrictions": ["vegetarian"],
        },
        {
            "label":              "Adventure + mountain, winter, premium budget",
            "preferred_types":    ["adventure", "mountain"],
            "season":             "winter",
            "duration_days":      5,
            "budget_level":       "premium",
            "num_people":         1,
            "dietary_restrictions": [],
        },
        {
            "label":              "City + nature, any season, budget traveller, vegan + halal",
            "preferred_types":    ["city", "nature"],
            "season":             None,
            "duration_days":      4,
            "budget_level":       "budget",
            "num_people":         3,
            "dietary_restrictions": ["vegan", "halal"],
        },
    ]

    for ex in examples:
        print(f"\n>>> Plan: {ex['label']}")
        plan = planner.plan_trip(
            preferred_types      = ex["preferred_types"],
            season               = ex["season"],
            duration_days        = ex["duration_days"],
            budget_level         = ex["budget_level"],
            num_people           = ex["num_people"],
            dietary_restrictions = ex["dietary_restrictions"],
        )
        print_plan(plan)


if __name__ == "__main__":
    print("Running example plans...\n")
    run_example_plans()

    print("\n\nWould you like to create a custom plan? (y/n): ", end="")
    ans = input().strip().lower()
    if ans == "y":
        interactive_planner()
