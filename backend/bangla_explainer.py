
"""
Bangla Explanation Generator
Simple language, no jargon, no fear-based messaging
"""

from typing import Dict, List

class BanglaExplainer:
    """
    Generates farmer-friendly Bangla explanations
    Structure: 🔎 কী সমস্যা ❓ কেন ✅ কী করবেন ❌ কী করবেন না ⚠️ সতর্কতা
    """

    def generate(self, diagnosis: str, cause: str, advice: Dict) -> Dict:
        """
        Generate structured Bangla explanation
        """
        return {
            "summary": self._generate_summary(diagnosis, cause),
            "problem": self._explain_problem(diagnosis, cause),
            "cause_explanation": self._explain_cause(cause),
            "action_items": self._generate_actions(advice),
            "donts": self._generate_donts(cause),
            "warnings": self._generate_warnings(),
            "follow_up": self._generate_follow_up()
        }

    def _generate_summary(self, diagnosis: str, cause: str) -> str:
        """Generate one-line summary"""
        return f"🔎 {diagnosis}। সম্ভবত কারণ: {cause}।"

    def _explain_problem(self, diagnosis: str, cause: str) -> str:
        """Explain what the problem is"""
        explanations = {
            "Fungal": "ছত্রাক একটি ক্ষুদ্র জীব যা গাছের রোগ সৃষ্টি করে। এটি বাতাস, পানি এবং মাটির মাধ্যমে ছড়িয়ে পড়ে।",
            "Bacterial": "ব্যাক্টেরিয়া ক্ষুদ্র জীবাণু যা গাছের ভেতরে প্রবেশ করে রোগ সৃষ্টি করে। এটি পানি ও কীটপতঙ্গের মাধ্যমে ছড়ায়।",
            "Viral": "ভাইরাস অতি ক্ষুদ্র জীবাণু যা কীটপতঙ্গের মাধ্যমে (যেমন সাদা মাছি) গাছে প্রবেশ করে।",
            "Insect": "পোকামাকড় গাছের বিভিন্ন অংশ কামড়িয়ে বা ভেতরে ঢুকে ক্ষতি করে।",
            "Nematode": "নেমাটোড হলো অতি ক্ষুদ্র কৃমি যা গোড়ায় থাকে এবং গিট তৈরি করে।",
            "Nutrient_deficiency": "মাটিতে প্রয়োজনীয় খাদ্য উপাদানের অভাবে গাছ সঠিকভাবে বাড়তে পারে না।",
            "Abiotic_stress": "অতিরিক্ত পানি, তাপ বা অন্যান্য পরিবেশগত কারণে গাছ ক্ষতিগ্রস্ত হয়।"
        }
        return f"❓ কেন এমন হয়েছে: {explanations.get(cause, 'সঠিক কারণ নির্ণয়ে পরীক্ষা প্রয়োজন।')}"

    def _explain_cause(self, cause: str) -> str:
        """Explain the cause in simple terms"""
        return "এটি সম্ভবত উপরোক্ত কারণে হয়েছে। তবে নিশ্চিত হতে কৃষি কর্মকর্তার পরামর্শ নিন।"

    def _generate_actions(self, advice: Dict) -> List[str]:
        """Generate action items in Bangla"""
        actions = ["✅ এখন কী করবেন:"]

        # Cultural practices
        if "cultural" in advice:
            actions.append("🌱 সাংস্কৃতিক পদ্ধতি:")
            for item in advice["cultural"][:3]:  # Top 3
                actions.append(f"  • {item}")

        # IPM
        if "ipm" in advice:
            actions.append("🐛 জৈবিক দমন (IPM):")
            for item in advice["ipm"][:2]:  # Top 2
                actions.append(f"  • {item}")

        # Chemical (last resort)
        if "chemical" in advice:
            actions.append("💊 রাসায়নিক (শেষ উপায়):")
            actions.append(f"  • {advice['chemical'][0] if advice['chemical'] else 'ETL অনুযায়ী ব্যবস্থা'}")
            actions.append("  • কীটনাশক ব্যবহারের আগে DAE অনুমোদিত তালিকা দেখুন")

        return actions

    def _generate_donts(self, cause: str) -> List[str]:
        """Generate don'ts in Bangla"""
        donts = ["❌ কী করবেন না:"]

        common_donts = [
            "বেশি পরিমাণ কীটনাশক স্প্রে করবেন না",
            "আক্রান্ত গাছের পরিচর্যা না করে অন্য গাছে কাজ করবেন না",
            "অনুমোদিত মাত্রার বেশি সার দেবেন না"
        ]

        specific_donts = {
            "Fungal": [
                "আক্রান্ত গাছের পাতা/ফল খেতে দেবেন না",
                "অনুমোদিত ছত্রাকনাশক ছাড়া অন্য ওষুধ ব্যবহার করবেন না"
            ],
            "Bacterial": [
                "আক্রান্ত গাছের রস যেন অন্য গাছে না লাগে",
                "ব্যাক্টেরিয়া নাশক ওষুধ ছাড়া অন্য কীটনাশক ব্যবহার করবেন না"
            ],
            "Viral": [
                "আক্রান্ত গাছ থেকে বীজ সংগ্রহ করবেন না",
                "কীটনাশক দিয়ে ভাইরাস সারাতে পারবেন না (বাহক পোকা দমন করুন)"
            ],
            "Insect": [
                "প্রতিদিন কীটনাশক স্প্রে করবেন না",
                "স্বাভাবিক শত্রু (ladybird beetle, spider) মারবেন না"
            ],
            "Nematode": [
                "আক্রান্ত গাছের চারা অন্য ক্ষেতে লাগাবেন না",
                "নেমাটোড আক্রান্ত মাটিতে বীজতলা করবেন না"
            ],
            "Nutrient_deficiency": [
                "অনুমানে সার দেবেন না",
                "মাটি পরীক্ষা না করে বেশি সার দেবেন না"
            ],
            "Abiotic_stress": [
                "অতিরিক্ত পানি দেবেন না",
                "তীব্র রোদে স্প্রে করবেন না"
            ]
        }

        donts.extend(common_donts)
        donts.extend(specific_donts.get(cause, []))

        return donts

    def _generate_warnings(self) -> List[str]:
        """Generate warnings"""
        return [
            "⚠️ সতর্কতা:",
            "• এই পরামর্শ কেবল AI-সহায়তা, চূড়ান্ত নির্ণয় নয়",
            "• কৃষি কর্মকর্তার সাথে যোগাযোগ করুন",
            "• কীটনাশক ব্যবহারের আগে DAE অনুমোদিত তালিকা দেখুন",
            "• সঠিক মাত্রা ও নিরাপত্তা বিধি অনুসরণ করুন",
            "• গুরুতর আক্রমণে 16263 নম্বরে কল করুন (DAE হটলাইন)"
        ]

    def _generate_follow_up(self) -> str:
        """Generate follow-up instructions"""
        return (
            "📞 পরবর্তী পদক্ষেপ:
"
            "• 3-5 দিন পর আবার ছবি তুলে পাঠান
"
            "• উন্নতি না হলে নিকটতম কৃষি অফিসে যোগাযোগ করুন
"
            "• ক্ষতির পরিমাণ বেশি হলে 16263 নম্বরে কল করুন"
        )

    def format_whatsapp(self, explanation: Dict) -> str:
        """Format for WhatsApp message"""
        lines = [
            f"*{explanation['summary']}*",
            "",
            explanation['problem'],
            "",
            "
".join(explanation['action_items']),
            "",
            "
".join(explanation['donts']),
            "",
            "
".join(explanation['warnings']),
            "",
            explanation['follow_up']
        ]
        return "
".join(lines)
