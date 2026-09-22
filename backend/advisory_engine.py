
"""
Bangladesh Advisory Engine
Integrates BRRI, BARI, DAE, SRDI, BARC knowledge
No pesticide dosage - only IPM and approved chemicals
"""

import json
from typing import Dict, List
from pathlib import Path

class AdvisoryEngine:
    """
    Generates government-authoritative advisory
    Sources: BRRI (Rice), BARI (Vegetables), DAE (Pesticide), SRDI (Nutrient), BARC (IPM)
    """

    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> Dict:
        """Load Bangladesh agricultural knowledge base"""
        return {
            "rice": {
                "Fungal": {
                    "diagnosis": "সম্ভবত ছত্রাকজনিত রোগ (Probable fungal disease)",
                    "common_diseases": ["Blast", "Sheath Blight", "Brown Spot"],
                    "cultural": [
                        "সহনশীল জাত ব্যবহার করুন (BRRI dhan33, BRRI dhan34)",
                        "সুস্থ বীজ ব্যবহার করুন",
                        "বীজ শোধন করুন (Thiram/Captan/Bavistin দিয়ে)",
                        "সুষম সার প্রয়োগ করুন",
                        "ক্ষেতে স্থায়ী জল রাখুন",
                        "আক্রান্ত গাছ পুড়িয়ে ফেলুন"
                    ],
                    "ipm": [
                        "Trichoderma বীজ শোধন (3%)",
                        "BAU-Biofungicide স্প্রে (3%)",
                        "সুষম সার ব্যবহার (বেশি ইউরিয়া নয়)",
                        "আক্রান্ত গাছ অপসারণ"
                    ],
                    "chemical": [
                        "অনুমোদিত ছত্রাকনাশক ব্যবহার করুন (DAE অনুমোদিত)",
                        "ETL (অর্থনৈতিক ক্ষতির সীমা) অনুযায়ী স্প্রে করুন",
                        "Amistar Top 325 SC @ 1 mL/L (Sheath blight এর জন্য)",
                        "Bavistin @ 0.1% (প্রতিরোধমূলক)"
                    ],
                    "etl": "Sheath blight: 20-25% কাণ্ড আক্রান্ত হলে স্প্রে করুন"
                },
                "Bacterial": {
                    "diagnosis": "সম্ভবত ব্যাক্টেরিয়াজনিত রোগ (Probable bacterial disease)",
                    "common_diseases": ["Bacterial Blight", "Bacterial Leaf Streak"],
                    "cultural": [
                        "সহনশীল জাত ব্যবহার করুন (Xa21 জিনযুক্ত: BRRI dhan51)",
                        "সুস্থ বীজ সংগ্রহ করুন",
                        "ক্ষেত শুকিয়ে দিন (7-8 দিন জল বন্ধ রাখুন)",
                        "0.33 একরে 5 কেজি পটাশ সার প্রয়োগ করুন",
                        "আক্রান্ত গাছ পুড়িয়ে ফেলুন"
                    ],
                    "ipm": [
                        "বীজ শোধন: Streptocycline (1g/40L জল) 30 মিনিট",
                        "সুষম সার: ইউরিয়া তিন কিস্তিতে দিন",
                        "পোকা দমন (পাতা কাটা পোকা রোধে)"
                    ],
                    "chemical": [
                        "Streptocycline স্প্রে (অনুমোদিত মাত্রায়)",
                        "Copper oxychloride (অনুমোদিত)"
                    ],
                    "etl": "10-15% পাতা আক্রান্ত হলে ব্যবস্থা নিন"
                },
                "Viral": {
                    "diagnosis": "সম্ভবত ভাইরাসজনিত রোগ (Probable viral disease)",
                    "common_diseases": ["Rice Tungro", "Rice Ragged Stunt"],
                    "cultural": [
                        "সহনশীল জাত ব্যবহার করুন",
                        "আক্রান্ত গাছ তুলে পুড়িয়ে ফেলুন",
                        "আরাই ঘাস (weed) পরিষ্কার করুন",
                        "বালাই ফাঁদ ও হাতজাল ব্যবহার করুন"
                    ],
                    "ipm": [
                        "ভাইরাস বাহক পোকা দমন (সবুজ পাতা পোকা, ব্রাউন প্ল্যান্ট হপার)",
                        "হাতজাল দিয়ে পোকা ধরুন",
                        "বালাই ফাঁদ ব্যবহার করুন"
                    ],
                    "chemical": [
                        "ETL অনুযায়ী কীটনাশক স্প্রে (বাহক পোকার জন্য)",
                        "Abamectin 1.8 EC @ 1 litre/ha (BPH এর জন্য)"
                    ],
                    "etl": "2-4টি প্রাপ্ত বা 8-10টি নিম্ফ প্রতি গাছে"
                },
                "Insect": {
                    "diagnosis": "সম্ভবত পোকামাকড়ের আক্রমণ (Probable insect pest)",
                    "common_pests": ["Stem Borer", "Brown Plant Hopper", "Rice Hispa"],
                    "cultural": [
                        "25x15 বা 20x20 সেমি দূরত্বে চারা রোপণ",
                        "আলো ও বাতাস চলাচলের ব্যবস্থা করুন",
                        "আক্রান্ত তন্ডুল পোড়ান",
                        "অবশিষ্টাংশ পুড়িয়ে বা মাটিতে মিশিয়ে দিন"
                    ],
                    "ipm": [
                        "বালাই ফাঁদ ব্যবহার",
                        "পাখি বসার ব্যবস্থা (perching)",
                        "প্যারাসাইটিক মাছি সংরক্ষণ",
                        "ডিম সংগ্রহ করে ধ্বংস করুন"
                    ],
                    "chemical": [
                        "ETL অনুযায়ী অনুমোদিত কীটনাশক ব্যবহার",
                        "Furadan 5G @ 2.5 kg/bigha (Ufra/Stem borer এর জন্য)",
                        "Abamectin 1.8 EC @ 1 L/ha (BPH এর জন্য)"
                    ],
                    "etl": "5% সাদা শীষ (Stem borer), 35% পাতা ক্ষতি (Hispa)"
                },
                "Nematode": {
                    "diagnosis": "সম্ভবত নেমাটোড/গোড়া পোকা (Probable nematode)",
                    "common": ["Root Knot Nematode", "Ufra"],
                    "cultural": [
                        "সহনশীল জাত ব্যবহার (Raida, Bajail)",
                        "ঘাস জাতীয় আগাছা নিয়ন্ত্রণ করুন",
                        "অবশিষ্টাংশ পুড়িয়ে ফেলুন",
                        "গভীর চাষ করে গোড়া পোকা মারুন"
                    ],
                    "ipm": [
                        "বীজ শোধন: Furadan 5G (15g/1L জল) এক রাত ভিজিয়ে রাখুন",
                        "নিম খৈল প্রয়োগ @ 250 kg/ha",
                        "গ্যাসিং (soil solarization) পদ্ধতি"
                    ],
                    "chemical": [
                        "Furadan 5G @ 2.5 kg/bigha (Ufra এর জন্য)",
                        "Carbofuran 3G @ 1 kg a.i./ha"
                    ],
                    "etl": "গোড়ায় গিট দেখা দিলে তৎক্ষণাৎ ব্যবস্থা"
                },
                "Nutrient_deficiency": {
                    "diagnosis": "সম্ভবত পুষ্টির অভাব (Probable nutrient deficiency)",
                    "cultural": [
                        "মাটি পরীক্ষা করুন (SRDI-তে যোগাযোগ করুন)",
                        "সুষম সার প্রয়োগ করুন",
                        "জৈব সার ব্যবহার বাড়ান",
                        "pH সমন্বয় করুন"
                    ],
                    "ipm": [
                        "সবুজ সার (Green manure) ব্যবহার",
                        "কম্পোস্ট সার প্রয়োগ",
                        "বায়োফার্টিলাইজার ব্যবহার"
                    ],
                    "chemical": [
                        "ঘাটতি অনুযায়ী সার প্রয়োগ",
                        "Zn, B, Mg ঘাটতি হলে স্প্রে"
                    ],
                    "etl": "পাতা রং পরিবর্তন দেখা দিলে"
                }
            },
            "eggplant": {
                "Fungal": {
                    "diagnosis": "সম্ভবত ছত্রাকজনিত রোগ (Probable fungal disease)",
                    "common_diseases": ["Fruit & Stem Rot", "Phomopsis Blight", "Damping Off"],
                    "cultural": [
                        "রোগমুক্ত বীজ ব্যবহার করুন",
                        "3-4 বছর ফসল পর্যায়ক্রমিক চাষ করুন",
                        "আক্রান্ত উদ্ভিদ অংশ ধ্বংস করুন",
                        "সোলানেসি আগাছা (nightshade) নিয়ন্ত্রণ করুন",
                        "মালচিং এবং সারি সেচ ব্যবহার করুন"
                    ],
                    "ipm": [
                        "BAU-Biofungicide (3%) স্প্রে",
                        "Trichoderma বীজ শোধন",
                        "সুষম সার ব্যবহার"
                    ],
                    "chemical": [
                        "Bavistin @ 2g/L (প্রতিরোধমূলক)",
                        "Mancozeb (অনুমোদিত মাত্রায়)",
                        "ETL অনুযায়ী স্প্রে"
                    ],
                    "etl": "20-25% ফল/কাণ্ড আক্রান্ত হলে"
                },
                "Bacterial": {
                    "diagnosis": "সম্ভবত ব্যাক্টেরিয়াজনিত রোগ (Probable bacterial disease)",
                    "common_diseases": ["Bacterial Wilt"],
                    "cultural": [
                        "রোগমুক্ত বীজ ব্যবহার",
                        "রোগমুক্ত চারা তৈরি করুন",
                        "টমেটো, আলু, ঢেঁড়সের পর বেগুন চাষ করবেন না",
                        "আক্রান্ত গাছ তুলে ধ্বংস করুন"
                    ],
                    "ipm": [
                        "বীজ শোধন: Streptocycline (1g/40L জল) 30 মিনিট",
                        "রোগ প্রতিরোধী জাত: Jessore local, Kata begun, Ishwardi-1",
                        "গোড়ায় ছাই দিন (ash treatment)"
                    ],
                    "chemical": [
                        "Streptocycline (অনুমোদিত মাত্রায়)",
                        "Copper fungicide (প্রতিরোধমূলক)"
                    ],
                    "etl": "গাছ হঠাৎ শুকিয়ে গেলে তৎক্ষণাৎ ব্যবস্থা"
                },
                "Insect": {
                    "diagnosis": "সম্ভবত পোকামাকড়ের আক্রমণ (Probable insect pest)",
                    "common_pests": ["Shoot & Fruit Borer (BSFB)", "Epilachna Beetle", "Thrips"],
                    "cultural": [
                        "আক্রান্ত ডগা ও ফল সংগ্রহ করে ধ্বংস করুন",
                        "আগাছা পরিষ্কার রাখুন",
                        "ফল ব্যাগিং (polythene bag with pinholes)",
                        "পরিষ্কার চাষাবাদ"
                    ],
                    "ipm": [
                        "সেক্স ফেরোমোন ফাঁদ (10-15m গ্রিডে)",
                        "Bt বেগুন (BARI অনুমোদিত) ব্যবহার",
                        "বালাই ফাঁদ ও পাখি বসানোর ব্যবস্থা",
                        "Spinosad 45SC @ 4ml/10L (গুরুতর আক্রমণে)",
                        "Neem solution (1kg neem/20L water, 12 ঘণ্টা ভিজিয়ে)"
                    ],
                    "chemical": [
                        "ETL অনুযায়ী অনুমোদিত কীটনাশক",
                        "Spinosad (বায়ো-কীটনাশক, অনুমোদিত)",
                        "Fipronil (অনুমোদিত মাত্রায়)"
                    ],
                    "etl": "5% ডগা বা ফল আক্রান্ত হলে"
                }
            },
            "tomato": {
                "Fungal": {
                    "diagnosis": "সম্ভবত ছত্রাকজনিত রোগ (Probable fungal disease)",
                    "common_diseases": ["Early Blight", "Late Blight", "Fusarium Wilt"],
                    "cultural": [
                        "রোগমুক্ত বীজ ব্যবহার",
                        "ক্ষেত পরিষ্কার রাখুন",
                        "সারি সেচ ব্যবহার করুন (overhead irrigation নয়)",
                        "3 বছর ফসল পর্যায়ক্রমিক চাষ"
                    ],
                    "ipm": [
                        "Trichoderma বীজ শোধন (3%)",
                        "BAU-Biofungicide (3%) স্প্রে 7 দিন অন্তর",
                        "সুষম সার ব্যবহার"
                    ],
                    "chemical": [
                        "Dithane M-45 @ 7 দিন অন্তর (Early blight)",
                        "Mancozeb (Late blight)",
                        "Carbendazim (অনুমোদিত মাত্রায়)"
                    ],
                    "etl": "10-15% পাতা আক্রান্ত হলে"
                },
                "Bacterial": {
                    "diagnosis": "সম্ভবত ব্যাক্টেরিয়াজনিত রোগ (Probable bacterial disease)",
                    "common_diseases": ["Bacterial Wilt", "Bacterial Spot"],
                    "cultural": [
                        "রোগমুক্ত বীজ ও চারা ব্যবহার",
                        "3 বছর ধান/শস্য চাষ করুন (আক্রান্ত ক্ষেতে)",
                        "আক্রান্ত গাছ তুলে ধ্বংস করুন",
                        "ক্ষেত শুকিয়ে দিন (7-8 দিন)"
                    ],
                    "ipm": [
                        "বীজ শোধন: Streptocycline (1g/40L জল)",
                        "মাটির pH সমন্বয় (pH 6.5-7.0)",
                        "গোড়ায় ছাই প্রয়োগ"
                    ],
                    "chemical": [
                        "Streptocycline (অনুমোদিত)",
                        "Copper oxychloride"
                    ],
                    "etl": "একটি গাছ আক্রান্ত হলেও ব্যবস্থা নিন"
                },
                "Viral": {
                    "diagnosis": "সম্ভবত ভাইরাসজনিত রোগ (Probable viral disease)",
                    "common_diseases": ["Tomato Leaf Curl Virus", "Tomato Mosaic Virus"],
                    "cultural": [
                        "জালের নিচে চারা তৈরি করুন",
                        "আক্রান্ত গাছ ও আগাছা তুলে ধ্বংস করুন",
                        "বাধা ফসল (barrier crop) ব্যবহার",
                        "হলুদ আঠালো ফাঁদ (yellow sticky trap)"
                    ],
                    "ipm": [
                        "সাদা মাছি (whitefly) দমন - ভাইরাস বাহক",
                        "Dimethoate @ 10 দিন অন্তর (গুরুতর আক্রমণে)",
                        "Neem extract স্প্রে"
                    ],
                    "chemical": [
                        "Dimethoate (সাদা মাছির জন্য, অনুমোদিত)",
                        "Imidacloprid (অনুমোদিত মাত্রায়)"
                    ],
                    "etl": "5% গাছ আক্রান্ত হলে"
                }
            },
            "potato": {
                "Fungal": {
                    "diagnosis": "সম্ভবত ছত্রাকজনিত রোগ (Probable fungal disease)",
                    "common_diseases": ["Late Blight", "Early Blight", "Black Scurf"],
                    "cultural": [
                        "সুস্থ আলু বীজ ব্যবহার",
                        "3-4 বছর ফসল পর্যায়ক্রমিক চাষ",
                        "আক্রান্ত আলু ধ্বংস করুন",
                        "সারি সেচ ব্যবহার করুন"
                    ],
                    "ipm": [
                        "Ridomil Gold (Metalaxyl) বীজ শোধন",
                        "BAU-Biofungicide স্প্রে",
                        "সুষম সার ব্যবহার"
                    ],
                    "chemical": [
                        "Mancozeb (প্রতিরোধমূলক)",
                        "Ridomil Gold MZ (গুরুতর আক্রমণে)",
                        "Dithane M-45"
                    ],
                    "etl": "5-10% পাতা আক্রান্ত হলে"
                }
            },
            "default": {
                "Fungal": {
                    "diagnosis": "সম্ভবত ছত্রাকজনিত রোগ (Probable fungal disease)",
                    "cultural": [
                        "রোগমুক্ত বীজ/চারা ব্যবহার করুন",
                        "ক্ষেত পরিষ্কার রাখুন",
                        "আক্রান্ত গাছ পুড়িয়ে ফেলুন",
                        "সুষম সার প্রয়োগ করুন",
                        "সেচ ব্যবস্থা সমন্বয় করুন (overhead irrigation এড়িয়ে চলুন)"
                    ],
                    "ipm": [
                        "Trichoderma বীজ শোধন (3%)",
                        "BAU-Biofungicide স্প্রে",
                        "সুষম সার ব্যবহার",
                        "ফসল পর্যায়ক্রমিকতা"
                    ],
                    "chemical": [
                        "অনুমোদিত ছত্রাকনাশক ব্যবহার করুন (DAE অনুমোদিত তালিকা থেকে)",
                        "ETL (অর্থনৈতিক ক্ষতির সীমা) অনুযায়ী স্প্রে করুন",
                        "Mancozeb/Carbendazim (অনুমোদিত মাত্রায়)"
                    ],
                    "etl": "ETL অনুযায়ী ব্যবস্থা নিন"
                },
                "Bacterial": {
                    "diagnosis": "সম্ভবত ব্যাক্টেরিয়াজনিত রোগ (Probable bacterial disease)",
                    "cultural": [
                        "রোগমুক্ত বীজ ব্যবহার",
                        "আক্রান্ত গাছ তুলে ধ্বংস করুন",
                        "ক্ষেত শুকিয়ে দিন (কিছুদিন সেচ বন্ধ রাখুন)",
                        "সোলানেসি পরিবারের ফসল পর্যায়ক্রমিকতা (টমেটো, আলু, বেগুন)"
                    ],
                    "ipm": [
                        "বীজ শোধন: Streptocycline (1g/40L জল) 30 মিনিট",
                        "গোড়ায় ছাই প্রয়োগ",
                        "মাটির pH সমন্বয়"
                    ],
                    "chemical": [
                        "Streptocycline (অনুমোদিত মাত্রায়)",
                        "Copper oxychloride (প্রতিরোধমূলক)"
                    ],
                    "etl": "আক্রমণ দেখা দিলে তৎক্ষণাৎ ব্যবস্থা"
                },
                "Viral": {
                    "diagnosis": "সম্ভবত ভাইরাসজনিত রোগ (Probable viral disease)",
                    "cultural": [
                        "রোগমুক্ত বীজ/চারা ব্যবহার",
                        "জালের নিচে চারা তৈরি করুন",
                        "আক্রান্ত গাছ ও আগাছা তুলে ধ্বংস করুন",
                        "বাধা ফসল ব্যবহার করুন"
                    ],
                    "ipm": [
                        "ভাইরাস বাহক পোকা দমন (সাদা মাছি, এফিড)",
                        "হলুদ আঠালো ফাঁদ ব্যবহার",
                        "Neem extract স্প্রে"
                    ],
                    "chemical": [
                        "ETL অনুযায়ী কীটনাশক (বাহক পোকার জন্য)",
                        "Imidacloprid/Dimethoate (অনুমোদিত)"
                    ],
                    "etl": "5% গাছ আক্রান্ত বা বাহক পোকা ETL অতিক্রম করলে"
                },
                "Insect": {
                    "diagnosis": "সম্ভবত পোকামাকড়ের আক্রমণ (Probable insect pest)",
                    "cultural": [
                        "আক্রান্ত অংশ সংগ্রহ করে ধ্বংস করুন",
                        "ক্ষেত পরিষ্কার রাখুন",
                        "আগাছা নিয়ন্ত্রণ করুন",
                        "পরিষ্কার চাষাবাদ"
                    ],
                    "ipm": [
                        "বালাই ফাঁদ ব্যবহার",
                        "পাখি বসানোর ব্যবস্থা (perching)",
                        "স্বাভাবিক শত্রু সংরক্ষণ",
                        "Neem solution (1kg neem/20L water)"
                    ],
                    "chemical": [
                        "ETL অনুযায়ী অনুমোদিত কীটনাশক ব্যবহার",
                        "Spinosad, Malathion (অনুমোদিত মাত্রায়)",
                        "যে কীটনাশকই ব্যবহার করুন না কেন, DAE অনুমোদিত তালিকা থেকে নিন"
                    ],
                    "etl": "ETL অনুযায়ী ব্যবস্থা নিন"
                },
                "Nematode": {
                    "diagnosis": "সম্ভবত নেমাটোড/গোড়া পোকা (Probable nematode)",
                    "cultural": [
                        "আগাছা ও আগাছা হোস্ট ধ্বংস করুন",
                        "গভীর চাষ করুন (গ্রীষ্মে)",
                        "ক্ষেত 2-3 সপ্তাহ পরিত্যক্ত রাখুন",
                        "গোড়া পরীক্ষা করুন"
                    ],
                    "ipm": [
                        "নিম খৈল প্রয়োগ @ 250 kg/ha",
                        "মাটি সোলারাইজেশন (গ্রীষ্মে)",
                        "বায়োনিমাটিসাইড (Trichoderma, Pseudomonas)"
                    ],
                    "chemical": [
                        "Carbofuran 3G @ 1 kg a.i./ha",
                        "Furadan 5G (অনুমোদিত মাত্রায়)"
                    ],
                    "etl": "গোড়ায় গিট দেখা দিলে"
                },
                "Nutrient_deficiency": {
                    "diagnosis": "সম্ভবত পুষ্টির অভাব (Probable nutrient deficiency)",
                    "cultural": [
                        "মাটি পরীক্ষা করুন (SRDI-তে যোগাযোগ করুন)",
                        "সুষম সার প্রয়োগ করুন",
                        "জৈব সার ব্যবহার বাড়ান",
                        "pH সমন্বয় করুন"
                    ],
                    "ipm": [
                        "সবুজ সার ব্যবহার",
                        "কম্পোস্ট/ভার্মিকম্পোস্ট প্রয়োগ",
                        "বায়োফার্টিলাইজার ব্যবহার"
                    ],
                    "chemical": [
                        "NPK সার সমন্বয়",
                        "Zn, B, Mg, Fe ঘাটতি অনুযায়ী স্প্রে"
                    ],
                    "etl": "পাতা রং পরিবর্তন দেখা দিলে"
                },
                "Abiotic_stress": {
                    "diagnosis": "সম্ভবত পরিবেশগত চাপ (Probable environmental stress)",
                    "cultural": [
                        "সেচ ব্যবস্থা সমন্বয় করুন",
                        "অতিরিক্ত পানি নিষ্কাশন করুন",
                        "ছায়ার ব্যবস্থা করুন (যদি অতি তাপ)",
                        "মাটি পরিষ্কার রাখুন"
                    ],
                    "ipm": [
                        "মালচিং ব্যবহার",
                        "সুষম সার (বিশেষ করে পটাশ)"
                    ],
                    "chemical": [
                        "প্রয়োজনে কেল্প/সি-উইড স্প্রে"
                    ],
                    "etl": "পরিবেশগত কারণ দেখা দিলে"
                }
            }
        }

    def generate(self, symptom: str, cause_group: str, crop: str, confidence: float) -> Dict:
        """
        Generate advisory based on crop and cause group
        """
        # Get crop-specific or default advisory
        crop_kb = self.knowledge_base.get(crop, self.knowledge_base["default"])

        if cause_group not in crop_kb:
            cause_group = "Fungal"  # Default fallback

        advisory_data = crop_kb[cause_group]

        # Build response
        return {
            "diagnosis": advisory_data["diagnosis"],
            "confidence_level": "low" if confidence < 0.6 else "medium" if confidence < 0.8 else "high",
            "ai_certainty": "এটি AI-পরামর্শ, চূড়ান্ত নির্ণয়ের জন্য কৃষি কর্মকর্তার সাথে কথা বলুন",
            "advice": {
                "cultural": advisory_data["cultural"],
                "ipm": advisory_data["ipm"],
                "chemical": advisory_data["chemical"]
            },
            "etl_condition": advisory_data.get("etl", "ETL অনুযায়ী ব্যবস্থা নিন"),
            "sources": ["BRRI", "BARI", "DAE", "SRDI", "BARC"],
            "disclaimer": "⚠️ এই পরামর্শ কেবল AI-সহায়তা। চূড়ান্ত সিদ্ধান্তের জন্য DAE/BARI/BRRI কর্মকর্তার সাথে যোগাযোগ করুন। কীটনাশক ব্যবহারের আগে DAE অনুমোদিত তালিকা দেখুন এবং সঠিক মাত্রা অনুসরণ করুন।"
        }
