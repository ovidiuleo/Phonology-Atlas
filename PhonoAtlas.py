import streamlit as st
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
import json
import re
import uuid
from collections import defaultdict, Counter
from datetime import datetime

st.set_page_config(page_title="Decision Atlas", page_icon="🧭", layout="wide")

# ============================================================
# THEME
# ============================================================

THEME = {
    "header_bg": "linear-gradient(90deg, #155e75 0%, #0f766e 55%, #1d4ed8 100%)",
    "header_text": "#ffffff",
    "surface": "#ffffff",
    "surface_alt": "#f3f4f6",
    "border": "#d1d5db",
    "text": "#1f2937",
    "muted": "#6b7280",
    "tab_clinical": "#1f6fb2",
    "tab_education": "#0f766e",
    "button_primary": "#1f6fb2",
    "button_primary_hover": "#1a5f97",
    "button_secondary": "#0f766e",
    "button_secondary_hover": "#0b5b54",
    "success_bg": "#ecfdf5",
    "success_border": "#10b981",
    "warning_bg": "#fff7ed",
    "warning_border": "#f59e0b",
    "danger_bg": "#fef2f2",
    "danger_border": "#ef4444",
    "info_bg": "#eff6ff",
    "info_border": "#3b82f6",
    "chip_blue_bg": "#dbeafe",
    "chip_blue_fg": "#1d4ed8",
    "chip_green_bg": "#dcfce7",
    "chip_green_fg": "#166534",
    "chip_purple_bg": "#ede9fe",
    "chip_purple_fg": "#6d28d9",
    "chip_amber_bg": "#fef3c7",
    "chip_amber_fg": "#92400e",
    "chip_red_bg": "#fee2e2",
    "chip_red_fg": "#991b1b",
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {THEME['surface_alt']};
        color: {THEME['text']};
    }}

    .block-container {{
        padding-top: 0.7rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }}

    .atlas-header {{
        position: sticky;
        top: 0;
        z-index: 999;
        background: {THEME['header_bg']};
        color: {THEME['header_text']};
        padding: 2rem 1.4rem;
        border-radius: 26px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
        margin-bottom: 1rem;
        overflow: hidden;
    }}

    .atlas-header::after {{
        content: "";
        position: absolute;
        right: -80px;
        top: -60px;
        width: 320px;
        height: 320px;
        background: rgba(255,255,255,0.10);
        border-radius: 50%;
    }}

    .atlas-header h1 {{
        margin: 0;
        font-size: 3rem;
        line-height: 1.08;
        position: relative;
        z-index: 1;
        text-align: center;
    }}

    .atlas-header p {{
        margin: 0.55rem 0 0 0;
        opacity: 0.96;
        font-size: 1.15rem;
        position: relative;
        z-index: 1;
        text-align: center;
    }}

    .atlas-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 22px;
        padding: 1rem 1.15rem;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }}

    .atlas-note, .atlas-warning, .atlas-success, .atlas-danger {{
        border-radius: 14px;
        padding: 0.9rem 1rem;
        margin: 0.4rem 0 0.9rem 0;
        color: {THEME['text']};
        border-left-width: 6px;
        border-left-style: solid;
    }}

    .atlas-note {{
        border-left-color: {THEME['info_border']};
        background: {THEME['info_bg']};
    }}

    .atlas-warning {{
        border-left-color: {THEME['warning_border']};
        background: {THEME['warning_bg']};
    }}

    .atlas-success {{
        border-left-color: {THEME['success_border']};
        background: {THEME['success_bg']};
    }}

    .atlas-danger {{
        border-left-color: {THEME['danger_border']};
        background: {THEME['danger_bg']};
    }}

    .atlas-pill {{
        display:inline-block;
        padding:0.28rem 0.8rem;
        margin:0.15rem 0.28rem 0.15rem 0;
        border-radius:999px;
        font-size:0.84rem;
        font-weight:700;
        border:1px solid transparent;
    }}

    .atlas-subtle {{
        color: {THEME['muted']};
        font-size: 0.92rem;
    }}

    div[data-baseweb="tab-list"] {{
        gap: 0.5rem;
        margin-bottom: 0.6rem;
    }}

    div[data-baseweb="tab-list"] button[role="tab"] {{
        border-radius: 16px !important;
        padding: 0.72rem 1.05rem !important;
        border: 1px solid {THEME['border']} !important;
        background: #ffffff !important;
        color: {THEME['text']} !important;
        font-weight: 700 !important;
    }}

    div[data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: #ffffff !important;
        border: 1px solid transparent !important;
        box-shadow: 0 6px 14px rgba(79, 70, 229, 0.18);
    }}

    div[data-baseweb="tab-list"] button[aria-selected="true"]:nth-child(1) {{
        background: {THEME['tab_clinical']} !important;
    }}

    div[data-baseweb="tab-list"] button[aria-selected="true"]:nth-child(2) {{
        background: {THEME['tab_education']} !important;
    }}

    .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        color: white !important;
        background: {THEME['button_primary']} !important;
        box-shadow: 0 6px 14px rgba(31, 111, 178, 0.16);
    }}

    .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
        background: {THEME['button_primary_hover']} !important;
    }}

    div[data-testid="stSidebar"] .stButton > button,
    div[data-testid="stSidebar"] .stDownloadButton > button,
    div[data-testid="stSidebar"] .stFormSubmitButton > button {{
        background: {THEME['button_secondary']} !important;
        box-shadow: 0 6px 14px rgba(15, 118, 110, 0.16);
    }}

    div[data-testid="stSidebar"] .stButton > button:hover,
    div[data-testid="stSidebar"] .stDownloadButton > button:hover,
    div[data-testid="stSidebar"] .stFormSubmitButton > button:hover {{
        background: {THEME['button_secondary_hover']} !important;
    }}

    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        border-radius: 12px !important;
        border: 1px solid {THEME['border']} !important;
        background: #ffffff !important;
    }}

    .atlas-section-bar {{
        background: linear-gradient(90deg, #23618f, #2f7bb3);
        color: white;
        border-radius: 18px 18px 0 0;
        padding: 1rem 1.2rem;
        margin: -1rem -1.15rem 1rem -1.15rem;
        font-size: 1.15rem;
        font-weight: 800;
    }}

    .atlas-legend {{
        background: white;
        border: 1px solid {THEME['border']};
        border-radius: 18px;
        padding: 0.95rem 1.1rem;
        margin-bottom: 1rem;
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.04);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class ReliabilityNote:
    label: str
    text: str


@dataclass
class ProcessEntry:
    name: str
    aliases: List[str]
    short_definition: str
    typical_targets: List[str]
    common_outputs: List[str]
    system_effect: str
    clinical_significance: str
    educational_exploration: Dict[str, List[str] | str]
    cautions: List[str] = field(default_factory=list)
    reliability_notes: List[ReliabilityNote] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    visible_tags: List[str] = field(default_factory=list)
    filter_tags: List[str] = field(default_factory=list)


@dataclass
class Observation:
    id: str
    category: str
    target: str
    realization: str
    target_format: str
    realization_format: str
    context: str
    notes: str
    significance: str
    created_at: str


OBSERVATION_TYPE_HELP = {
    "Speech pattern": "Use this when you are recording a recurring phonological pattern or a likely process shown by one or more productions.",
    "Contrast impact": "Use this when the key issue is loss or reduction of a phonemic contrast, even if you are not yet naming a process.",
    "Intelligibility": "Use this when the observation is mainly about how understandable the child is to listeners.",
    "Context / task effect": "Use this when performance changes across word position, task type, prompting, repetition, or speech context.",
    "Developmental consideration": "Use this when you want to note age-related interpretation, persistence, or whether a pattern may need cautious developmental judgement.",
    "Other": "Use this for observations that matter clinically but do not fit neatly into the other categories."
}


PROCESS_DB: List[ProcessEntry] = [
    ProcessEntry(
        name="Velar Fronting",
        aliases=["fronting of velars", "velar to alveolar", "velar to coronal"],
        short_definition="Target velars may be realised as more anterior outputs, often coronal or alveolar sounds.",
        typical_targets=["/k/", "/g/", "/ŋ/"],
        common_outputs=["/t/", "/d/", "/n/"],
        system_effect="May reduce or neutralise the velar–coronal place contrast in affected contexts.",
        clinical_significance="Can affect intelligibility and may be relevant when analysing whether a child is maintaining place contrasts across the wider phonological system.",
        educational_exploration={
            "What to notice": [
                "Is the pattern consistent across words, or limited to certain lexical items?",
                "Does it affect both voiceless and voiced velars?",
                "Is the contrast lost across the system, or only in specific contexts?",
                "Do adult listeners lose meaningful distinctions because of the pattern?",
            ],
            "How to think about it": [
                "Describe the surface pattern first.",
                "Then ask what contrast may be reduced.",
                "Avoid jumping straight from the pattern to a claim about the underlying deficit.",
            ],
            "Developmental interpretation": "This pattern is commonly described in child phonology, but interpretation should depend on age, frequency, severity, intelligibility impact, dialect, multilingual background, and the child’s wider profile.",
        },
        cautions=[
            "Do not assume that every perceived alveolar output reflects a fully neutralised adult-like alveolar category.",
            "Do not treat the pattern alone as proof of a specific motor, phonological, or cognitive explanation.",
            "Do not treat developmental expectations as fixed rules across all children and language backgrounds.",
        ],
        reliability_notes=[
            ReliabilityNote("Confidence", "High as a descriptive system-map concept when phrased cautiously."),
            ReliabilityNote("Boundary", "Moderate for developmental interpretation unless contextual factors are explicitly considered."),
        ],
        examples=["key → tea", "car → tar", "go → doe"],
        visible_tags=["place contrast", "common pattern"],
        filter_tags=["place contrast", "common pattern", "system map", "education"],
    ),
    ProcessEntry(
        name="Final Consonant Deletion",
        aliases=["FCD", "omission of final consonants"],
        short_definition="Word-final consonants may be omitted, reducing syllable or word shape complexity.",
        typical_targets=["word-final singleton consonants"],
        common_outputs=["CV forms", "open syllable outputs"],
        system_effect="May reduce multiple final contrasts and can make many lexical items less distinct from one another.",
        clinical_significance="Can have a marked impact on intelligibility because grammatical and lexical distinctions may be obscured.",
        educational_exploration={
            "What to notice": [
                "Is deletion affecting many final consonants or only a subset?",
                "Are there exceptions in high-frequency or rehearsed words?",
                "Does deletion interact with cluster reduction or weak syllable deletion?",
            ],
            "How to think about it": [
                "Consider the system-wide effect on lexical contrast.",
                "Check whether morphological endings are also affected.",
                "Look at connected speech as well as single words.",
            ],
            "Developmental interpretation": "This pattern is often discussed in developmental and clinical phonology, but conclusions should be made cautiously and in context rather than from one age threshold alone.",
        },
        cautions=[
            "Do not assume all omissions are phonological in origin without considering task, attention, and connected-speech context.",
            "Do not reduce the analysis to a single age cut-off.",
        ],
        reliability_notes=[
            ReliabilityNote("Confidence", "High for describing word-shape consequences."),
            ReliabilityNote("Boundary", "Moderate for inferring severity without wider sampling."),
        ],
        examples=["dog → do", "bus → bu", "cat → ca"],
        visible_tags=["word shape", "intelligibility"],
        filter_tags=["word shape", "intelligibility", "system map", "education"],
    ),
    ProcessEntry(
        name="Cluster Reduction",
        aliases=["consonant cluster reduction", "CCR"],
        short_definition="One or more consonants in a cluster may be omitted, simplifying syllable structure.",
        typical_targets=["word-initial clusters", "word-final clusters"],
        common_outputs=["singleton consonants"],
        system_effect="May reduce distinctions involving manner, place, or morphological marking, depending on which element is omitted.",
        clinical_significance="Can affect intelligibility and may interact with other patterns, so analysis should consider which cluster elements are retained and in what contexts.",
        educational_exploration={
            "What to notice": [
                "Which consonant is retained?",
                "Does the retained element vary by cluster type?",
                "Does the pattern affect morphology, such as plural or tense marking?",
            ],
            "How to think about it": [
                "Describe retained-versus-omitted elements, not just that a cluster is simplified.",
                "Ask whether the simplification is broad or structure-specific.",
            ],
            "Developmental interpretation": "Cluster simplification is widely described in child speech, but the significance of persistence depends on context, severity, and the child’s broader phonological profile.",
        },
        cautions=[
            "Avoid treating all cluster reductions as equivalent; retained elements matter.",
            "Avoid making therapy recommendations from the pattern name alone.",
        ],
        reliability_notes=[
            ReliabilityNote("Confidence", "High for structural description; moderate for interpretation without deeper context."),
        ],
        examples=["spoon → poon", "blue → bu", "nest → nes"],
        visible_tags=["syllable structure", "morphology"],
        filter_tags=["syllable structure", "morphology", "system map", "education"],
    ),
    ProcessEntry(
        name="Weak Syllable Deletion",
        aliases=["unstressed syllable deletion"],
        short_definition="An unstressed syllable may be omitted, reducing word-shape complexity.",
        typical_targets=["multisyllabic words with weak syllables"],
        common_outputs=["shorter word forms"],
        system_effect="May alter prosodic shape and obscure lexical identity, especially in longer words.",
        clinical_significance="Can affect intelligibility and lexical access in connected speech and single-word tasks.",
        educational_exploration={
            "What to notice": [
                "Is the omitted syllable consistently unstressed?",
                "Does the child preserve the stressed syllable?",
                "Does the pattern affect specific word shapes more than others?",
            ],
            "How to think about it": [
                "Consider prosodic structure, not just segmental accuracy.",
                "Compare performance across known and less familiar words.",
            ],
            "Developmental interpretation": "Prosodic simplification may occur in early development, but significance depends on persistence, frequency, and broader speech profile.",
        },
        cautions=[
            "Do not interpret one shortened form in isolation as a stable pattern.",
            "Check whether task familiarity or memory load may also contribute.",
        ],
        reliability_notes=[ReliabilityNote("Confidence", "Moderate to high when based on repeated multisyllabic examples.")],
        examples=["banana → nana", "potato → tato"],
        visible_tags=["prosody", "word shape"],
        filter_tags=["prosody", "word shape", "system map", "education"],
    ),
    ProcessEntry(
        name="Stopping",
        aliases=["fricative stopping", "affricate stopping"],
        short_definition="Fricatives or affricates may be realised as stops, reducing continuant contrast.",
        typical_targets=["/s/ /z/ /f/ /v/ /ʃ/ /tʃ/ /dʒ/"],
        common_outputs=["/t/ /d/ /p/ /b/"],
        system_effect="May reduce manner contrasts between continuants and stops in affected contexts.",
        clinical_significance="Can affect intelligibility and may obscure multiple consonant distinctions across the system.",
        educational_exploration={
            "What to notice": [
                "Which target classes are affected: fricatives, affricates, or both?",
                "Is the output place stable or variable?",
                "Does the pattern occur in all word positions?",
            ],
            "How to think about it": [
                "Track both manner and place.",
                "Separate surface pattern description from explanations about motor control or phonological representation.",
            ],
            "Developmental interpretation": "Some stopping patterns are commonly described in child speech, but interpretation should remain context-sensitive.",
        },
        cautions=["Do not assume all stop substitutions belong to one single pattern without checking target class."],
        reliability_notes=[ReliabilityNote("Confidence", "High for contrast-based description; moderate for interpretation without position sampling.")],
        examples=["see → tea", "fish → pit"],
        visible_tags=["manner contrast"],
        filter_tags=["manner contrast", "system map", "education"],
    ),
    ProcessEntry(
        name="Gliding",
        aliases=["liquid gliding"],
        short_definition="Liquids may be realised as glides, often reducing liquid–glide contrast.",
        typical_targets=["/r/ /l/"],
        common_outputs=["/w/ /j/"],
        system_effect="May reduce contrast involving liquids, especially in word-initial and cluster contexts.",
        clinical_significance="Can affect intelligibility, though some substitutions may remain more interpretable than others.",
        educational_exploration={
            "What to notice": [
                "Does the child substitute both /r/ and /l/?",
                "Is the pattern stable across positions?",
                "How does it interact with clusters?",
            ],
            "How to think about it": [
                "Track the target class carefully.",
                "Check whether the pattern changes across word structures.",
            ],
            "Developmental interpretation": "Liquid simplification is often discussed in child speech, but persistence and impact should be interpreted in context.",
        },
        cautions=["Avoid overgeneralising from a small set of familiar words."],
        reliability_notes=[ReliabilityNote("Confidence", "High for description when liquid targets are clearly sampled.")],
        examples=["rabbit → wabbit", "look → yook"],
        visible_tags=["manner contrast", "liquids"],
        filter_tags=["manner contrast", "liquids", "system map", "education"],
    ),
    ProcessEntry(
        name="Deaffrication",
        aliases=["affricate simplification"],
        short_definition="Affricates may be realised as fricatives or stops, reducing affricate contrast.",
        typical_targets=["/tʃ/ /dʒ/"],
        common_outputs=["/ʃ/ /ʒ/ /t/ /d/"],
        system_effect="May reduce the affricate category and alter manner distinctions.",
        clinical_significance="Can affect intelligibility and may interact with other manner-based patterns.",
        educational_exploration={
            "What to notice": [
                "Are both affricates affected?",
                "Is the output typically fricative-like or stop-like?",
                "Does it co-occur with stopping?",
            ],
            "How to think about it": [
                "Do not collapse all outputs into one explanation too quickly.",
                "Track whether the affricate release is preserved or lost.",
            ],
            "Developmental interpretation": "Interpretation should consider wider manner contrasts and not just isolated words.",
        },
        cautions=["Check whether broad transcription is hiding finer phonetic detail."],
        reliability_notes=[ReliabilityNote("Confidence", "Moderate to high depending on transcription detail.")],
        examples=["chair → share", "jam → zam"],
        visible_tags=["manner contrast", "affricates"],
        filter_tags=["manner contrast", "affricates", "system map", "education"],
    ),
    ProcessEntry(
        name="Backing",
        aliases=["alveolar backing", "front to back"],
        short_definition="More anterior targets may be realised as posterior outputs, reducing place contrast in the opposite direction to fronting.",
        typical_targets=["alveolars or other anterior consonants"],
        common_outputs=["velars or palatals"],
        system_effect="May reduce or reorganise place contrasts across the system.",
        clinical_significance="Less common in many child datasets, so repeated examples may deserve particularly careful analysis.",
        educational_exploration={
            "What to notice": [
                "Is the pattern stable or idiosyncratic?",
                "Are multiple anterior targets affected?",
                "Does the pattern appear in one position or across positions?",
            ],
            "How to think about it": [
                "Check carefully before deciding that backing is present.",
                "Repeated examples matter more than striking isolated tokens.",
            ],
            "Developmental interpretation": "Because this may be less common than some other patterns, cautious interpretation is especially important.",
        },
        cautions=["Avoid overcalling backing from one or two unusual productions."],
        reliability_notes=[ReliabilityNote("Confidence", "Moderate; repeated consistent evidence is especially important.")],
        examples=["tea → key"],
        visible_tags=["place contrast"],
        filter_tags=["place contrast", "system map", "education"],
    ),
]

PROCESS_LOOKUP = {entry.name.lower(): entry for entry in PROCESS_DB}
for entry in PROCESS_DB:
    for alias in entry.aliases:
        PROCESS_LOOKUP[alias.lower()] = entry

HEDGING_RULES = [
    "Prefer ‘may’, ‘can’, ‘often’, and ‘in affected contexts’ over absolute claims.",
    "Describe the observed pattern before suggesting interpretation.",
    "Separate descriptive content from developmental or clinical inference.",
    "Treat developmental expectations as context-sensitive rather than fixed laws.",
    "Avoid implying that one pattern proves a specific underlying deficit.",
]

RED_FLAG_PHRASES = [
    "always means",
    "proves that",
    "definitely indicates",
    "is abnormal after",
    "normal until",
    "shows the child cannot",
    "must be",
]

ANALYSIS_THRESHOLD = 3
ROMAN_HELP = [
    "Use one simple sound-like spelling, not ordinary English spelling.",
    "Write what the child said, not what the word should look like in English orthography.",
    "Recommended convention: sh, ch, ng, th, zh, ee, oo, ah, aw, uh, oy, eye, ow.",
    "Examples: cat → tat, key → tea, chair → share, rabbit → wabbit, banana → nana.",
    "Try to keep one symbol sequence for one sound across entries.",
]

# ============================================================
# SESSION STATE
# ============================================================

if "observations" not in st.session_state:
    st.session_state.observations = []
if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False
if "edit_observation_id" not in st.session_state:
    st.session_state.edit_observation_id = None
if "case_age" not in st.session_state:
    st.session_state.case_age = "3;0"

# ============================================================
# PHONOLOGY HELPERS
# ============================================================

IPA_MULTI = ["tʃ", "dʒ", "aɪ", "eɪ", "oʊ", "əʊ", "aʊ", "ɔɪ", "iː", "uː", "ɔː", "ɑː", "ɜː"]
ROMAN_MULTI = ["tch", "dge", "ch", "sh", "th", "ng", "zh", "ee", "oo", "ah", "aw", "uh", "oy", "eye", "ow"]
ROMAN_REPLACEMENTS = [
    ("tch", "tʃ"),
    ("ch", "tʃ"),
    ("dge", "dʒ"),
    ("j", "dʒ"),
    ("sh", "ʃ"),
    ("zh", "ʒ"),
    ("th", "θ"),
    ("ng", "ŋ"),
    ("ee", "iː"),
    ("oo", "uː"),
    ("ah", "ɑː"),
    ("aw", "ɔː"),
    ("uh", "ʌ"),
    ("oy", "ɔɪ"),
    ("eye", "aɪ"),
    ("ow", "aʊ"),
    ("y", "j"),
    ("c", "k"),
    ("q", "k"),
    ("x", "ks"),
]

CLASS_MAP = {
    "k": {"place": "velar", "manner": "stop", "voice": "voiceless", "class": "consonant"},
    "g": {"place": "velar", "manner": "stop", "voice": "voiced", "class": "consonant"},
    "ŋ": {"place": "velar", "manner": "nasal", "voice": "voiced", "class": "consonant"},
    "t": {"place": "alveolar", "manner": "stop", "voice": "voiceless", "class": "consonant"},
    "d": {"place": "alveolar", "manner": "stop", "voice": "voiced", "class": "consonant"},
    "n": {"place": "alveolar", "manner": "nasal", "voice": "voiced", "class": "consonant"},
    "s": {"place": "alveolar", "manner": "fricative", "voice": "voiceless", "class": "consonant"},
    "z": {"place": "alveolar", "manner": "fricative", "voice": "voiced", "class": "consonant"},
    "l": {"place": "alveolar", "manner": "liquid", "voice": "voiced", "class": "consonant"},
    "r": {"place": "alveolar", "manner": "liquid", "voice": "voiced", "class": "consonant"},
    "ɹ": {"place": "alveolar", "manner": "liquid", "voice": "voiced", "class": "consonant"},
    "w": {"place": "labial-velar", "manner": "glide", "voice": "voiced", "class": "consonant"},
    "j": {"place": "palatal", "manner": "glide", "voice": "voiced", "class": "consonant"},
    "p": {"place": "bilabial", "manner": "stop", "voice": "voiceless", "class": "consonant"},
    "b": {"place": "bilabial", "manner": "stop", "voice": "voiced", "class": "consonant"},
    "m": {"place": "bilabial", "manner": "nasal", "voice": "voiced", "class": "consonant"},
    "f": {"place": "labiodental", "manner": "fricative", "voice": "voiceless", "class": "consonant"},
    "v": {"place": "labiodental", "manner": "fricative", "voice": "voiced", "class": "consonant"},
    "ʃ": {"place": "postalveolar", "manner": "fricative", "voice": "voiceless", "class": "consonant"},
    "ʒ": {"place": "postalveolar", "manner": "fricative", "voice": "voiced", "class": "consonant"},
    "h": {"place": "glottal", "manner": "fricative", "voice": "voiceless", "class": "consonant"},
    "θ": {"place": "dental", "manner": "fricative", "voice": "voiceless", "class": "consonant"},
    "ð": {"place": "dental", "manner": "fricative", "voice": "voiced", "class": "consonant"},
    "tʃ": {"place": "postalveolar", "manner": "affricate", "voice": "voiceless", "class": "consonant"},
    "dʒ": {"place": "postalveolar", "manner": "affricate", "voice": "voiced", "class": "consonant"},
}

VOWELS = {"a", "e", "i", "o", "u", "ə", "ɪ", "ʊ", "ɛ", "æ", "ɔ", "ɑ", "ɒ", "ʌ", "ɜ", "iː", "uː", "ɔː", "ɑː", "ɜː", "aɪ", "eɪ", "oʊ", "əʊ", "aʊ", "ɔɪ"}

# ============================================================
# HELPERS
# ============================================================

def pill(text: str, tone: str = "blue"):
    tones = {
        "blue": (THEME["chip_blue_bg"], THEME["chip_blue_fg"]),
        "green": (THEME["chip_green_bg"], THEME["chip_green_fg"]),
        "purple": (THEME["chip_purple_bg"], THEME["chip_purple_fg"]),
        "amber": (THEME["chip_amber_bg"], THEME["chip_amber_fg"]),
        "red": (THEME["chip_red_bg"], THEME["chip_red_fg"]),
    }
    bg, fg = tones.get(tone, tones["blue"])
    st.markdown(f"<span class='atlas-pill' style='background:{bg};color:{fg};'>{text}</span>", unsafe_allow_html=True)


def render_header():
    st.markdown(
        """
        <div class="atlas-header">
            <h1>Decision Atlas</h1>
            <p>Structured clinical reasoning and education with cautious, reliability-aware language.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def legend_row():
    st.markdown("<div class='atlas-legend'>", unsafe_allow_html=True)
    pill("Clinical Reasoning", "blue")
    pill("Education", "green")
    pill("Pattern evidence", "amber")
    pill("Needs review", "red")
    st.markdown("<div class='atlas-subtle' style='margin-top:0.5rem;'>Colours now mirror the calmer blue–green style from your screenshot more closely.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def card_start(title: Optional[str] = None, section_bar: bool = False):
    st.markdown("<div class='atlas-card'>", unsafe_allow_html=True)
    if title:
        if section_bar:
            st.markdown(f"<div class='atlas-section-bar'>{title}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"### {title}")


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def info_box(text: str, kind: str = "info"):
    classes = {"info": "atlas-note", "warning": "atlas-warning", "success": "atlas-success", "danger": "atlas-danger"}
    st.markdown(f"<div class='{classes.get(kind, 'atlas-note')}'>{text}</div>", unsafe_allow_html=True)


def reliability_scan(text: str) -> List[str]:
    lowered = text.lower()
    return [f"Potential overclaim detected: '{phrase}'" for phrase in RED_FLAG_PHRASES if phrase in lowered]


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\[\]/,;:(){}]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def roman_to_soundlike(text: str) -> str:
    working = normalize_text(text).replace(" ", "")
    for src, tgt in ROMAN_REPLACEMENTS:
        working = working.replace(src, tgt)
    return working


def tokenise_phonology(text: str, fmt: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []
    working = text.replace(" ", "") if fmt == "IPA" else roman_to_soundlike(text)
    tokens = []
    i = 0
    while i < len(working):
        matched = False
        for chunk in sorted(IPA_MULTI, key=len, reverse=True):
            if working[i:i+len(chunk)] == chunk:
                tokens.append(chunk)
                i += len(chunk)
                matched = True
                break
        if matched:
            continue
        tokens.append(working[i])
        i += 1
    return [t for t in tokens if t]


def token_features(token: Optional[str]) -> Dict[str, str]:
    if not token:
        return {"class": "none", "manner": "none", "place": "none", "voice": "none"}
    if token in CLASS_MAP:
        return CLASS_MAP[token]
    if token in VOWELS or re.fullmatch(r"[aeiou]", token):
        return {"class": "vowel", "manner": "vowel", "place": "vowel", "voice": "voiced"}
    return {"class": "unknown", "manner": "unknown", "place": "unknown", "voice": "unknown"}


def first_consonant(tokens: List[str]) -> Optional[str]:
    for t in tokens:
        if token_features(t).get("class") == "consonant":
            return t
    return None


def final_consonant(tokens: List[str]) -> Optional[str]:
    for t in reversed(tokens):
        if token_features(t).get("class") == "consonant":
            return t
    return None


def initial_cluster(tokens: List[str]) -> List[str]:
    cluster = []
    for t in tokens:
        features = token_features(t)
        if features.get("class") == "consonant":
            cluster.append(t)
        elif cluster or features.get("class") == "vowel":
            break
    return cluster


def final_cluster(tokens: List[str]) -> List[str]:
    cluster = []
    for t in reversed(tokens):
        features = token_features(t)
        if features.get("class") == "consonant":
            cluster.insert(0, t)
        elif cluster or features.get("class") == "vowel":
            break
    return cluster


def syllable_count_estimate(tokens: List[str]) -> int:
    return max(0, sum(1 for t in tokens if token_features(t).get("class") == "vowel"))


def observation_to_dict(obs: Observation) -> Dict:
    return asdict(obs)


def dict_to_observation(d: Dict) -> Observation:
    return Observation(
        id=d.get("id", str(uuid.uuid4())),
        category=d.get("category", "Other"),
        target=d.get("target", ""),
        realization=d.get("realization", ""),
        target_format=d.get("target_format", "Approximation / Roman"),
        realization_format=d.get("realization_format", "Approximation / Roman"),
        context=d.get("context", ""),
        notes=d.get("notes", ""),
        significance=d.get("significance", ""),
        created_at=d.get("created_at", datetime.utcnow().isoformat()),
    )


def add_or_update_observation(obs: Observation):
    for i, item in enumerate(st.session_state.observations):
        if item.id == obs.id:
            st.session_state.observations[i] = obs
            return
    st.session_state.observations.append(obs)


def get_observation_by_id(obs_id: Optional[str]) -> Optional[Observation]:
    if not obs_id:
        return None
    for obs in st.session_state.observations:
        if obs.id == obs_id:
            return obs
    return None


def delete_observation(obs_id: str):
    st.session_state.observations = [obs for obs in st.session_state.observations if obs.id != obs_id]
    if st.session_state.edit_observation_id == obs_id:
        st.session_state.edit_observation_id = None


def observation_count() -> int:
    return len(st.session_state.observations)


def ready_for_analysis() -> bool:
    return observation_count() >= ANALYSIS_THRESHOLD


def update_case_age(new_age: str):
    st.session_state.case_age = new_age.strip()


def confidence_label(score: int) -> str:
    if score >= 5:
        return "strong repeated evidence"
    if score >= 3:
        return "moderate repeated evidence"
    return "tentative evidence"


def parsed_representation(text: str, fmt: str) -> str:
    if not text.strip():
        return ""
    return " ".join(tokenise_phonology(text, fmt))


def compare_parse(obs: Observation) -> Dict:
    target_tokens = tokenise_phonology(obs.target, obs.target_format)
    real_tokens = tokenise_phonology(obs.realization, obs.realization_format)
    target_first = first_consonant(target_tokens)
    real_first = first_consonant(real_tokens)
    target_last = final_consonant(target_tokens)
    real_last = final_consonant(real_tokens)
    target_init_cluster = initial_cluster(target_tokens)
    real_init_cluster = initial_cluster(real_tokens)

    notes = []
    if obs.target_format == "Approximation / Roman":
        notes.append(f"Target parsed as: {' '.join(target_tokens) if target_tokens else '—'}")
    if obs.realization_format == "Approximation / Roman":
        notes.append(f"Realisation parsed as: {' '.join(real_tokens) if real_tokens else '—'}")
    if not target_tokens or not real_tokens:
        notes.append("One side could not be parsed clearly.")
    if obs.target_format == "Approximation / Roman" or obs.realization_format == "Approximation / Roman":
        notes.append("Roman input uses the app mini-convention, not ordinary spelling.")

    flags = []
    if obs.target_format == "Approximation / Roman" and obs.target.lower() == obs.realization.lower():
        flags.append("Target and realisation are identical in Roman input. Check that the child form was entered separately.")
    if target_first and real_first and target_first == real_first:
        flags.append("Initial consonant looks preserved by the parser.")
    if target_last and real_last and target_last == real_last:
        flags.append("Final consonant looks preserved by the parser.")
    if len(target_init_cluster) >= 2 and len(real_init_cluster) < len(target_init_cluster):
        flags.append("Initial cluster appears simplified in parsing.")

    return {
        "target_tokens": target_tokens,
        "real_tokens": real_tokens,
        "target_first": target_first,
        "real_first": real_first,
        "target_last": target_last,
        "real_last": real_last,
        "notes": notes,
        "flags": flags,
    }


def detect_patterns(obs: Observation) -> List[Tuple[str, str]]:
    parse = compare_parse(obs)
    target_tokens = parse["target_tokens"]
    real_tokens = parse["real_tokens"]
    if not target_tokens or not real_tokens:
        return []

    findings = []
    target_first = parse["target_first"]
    real_first = parse["real_first"]
    target_last = parse["target_last"]
    real_last = parse["real_last"]
    tf = token_features(target_first)
    rf = token_features(real_first)
    tlf = token_features(target_last)
    rlf = token_features(real_last)
    target_init_cluster = initial_cluster(target_tokens)
    real_init_cluster = initial_cluster(real_tokens)
    target_final_cluster = final_cluster(target_tokens)
    real_final_cluster = final_cluster(real_tokens)

    if target_first and real_first:
        if tf.get("place") == "velar" and rf.get("place") in {"alveolar", "dental", "postalveolar"}:
            findings.append(("Velar Fronting", f"Initial target {target_first} was realised as more anterior {real_first}."))
        if tf.get("place") in {"alveolar", "dental"} and rf.get("place") == "velar":
            findings.append(("Backing", f"Initial target {target_first} was realised as more posterior {real_first}."))
        if tf.get("manner") in {"fricative", "affricate"} and rf.get("manner") == "stop":
            findings.append(("Stopping", f"Initial continuant/affricate target {target_first} was realised as stop {real_first}."))
        if tf.get("manner") == "affricate" and rf.get("manner") in {"fricative", "stop"}:
            findings.append(("Deaffrication", f"Affricate target {target_first} lost affricate structure in realisation {real_first}."))
        if tf.get("manner") == "liquid" and rf.get("manner") == "glide":
            findings.append(("Gliding", f"Liquid target {target_first} was realised as glide {real_first}."))

    if target_last and not real_last:
        findings.append(("Final Consonant Deletion", f"The target ended in consonant {target_last}, but no final consonant was preserved in the realisation."))
    elif target_last and real_last and tlf.get("class") == "consonant" and rlf.get("class") != "consonant":
        findings.append(("Final Consonant Deletion", f"The target ended in consonant {target_last}, but the realisation did not preserve a final consonant."))

    if len(target_init_cluster) >= 2 and len(real_init_cluster) < len(target_init_cluster):
        findings.append(("Cluster Reduction", f"The initial cluster {''.join(target_init_cluster)} was simplified to {''.join(real_init_cluster) or 'Ø'}."))
    if len(target_final_cluster) >= 2 and len(real_final_cluster) < len(target_final_cluster):
        findings.append(("Cluster Reduction", f"The final cluster {''.join(target_final_cluster)} was simplified to {''.join(real_final_cluster) or 'Ø'}."))

    target_syllables = syllable_count_estimate(target_tokens)
    real_syllables = syllable_count_estimate(real_tokens)
    if target_syllables >= 2 and real_syllables < target_syllables:
        findings.append(("Weak Syllable Deletion", f"The realisation appears shorter prosodically ({target_syllables} syllable estimate → {real_syllables})."))

    notes_blob = f"{obs.notes} {obs.significance} {obs.context}".lower()
    if "intelligib" in notes_blob:
        findings.append(("Intelligibility impact", "The notes explicitly mention intelligibility consequences."))
    if "contrast" in notes_blob:
        findings.append(("Contrast concern", "The notes explicitly mention reduced or lost contrast."))

    return findings


def build_analysis_summary() -> Dict:
    evidence_by_pattern = defaultdict(list)
    category_counter = Counter()
    contexts = []
    all_findings = []
    child_age = st.session_state.case_age.strip() or "Not set"

    for obs in st.session_state.observations:
        category_counter[obs.category] += 1
        if obs.context.strip():
            contexts.append(obs.context.strip())
        findings = detect_patterns(obs)
        all_findings.extend(findings)
        for pattern, explanation in findings:
            evidence_by_pattern[pattern].append({
                "observation_id": obs.id,
                "target": obs.target,
                "realization": obs.realization,
                "explanation": explanation,
                "notes": obs.notes,
            })

    ranked_patterns = [
        {"pattern": pattern, "count": len(items), "confidence": confidence_label(len(items)), "evidence": items}
        for pattern, items in evidence_by_pattern.items()
    ]
    ranked_patterns.sort(key=lambda x: x["count"], reverse=True)

    return {
        "child_age": child_age,
        "category_counter": category_counter,
        "contexts": contexts,
        "ranked_patterns": ranked_patterns,
        "reasoning": [
            "The summary below stays descriptive first and inferential second.",
            f"Current age input: {child_age}. Developmental interpretation should be read through that age setting and updated if the age changes.",
            "Repeated target–realisation relationships are weighted more heavily than isolated striking examples.",
            "Approximation / Roman inputs are accepted through an explicit mini-convention, not through ordinary English spelling.",
            "This remains a working analysis and should be checked against broader sampling, position effects, and intelligibility impact.",
        ],
        "next_questions": [
            "Are the same contrasts reduced across multiple lexical items?",
            "Is the pattern stable across positions, tasks, and levels of support?",
            "Does the pattern affect intelligibility enough to change priority?",
            "Would broader sampling strengthen or weaken the current interpretation?",
        ],
        "all_findings_count": len(all_findings),
    }


def export_observations_json() -> str:
    payload = {
        "app": "Decision Atlas",
        "version": "1.1",
        "exported_at": datetime.utcnow().isoformat(),
        "observations": [observation_to_dict(obs) for obs in st.session_state.observations],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def import_observations_from_json(uploaded_text: str, mode: str = "merge") -> Tuple[bool, str]:
    try:
        data = json.loads(uploaded_text)
    except json.JSONDecodeError:
        return False, "The uploaded file is not valid JSON."
    incoming = data.get("observations") if isinstance(data, dict) else data
    if not isinstance(incoming, list):
        return False, "The JSON did not contain an observations list."
    imported = [dict_to_observation(item) for item in incoming if isinstance(item, dict)]
    if mode == "replace":
        st.session_state.observations = imported
    else:
        existing_ids = {obs.id for obs in st.session_state.observations}
        for obs in imported:
            if obs.id in existing_ids:
                obs.id = str(uuid.uuid4())
            st.session_state.observations.append(obs)
    st.session_state.analysis_requested = False
    st.session_state.edit_observation_id = None
    return True, f"Imported {len(imported)} observation(s)."


def render_process_entry(entry: ProcessEntry):
    st.subheader(entry.name)
    st.write(entry.short_definition)
    for tag in entry.visible_tags:
        pill(tag, "blue" if tag not in {"affricates", "liquids"} else "purple")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Typical targets**")
        for item in entry.typical_targets:
            st.write(f"- {item}")
        st.markdown("**Common outputs**")
        for item in entry.common_outputs:
            st.write(f"- {item}")
        st.markdown("**System effect**")
        st.write(entry.system_effect)
    with c2:
        st.markdown("**Clinical significance**")
        st.write(entry.clinical_significance)
        st.markdown("**Examples**")
        for ex in entry.examples:
            st.write(f"- {ex}")
        st.markdown("**Reliability notes**")
        for note in entry.reliability_notes:
            st.write(f"- **{note.label}:** {note.text}")

    st.markdown("### Educational Exploration")
    for key, value in entry.educational_exploration.items():
        st.markdown(f"**{key}**")
        if isinstance(value, list):
            for item in value:
                st.write(f"- {item}")
        else:
            st.write(value)

    with st.expander("Cautions and boundaries"):
        for item in entry.cautions:
            st.write(f"- {item}")

# ============================================================
# UI
# ============================================================

render_header()
legend_row()

with st.sidebar:
    st.markdown("## Atlas controls")
    st.write("This build separates clinical reasoning from educational content and keeps the language intentionally cautious.")

    st.markdown("### Case metadata")
    with st.form("age_update_form"):
        sidebar_age = st.text_input("Child age", value=st.session_state.case_age, placeholder="e.g. 3;0 or 8;3")
        age_updated = st.form_submit_button("Update age")
        if age_updated:
            update_case_age(sidebar_age)
            st.session_state.analysis_requested = False
            st.success("Age updated. The analysis will now use the new age setting.")
            st.rerun()

    if st.button("Clear all observations"):
        st.session_state.observations = []
        st.session_state.analysis_requested = False
        st.session_state.edit_observation_id = None
        st.rerun()

    st.markdown("---")
    st.markdown("### Export / import")
    st.download_button("Export observations as JSON", data=export_observations_json(), file_name="decision_atlas_observations.json", mime="application/json")
    uploaded = st.file_uploader("Import observations JSON", type=["json"])
    import_mode = st.radio("Import mode", ["merge", "replace"], horizontal=True)
    if uploaded is not None and st.button("Run import"):
        success, message = import_observations_from_json(uploaded.getvalue().decode("utf-8"), mode=import_mode)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

    st.markdown("---")
    st.markdown("### Roman mini-convention")
    for rule in ROMAN_HELP:
        st.write(f"- {rule}")

    st.markdown("---")
    st.markdown("### Reliability commitments")
    for rule in HEDGING_RULES:
        st.write(f"- {rule}")

clinical_tab, education_tab = st.tabs(["Clinical Reasoning", "Education"])

with clinical_tab:
    st.markdown(f"**Current child age:** {st.session_state.case_age}")
    left, right = st.columns([1.02, 1.25])

    with left:
        card_start("Input & Observations", section_bar=True)
        st.write("Add target–realisation pairs, contextual notes, and significance statements before moving into analysis.")
        info_box("You can enter the target and the realisation in <strong>IPA</strong> or in <strong>Approximation / Roman</strong>. Roman entries use the app’s mini-convention rather than ordinary English spelling.", "info")

        editing_obs = get_observation_by_id(st.session_state.edit_observation_id)
        categories = ["Speech pattern", "Contrast impact", "Intelligibility", "Context / task effect", "Developmental consideration", "Other"]

        with st.form("observation_form", clear_on_submit=editing_obs is None):
            category = st.selectbox("Observation type", categories, index=categories.index(editing_obs.category) if editing_obs and editing_obs.category in categories else 0)
            st.caption(OBSERVATION_TYPE_HELP.get(category, ""))
            c1, c2 = st.columns(2)
            with c1:
                target = st.text_input("Target", value=editing_obs.target if editing_obs else "", placeholder="e.g. /kæt/ or kat")
                target_format = st.selectbox("Target format", ["IPA", "Approximation / Roman"], index=0 if editing_obs and editing_obs.target_format == "IPA" else 1)
            with c2:
                realization = st.text_input("Realisation", value=editing_obs.realization if editing_obs else "", placeholder="e.g. /tæt/ or tat")
                realization_format = st.selectbox("Realisation format", ["IPA", "Approximation / Roman"], index=0 if editing_obs and editing_obs.realization_format == "IPA" else 1)

            context = st.text_input("Context / position / task", value=editing_obs.context if editing_obs else "", placeholder="e.g. word-initial, single-word naming, spontaneous speech")
            notes = st.text_area("Observation notes", value=editing_obs.notes if editing_obs else "", placeholder="Describe what was observed, including consistency, contrast effects, or variability.", height=100)
            significance = st.text_area("Why this may matter", value=editing_obs.significance if editing_obs else "", placeholder="e.g. This may reduce the velar–coronal place contrast and affect intelligibility.", height=90)

            save_label = "Update observation" if editing_obs else "Add observation"
            submitted = st.form_submit_button(save_label)
            if submitted:
                if target.strip() and realization.strip():
                    add_or_update_observation(Observation(
                        id=editing_obs.id if editing_obs else str(uuid.uuid4()),
                        category=category,
                        target=target.strip(),
                        realization=realization.strip(),
                        target_format=target_format,
                        realization_format=realization_format,
                        context=context.strip(),
                        notes=notes.strip(),
                        significance=significance.strip(),
                        created_at=editing_obs.created_at if editing_obs else datetime.utcnow().isoformat(),
                    ))
                    st.session_state.analysis_requested = False
                    st.session_state.edit_observation_id = None
                    st.rerun()
                else:
                    st.error("Please enter both a target and a realisation.")

        if editing_obs and st.button("Cancel editing"):
            st.session_state.edit_observation_id = None
            st.rerun()

        if not st.session_state.observations:
            info_box("<strong>No observations yet.</strong> Use the form above to add observations.", "info")

        if not ready_for_analysis():
            needed = ANALYSIS_THRESHOLD - observation_count()
            info_box(f"<strong>Not enough observations to build a reliable analysis.</strong><br>You currently have {observation_count()} observation(s). Add {needed} more to unlock a fuller reasoning summary.", "warning")
        else:
            info_box("<strong>Enough observations to begin a cautious analysis.</strong><br>Check analysis now or continue adding observations to strengthen the pattern picture.", "success")

        st.markdown("### Observation log")
        if st.session_state.observations:
            for idx, obs in enumerate(st.session_state.observations, start=1):
                with st.expander(f"Observation {idx}: {obs.target} → {obs.realization}"):
                    st.write(f"**Type:** {obs.category}")
                    st.write(f"**Target:** {obs.target} ({obs.target_format})")
                    st.write(f"**Realisation:** {obs.realization} ({obs.realization_format})")
                    if obs.context:
                        st.write(f"**Context:** {obs.context}")
                    if obs.notes:
                        st.write(f"**Notes:** {obs.notes}")
                    if obs.significance:
                        st.write(f"**Why it may matter:** {obs.significance}")
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("Edit", key=f"edit_{obs.id}"):
                            st.session_state.edit_observation_id = obs.id
                            st.rerun()
                    with b2:
                        if st.button("Delete entry", key=f"delete_{obs.id}"):
                            delete_observation(obs.id)
                            st.rerun()
        card_end()

    with right:
        card_start("Analysis & Reasoning", section_bar=True)
        st.write("This section uses repeated target–realisation relationships, not only keyword matching.")

        st.markdown("### Parse check table")
        if st.session_state.observations:
            comparison_rows = []
            for obs in st.session_state.observations:
                parse = compare_parse(obs)
                comparison_rows.append({
                    "Target": obs.target,
                    "Target fmt": obs.target_format.replace("Approximation / Roman", "Approx/Roman"),
                    "Parsed target": " ".join(parse["target_tokens"]) if parse["target_tokens"] else "—",
                    "Realisation": obs.realization,
                    "Realisation fmt": obs.realization_format.replace("Approximation / Roman", "Approx/Roman"),
                    "Parsed realisation": " ".join(parse["real_tokens"]) if parse["real_tokens"] else "—",
                    "Initial C": f"{parse['target_first'] or '—'} → {parse['real_first'] or '—'}",
                    "Final C": f"{parse['target_last'] or '—'} → {parse['real_last'] or '—'}",
                    "Flags": " | ".join(parse["flags"]) if parse["flags"] else "—",
                })
            st.dataframe(comparison_rows, use_container_width=True, hide_index=True)
            info_box("Use this table to check how the app parsed each pair before trusting the analysis below.", "info")

            a1, a2 = st.columns(2)
            with a1:
                if st.button("Check analysis now"):
                    st.session_state.analysis_requested = True
            with a2:
                if st.button("Continue adding observations"):
                    st.session_state.analysis_requested = False
        else:
            info_box("Add observations to populate the parse check table.", "info")

        if not ready_for_analysis():
            info_box("There are not yet enough observations to build a reliable analysis summary. Keep collecting observations across pattern, contrast, intelligibility, and context.", "warning")
        elif st.session_state.analysis_requested:
            summary = build_analysis_summary()
            info_box("This is a cautious working analysis. It is designed to support reasoning, not replace full assessment or judgement.", "info")
            st.markdown("### Overview")
            pill(f"Age: {summary['child_age']}", "purple")
            pill(f"Observations: {observation_count()}", "blue")
            pill(f"Detected evidence items: {summary['all_findings_count']}", "green")
            if summary["contexts"]:
                pill(f"Contexts noted: {len(summary['contexts'])}", "purple")

            st.markdown("### Category spread")
            for category, count in summary["category_counter"].most_common():
                st.write(f"- **{category}:** {count}")

            st.markdown("### Pattern candidates")
            if summary["ranked_patterns"]:
                for item in summary["ranked_patterns"]:
                    with st.expander(f"{item['pattern']} — {item['confidence']} ({item['count']} evidence item(s))", expanded=item['count'] >= 3):
                        for ev in item["evidence"]:
                            st.write(f"- **{ev['target']} → {ev['realization']}**: {ev['explanation']}")
                            if ev["notes"]:
                                st.caption(ev["notes"])
            else:
                info_box("No clear process candidate was detected automatically from the current target–realisation pairs. That may mean the dataset is too small, too mixed, or not well captured by the current rule set.", "warning")

            st.markdown("### Reasoning frame")
            for line in summary["reasoning"]:
                st.write(f"- {line}")
            st.markdown("### Next questions")
            for q in summary["next_questions"]:
                st.write(f"- {q}")
        else:
            info_box("Ready when you are. Once enough observations are present, choose ‘Check analysis now’ to generate a cautious working summary.", "info")
        card_end()

with education_tab:
    edu_left, edu_right = st.columns([1.15, 1])
    with edu_left:
        card_start("System Map", section_bar=True)
        all_filter_tags = sorted({tag for entry in PROCESS_DB for tag in entry.filter_tags})
        query = st.text_input("Search process", placeholder="Try: velar fronting, FCD, cluster reduction")
        selected_tags = st.multiselect("Filter by theme", all_filter_tags)
        filtered = PROCESS_DB
        if query.strip():
            q = query.strip().lower()
            filtered = [entry for entry in filtered if q in entry.name.lower() or any(q in alias.lower() for alias in entry.aliases) or q in entry.short_definition.lower() or any(q in tag.lower() for tag in entry.filter_tags)]
        if selected_tags:
            filtered = [entry for entry in filtered if all(tag in entry.filter_tags for tag in selected_tags)]
        st.write(f"Showing {len(filtered)} pattern(s).")
        if filtered:
            for entry in filtered:
                with st.container(border=True):
                    render_process_entry(entry)
        else:
            info_box("No matching process found. Try a broader search term.", "warning")
        card_end()

    with edu_right:
        card_start("Educational Exploration", section_bar=True)
        st.write("Use this section to practise thinking carefully without turning heuristics into rigid rules.")
        st.markdown("### Roman input guide")
        for rule in ROMAN_HELP:
            st.write(f"- {rule}")

        st.markdown("### Reflection prompts")
        prompts = [
            "What is the observed pattern, purely descriptively?",
            "Which phonemic contrast may be reduced or neutralised?",
            "Is the issue segment-specific, class-wide, structural, or context-bound?",
            "What evidence would still be needed before making a developmental or clinical judgement?",
            "How might dialect, multilingual exposure, lexical familiarity, and task demands change interpretation?",
        ]
        for p in prompts:
            st.write(f"- {p}")

        st.markdown("### Overclaim detector")
        user_text = st.text_area("Paste an explanation to check whether it sounds too absolute", placeholder="Example: Velar fronting always means the child cannot produce velars.", height=130)
        if user_text.strip():
            findings = reliability_scan(user_text)
            if findings:
                info_box("This wording may be too strong or too absolute.", "danger")
                for item in findings:
                    st.write(f"- {item}")
                st.markdown("**Safer direction**")
                st.write("Try rewriting the statement so it separates observation from interpretation and uses context-sensitive wording such as ‘may’, ‘can’, or ‘often’.")
            else:
                info_box("No obvious red-flag overclaims detected in the wording you pasted.", "success")
                st.write("That does not guarantee correctness, but the phrasing does not immediately look overly absolute.")

        st.markdown("### Example contrast")
        st.markdown("**Overstated**")
        st.write("Velar fronting means the child cannot produce velars and is abnormal after a certain age.")
        st.markdown("**More reliable educational wording**")
        st.write("Velar fronting describes a pattern in which target velars may be realised as more anterior outputs. Its significance depends on age, consistency, intelligibility impact, linguistic background, and the child’s wider phonological system.")
        card_end()
