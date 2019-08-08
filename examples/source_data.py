from datetime import date


baker_form = {
    "Zeb": {
        "pronouns": "they/them",
        "contact": {
            "phone": 6304206969,
            "email": "zeb@zeb.bakes",
            "insta_handle": "@zeb.bakes",
            "birthday": date(1999, 12, 19),
        },
        "specialties": ["miche", "rye"],
    },
    "Gary": {
        "pronouns": "he/him",
        "contact": {
            "phone": 6304206969,
            "email": "garyjones@gmail.com",
            "insta_handle": "@gar-bear",
            "birthday": date(1992, 4, 21),
        },
        "specialties": ["wonder"],
    },
    "Rosalia": {
        "pronouns": "she/her",
        "contact": {
            "phone": 6304206969,
            "email": "rosalia@bakezone.org",
            "insta_handle": "@rosybread",
            "birthday": date(2001, 1, 21),
        },
        "specialties": ["miche", "rye", "challah"],
    },
    "Guido": {
        "pronouns": "he/him",
        "contact": {
            "phone": 6304206969,
            "email": "gvr@snakebread.io",
            "insta_handle": "@snakebread",
            "birthday": date(1995, 8, 23),
        },
        "specialties": ["challah", "naan"],
    },
}

all_existing_breads = [
    {"name": "miche", "is_delicious": True, "ingredient_cost": 2.22},
    {"name": "rye", "is_delicious": True, "ingredient_cost": 1.46},
    {"name": "wonder", "is_delicious": False, "ingredient_cost": 0.60},
    {"name": "challah", "is_delicious": True, "ingredient_cost": 1.99},
    {"name": "naan", "is_delicious": True, "ingredient_cost": 0.42},
    {"name": "brioche", "is_delicious": True, "ingredient_cost": 2.03},
]
