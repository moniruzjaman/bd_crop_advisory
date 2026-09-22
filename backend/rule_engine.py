
"""
JSON-based Rule Engine
Plantwise Elimination Logic
Returns probable cause groups only
"""

import json
from typing import Dict, List
from pathlib import Path

class RuleEngine:
    """
    Implements Plantwise elimination methodology
    Maps symptoms + observations to probable cause groups
    """

    ALLOWED_CAUSES = [
        "Fungal",
        "Bacterial", 
        "Viral",
        "Insect",
        "Nematode",
        "Nutrient_deficiency",
        "Abiotic_stress"
    ]

    def __init__(self, rules_path: str = None):
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict:
        """Load elimination rules"""
        # Comprehensive rules based on Plantwise methodology
        return {
            "leaf_spot": {
                "observation_rules": {
                    "concentric_rings": {"cause": "Fungal", "confidence": 0.8},
                    "water_soaked": {"cause": "Bacterial", "confidence": 0.75},
                    "yellow_halo": {"cause": "Bacterial", "confidence": 0.7},
                    "dark_margins": {"cause": "Fungal", "confidence": 0.75},
                    "small_black_dots": {"cause": "Fungal", "confidence": 0.8},
                    "spreading_fast": {"cause": "Bacterial", "confidence": 0.7}
                },
                "default": {"cause": "Fungal", "confidence": 0.6}
            },
            "yellowing": {
                "observation_rules": {
                    "uniform_yellow": {"cause": "Nutrient_deficiency", "confidence": 0.8},
                    "veins_stay_green": {"cause": "Nutrient_deficiency", "confidence": 0.85},
                    "older_leaves_first": {"cause": "Nutrient_deficiency", "confidence": 0.8},
                    "young_leaves_first": {"cause": "Viral", "confidence": 0.75},
                    "mosaic_pattern": {"cause": "Viral", "confidence": 0.85},
                    "stunted_growth": {"cause": "Nematode", "confidence": 0.7},
                    "waterlogged": {"cause": "Abiotic_stress", "confidence": 0.8}
                },
                "default": {"cause": "Nutrient_deficiency", "confidence": 0.55}
            },
            "wilt": {
                "observation_rules": {
                    "whole_plant": {"cause": "Fungal", "confidence": 0.75},
                    "one_side": {"cause": "Bacterial", "confidence": 0.8},
                    "recovery_at_night": {"cause": "Fungal", "confidence": 0.85},
                    "no_recovery": {"cause": "Bacterial", "confidence": 0.8},
                    "root_rot": {"cause": "Fungal", "confidence": 0.9},
                    "galls_on_roots": {"cause": "Nematode", "confidence": 0.9},
                    "dry_soil": {"cause": "Abiotic_stress", "confidence": 0.9}
                },
                "default": {"cause": "Fungal", "confidence": 0.6}
            },
            "mosaic": {
                "observation_rules": {
                    "irregular_pattern": {"cause": "Viral", "confidence": 0.9},
                    "leaf_curl": {"cause": "Viral", "confidence": 0.85},
                    "stunted": {"cause": "Viral", "confidence": 0.8},
                    "whiteflies_present": {"cause": "Viral", "confidence": 0.9}
                },
                "default": {"cause": "Viral", "confidence": 0.85}
            },
            "leaf_distortion": {
                "observation_rules": {
                    "curl_downward": {"cause": "Viral", "confidence": 0.8},
                    "curl_upward": {"cause": "Insect", "confidence": 0.75},
                    "thrips_present": {"cause": "Insect", "confidence": 0.9},
                    "aphids_present": {"cause": "Insect", "confidence": 0.9},
                    "irregular_shape": {"cause": "Viral", "confidence": 0.75}
                },
                "default": {"cause": "Insect", "confidence": 0.6}
            },
            "galls": {
                "observation_rules": {
                    "on_roots": {"cause": "Nematode", "confidence": 0.95},
                    "on_stem": {"cause": "Insect", "confidence": 0.8},
                    "on_leaves": {"cause": "Insect", "confidence": 0.85},
                    "swollen_nodes": {"cause": "Nematode", "confidence": 0.9}
                },
                "default": {"cause": "Nematode", "confidence": 0.7}
            },
            "necrosis_blight": {
                "observation_rules": {
                    "rapid_spread": {"cause": "Bacterial", "confidence": 0.8},
                    "fuzzy_growth": {"cause": "Fungal", "confidence": 0.9},
                    "bad_smell": {"cause": "Bacterial", "confidence": 0.85},
                    "starting_from_tips": {"cause": "Abiotic_stress", "confidence": 0.75},
                    "after_frost": {"cause": "Abiotic_stress", "confidence": 0.9}
                },
                "default": {"cause": "Fungal", "confidence": 0.65}
            },
            "root_problem": {
                "observation_rules": {
                    "rotten_smell": {"cause": "Fungal", "confidence": 0.85},
                    "white_fungus": {"cause": "Fungal", "confidence": 0.9},
                    "knots_galls": {"cause": "Nematode", "confidence": 0.95},
                    "blackened": {"cause": "Fungal", "confidence": 0.8},
                    "waterlogged_soil": {"cause": "Abiotic_stress", "confidence": 0.85}
                },
                "default": {"cause": "Fungal", "confidence": 0.6}
            },
            "stem_damage": {
                "observation_rules": {
                    "bore_holes": {"cause": "Insect", "confidence": 0.95},
                    "frass_present": {"cause": "Insect", "confidence": 0.9},
                    "discolored_vascular": {"cause": "Bacterial", "confidence": 0.85},
                    "canker": {"cause": "Fungal", "confidence": 0.8},
                    "splitting": {"cause": "Abiotic_stress", "confidence": 0.7}
                },
                "default": {"cause": "Insect", "confidence": 0.65}
            },
            "panicle_ear_problem": {
                "observation_rules": {
                    "blank_grains": {"cause": "Viral", "confidence": 0.75},
                    "discolored_grains": {"cause": "Fungal", "confidence": 0.85},
                    "insects_inside": {"cause": "Insect", "confidence": 0.95},
                    "sterility": {"cause": "Abiotic_stress", "confidence": 0.8},
                    "partial_filling": {"cause": "Nutrient_deficiency", "confidence": 0.8}
                },
                "default": {"cause": "Fungal", "confidence": 0.6}
            },
            "healthy": {
                "default": {"cause": "None", "confidence": 1.0}
            }
        }

    def process(self, symptom: str, observation_flags: List[str], crop: str = None) -> Dict:
        """
        Process symptom and observations to determine probable cause
        Always returns "Probable" level language
        """
        if symptom not in self.rules:
            return {
                "cause_group": "Unknown",
                "confidence": 0.0,
                "message": "সিম্পটম চিহ্নিত করা যায়নি (Symptom not recognized)"
            }

        rule_set = self.rules[symptom]

        # Check observation flags
        max_confidence = 0
        selected_cause = rule_set["default"]["cause"]

        for flag in observation_flags:
            if flag in rule_set.get("observation_rules", {}):
                flag_rule = rule_set["observation_rules"][flag]
                if flag_rule["confidence"] > max_confidence:
                    max_confidence = flag_rule["confidence"]
                    selected_cause = flag_rule["cause"]

        # If no flags matched, use default
        if max_confidence == 0:
            max_confidence = rule_set["default"]["confidence"]

        # Generate Bangla cause name
        cause_names = {
            "Fungal": "ছত্রাক (Fungal)",
            "Bacterial": "ব্যাক্টেরিয়া (Bacterial)",
            "Viral": "ভাইরাস (Viral)",
            "Insect": "পোকামাকড় (Insect)",
            "Nematode": "নেমাটোড/গোড়া পোকা (Nematode)",
            "Nutrient_deficiency": "পুষ্টির অভাব (Nutrient deficiency)",
            "Abiotic_stress": "পরিবেশগত চাপ (Environmental stress)",
            "Unknown": "অজানা (Unknown)",
            "None": "কোনো সমস্যা নেই (None)"
        }

        return {
            "cause_group": selected_cause,
            "confidence": round(max_confidence, 2),
            "cause_name_bn": cause_names.get(selected_cause, selected_cause),
            "message": f"সম্ভবত: {cause_names.get(selected_cause, selected_cause)}",
            "level": "Probable",
            "requires_expert": max_confidence < 0.7
        }

    def get_elimination_questions(self, symptom: str) -> List[Dict]:
        """Get relevant observation questions for symptom"""
        questions = {
            "leaf_spot": [
                {"id": "concentric_rings", "text_bn": "দাগের মধ্যে গোল গোল বলয় আছে কি?", "text_en": "Concentric rings in spots?"},
                {"id": "water_soaked", "text_bn": "দাগ পানিতে ভেজা দেখাচ্ছে কি?", "text_en": "Water-soaked appearance?"},
                {"id": "yellow_halo", "text_bn": "দাগের চারপাশে হলুদ বলয় আছে কি?", "text_en": "Yellow halo around spots?"}
            ],
            "yellowing": [
                {"id": "veins_stay_green", "text_bn": "শিরা সবুজ আছে কিন্তু পাতা হলুদ?", "text_en": "Veins green but leaf yellow?"},
                {"id": "older_leaves_first", "text_bn": "নিচের পাতা আগে হলুদ হয়েছে?", "text_en": "Older leaves yellowed first?"},
                {"id": "mosaic_pattern", "text_bn": "পাতায় মোজাইক/টাইলস প্যাটার্ন আছে কি?", "text_en": "Mosaic pattern on leaves?"}
            ],
            "wilt": [
                {"id": "recovery_at_night", "text_bn": "রাতে গাছ সুস্থ দেখাচ্ছে কিন্তু দিনে শুকিয়ে যাচ্ছে?", "text_en": "Recovers at night, wilts by day?"},
                {"id": "one_side", "text_bn": "গাছের একপাশ শুকিয়ে গেছে?", "text_en": "Only one side wilting?"},
                {"id": "root_rot", "text_bn": "গোড়া পচে গেছে কি?", "text_en": "Roots rotting?"}
            ],
            "mosaic": [
                {"id": "leaf_curl", "text_bn": "পাতা কুঁকড়ে গেছে কি?", "text_en": "Leaves curling?"},
                {"id": "stunted", "text_bn": "গাছের বৃদ্ধি কমেছে কি?", "text_en": "Stunted growth?"},
                {"id": "whiteflies_present", "text_bn": "সাদা মাছি দেখা যাচ্ছে কি?", "text_en": "Whiteflies present?"}
            ],
            "leaf_distortion": [
                {"id": "thrips_present", "text_bn": "ক্ষুদ্র পোকা (থ্রিপস) দেখা যাচ্ছে কি?", "text_en": "Thrips visible?"},
                {"id": "aphids_present", "text_bn": "এফিড/পাতা পোকা দেখা যাচ্ছে কি?", "text_en": "Aphids visible?"},
                {"id": "curl_downward", "text_bn": "পাতা নিচের দিকে কুঁকড়ে আছে কি?", "text_en": "Leaves curling downward?"}
            ],
            "galls": [
                {"id": "on_roots", "text_bn": "গোড়ায় ফোলা আছে কি?", "text_en": "Swelling on roots?"},
                {"id": "on_stem", "text_bn": "কাণ্ডে ফোলা আছে কি?", "text_en": "Swelling on stem?"},
                {"id": "on_leaves", "text_bn": "পাতায় গাল/ফোলা আছে কি?", "text_en": "Galls on leaves?"}
            ],
            "necrosis_blight": [
                {"id": "fuzzy_growth", "text_bn": "পাতায় তুলতুলে ছত্রাক দেখা যাচ্ছে কি?", "text_en": "Fuzzy fungal growth?"},
                {"id": "rapid_spread", "text_bn": "দ্রুত ছড়িয়ে পড়ছে কি?", "text_en": "Spreading rapidly?"},
                {"id": "starting_from_tips", "text_bn": "পাতার ডগা থেকে শুরু হয়েছে কি?", "text_en": "Starting from leaf tips?"}
            ],
            "root_problem": [
                {"id": "rotten_smell", "text_bn": "গোড়া থেকে পচা গন্ধ আসছে কি?", "text_en": "Rotten smell from roots?"},
                {"id": "knots_galls", "text_bn": "গোড়ায় গিট/ফোলা আছে কি?", "text_en": "Knots/galls on roots?"},
                {"id": "white_fungus", "text_bn": "সাদা ছত্রাক দেখা যাচ্ছে কি?", "text_en": "White fungus visible?"}
            ],
            "stem_damage": [
                {"id": "bore_holes", "text_bn": "কাণ্ডে ছিদ্র আছে কি?", "text_en": "Bore holes in stem?"},
                {"id": "frass_present", "text_bn": "কাণ্ডে পোকার বিষ্ঠা আছে কি?", "text_en": "Insect frass present?"},
                {"id": "discolored_vascular", "text_bn": "কাণ্ড কাটলে ভেতরে রং পরিবর্তন দেখা যাচ্ছে কি?", "text_en": "Discolored vascular tissue?"}
            ],
            "panicle_ear_problem": [
                {"id": "insects_inside", "text_bn": "শীষে/ফলে পোকা আছে কি?", "text_en": "Insects inside ear/fruit?"},
                {"id": "blank_grains", "text_bn": "শীষে খালি দানা আছে কি?", "text_en": "Blank grains in ear?"},
                {"id": "discolored_grains", "text_bn": "দানার রং পরিবর্তন হয়েছে কি?", "text_en": "Discolored grains?"}
            ]
        }

        return questions.get(symptom, [])
