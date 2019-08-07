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
    ("miche", True, 2.22),
    ("rye", True, 1.46),
    ("wonder", False, 0.60),
    ("challah", True, 1.99),
    ("naan", True, 0.42),
    ("brioche", True, 2.03),
]

contact_info_dict = {
    "Zeb": (6304206969, "zeb@zeb.bakes", "@zeb.bakes", date(1999, 12, 19)),
    "Gary": (6304206969, "garyjones@gmail.com", "@gar-bear", date(1992, 4, 21)),
    "Rosalia": (6304206969, "rosalia@bakezone.org", "@rosybread", date(2001, 1, 21)),
    "Guido": (6304206969, "gvr@snakebread.io", "@snakebread", date(1995, 8, 23)),
}

baker_list = [
    ("Zeb", "they/them", 1),
    ("Gary", "he/him", 2),
    ("Rosalia", "she/her", 3),
    ("Guido", "he/him", 4),
]


# for core
baker_specialty_list = [
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 1),
    (3, 2),
    (3, 4),
    (4, 2),
    (4, 4),
    (4, 5),
]
