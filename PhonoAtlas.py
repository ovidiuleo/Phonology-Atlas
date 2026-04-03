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
    "header_bg": "linear-gradient(90deg, #1f3c88 0%, #4f46e5 55%, #7c3aed 100%)",
    "header_text": "#ffffff",
    "surface": "#ffffff",
    "surface_alt": "#f8fafc",
    "border": "#dbe4f0",
    "text": "#1f2937",
    "muted": "#5b6472",
    "tab_clinical": "#2563eb",
    "tab_education": "#7c3aed",
    "button_primary": "#2563eb",
    "button_primary_hover": "#1d4ed8",
    "button_secondary": "#7c3aed",
    "button_secondary_hover": "#6d28d9",
    "success_bg": "#ecfdf5",
    "success_border": "#10b981",
    "warning_bg": "#fff7ed",
    "warning_border": "#f59e0b",
    "danger_bg": "#fef2f2",
    "danger_border": "#ef4444",
    "info_bg": "#eff6ff",
    "info_border": "#3b82f6",
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {THEME['surface_alt']};
        color: {THEME['text']};
    }}

    .atlas-header {{
        position: sticky;
        top: 0;
        z-index: 999;
        background: {THEME['header_bg']};
        color: {THEME['header_text']};
        padding: 1rem 1.25rem;
        border-radius: 0 0 18px 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15);
        margin-bottom: 1rem;
    }}

    .atlas-header h1 {{
        margin: 0;
        font-size: 1.8rem;
        line-height: 1.1;
    }}

    .atlas-header p {{
        margin: 0.35rem 0 0 0;
        opacity: 0.95;
        font-size: 0.98rem;
    }}

    .atlas-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
        margin-bottom: 1rem;
    }}

    .atlas-note {{
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin: 0.5rem 0 1rem 0;
        border-left: 6px solid {THEME['info_border']};
        background: {THEME['info_bg']};
        color: {THEME['text']};
    }}

    .atlas-warning {{
        border-radius: 14px;
        padding: 0.9rem 1rem;
        margin: 0.5rem 0 1rem 0;
        border-left: 6px solid {THEME['warning_border']};
        background: {THEME['warning_bg']};
        color: {THEME['text']};
    }}

    .atlas-success {{
        border-radius: 14px;
        padding: 0.9rem 1rem;
        margin: 0.5rem 0 1rem 0;
        border-left: 6px solid {THEME['success_border']};
        background: {THEME['success_bg']};
        color: {THEME['text']};
    }}

    .atlas-danger {{
        border-radius: 14px;
        padding: 0.9rem 1rem;
        margin: 0.5rem 0 1rem 0;
        border-left: 6px solid {THEME['danger_border']};
        background: {THEME['danger_bg']};
        color: {THEME['text']};
    }}

    .atlas-pill {{
        display:inline-block;
        padding:0.24rem 0.65rem;
        margin:0.15rem 0.28rem 0.15rem 0;
        border-radius:999px;
        font-size:0.82rem;
        font-weight:600;
        border:1px solid transparent;
    }}

    div[data-baseweb="tab-list"] button[role="tab"] {{
        border-radius: 14px !important;
        padding: 0.65rem 1rem !important;
        border: 1px solid {THEME['border']} !important;
        margin-right: 0.35rem;
        background: #ffffff !important;
        color: {THEME['text']} !important;
        font-weight: 600 !important;
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
        font-weight: 600 !important;
        border: none !important;
        color: white !important;
        background: {THEME['button_primary']} !important;
        box-shadow: 0 6px 14px rgba(37, 99, 235, 0.18);
    }}

    .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
        background: {THEME['button_primary_hover']} !important;
    }}

    div[data-testid="stSidebar"] .stButton > button,
    div[data-testid="stSidebar"] .stDownloadButton > button,
    div[data-testid="stSidebar"] .stFormSubmitButton > button {{
        background: {THEME['button_secondary']} !important;
        box-shadow: 0 6px 14px rgba(124, 58, 237, 0.18);
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
    tags: List[str] = field(default_factory=list)


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
        tags=["place contrast", "common pattern", "system map", "education"],
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
        tags=["word shape", "intelligibility", "system map", "education"],
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
        tags=["syllable structure", "morphology", "system map", "education"],
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
        tags=["prosody", "word shape", "system map", "education"],
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
        tags=["manner contrast", "system map", "education"],
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
        tags=["manner contrast", "liquids", "system map", "education"],
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
        tags=["manner contrast", "affricates", "system map", "education"],
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
        tags=["place contrast", "system map", "education"],
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

# ============================================================
# SESSION STATE
# ============================================================

if "observations" not in st.session_state:
    st.session_state.observations = []
if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False
if "edit_observation_id" not in st.session_state:
    st.session_state.edit_observation_id = None

# ============================================================
# PHONOLOGY HELPERS
# ============================================================

IPA_MULTI = ["tʃ", "dʒ", "aɪ", "eɪ", "oʊ", "əʊ", "aʊ", "ɔɪ", "iː", "uː", "ɔː", "ɑː", "ɜː"]
ROMAN_MULTI = ["tch", "dge", "ch", "sh", "th", "ng", "ph", "wh", "ee", "oo"]

CLASS_MAP = {
    "k": {"place": "velar", "manner": "stop", "voice": "voiceless", "class": "consonant"},
    "g": {"place": "velar", "manner": "stop", "voice": "voiced", "class": "consonant"},
    "ŋ": {"place": "velar", "manner": "nasal", "voice": "voiced", "class": "consonant"},
    "ng": {"place": "velar", "manner": "nasal", "voice": "voiced", "class": "consonant"},
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
    "ch": {"place": "postalveolar", "manner": "affricate", "voice": "voiceless", "class": "consonant"},
    "sh": {"place": "postalveolar", "manner": "fricative", "voice": "voiceless", "class": "consonant"},
    "zh": {"place": "postalveolar", "manner": "fricative", "voice": "voiced", "class": "consonant"},
    "y": {"place": "palatal", "manner": "glide", "voice": "voiced", "class": "consonant"},
}

VOWELS = set(list("aeiouəɪʊɛæɔɑɒʌɜo") + ["iː", "uː", "ɔː", "ɑː", "ɜː", "aɪ", "eɪ", "oʊ", "əʊ", "aʊ", "ɔɪ"])

ROMAN_EQUIV = {
    "c": "k",
    "q": "k",
    "x": "ks",
    "ng": "ng",
    "ch": "ch",
    "sh": "sh",
    "j": "dʒ",
    "y": "j",
}


# ============================================================
# GENERAL HELPERS
# ============================================================

def pill(text: str, tone: str = "blue"):
    tones = {
        "blue": ("#dbeafe", "#1d4ed8"),
        "purple": ("#ede9fe", "#6d28d9"),
        "green": ("#dcfce7", "#166534"),
        "amber": ("#fef3c7", "#92400e"),
        "red": ("#fee2e2", "#991b1b"),
    }
    bg, fg = tones.get(tone, tones["blue"])
    st.markdown(
        f"<span class='atlas-pill' style='background:{bg};color:{fg};'>{text}</span>",
        unsafe_allow_html=True,
    )


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


def card_start(title: Optional[str] = None):
    st.markdown("<div class='atlas-card'>", unsafe_allow_html=True)
    if title:
        st.markdown(f"### {title}")


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def info_box(text: str, kind: str = "info"):
    classes = {
        "info": "atlas-note",
        "warning": "atlas-warning",
        "success": "atlas-success",
        "danger": "atlas-danger",
    }
    cls = classes.get(kind, "atlas-note")
    st.markdown(f"<div class='{cls}'>{text}</div>", unsafe_allow_html=True)


def reliability_scan(text: str) -> List[str]:
    findings = []
    lowered = text.lower()
    for phrase in RED_FLAG_PHRASES:
        if phrase in lowered:
            findings.append(f"Potential overclaim detected: '{phrase}'")
    return findings


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\[\]/,;:(){}]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenise_phonology(text: str, fmt: str) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []

    if fmt == "IPA":
        working = text.replace(" ", "")
        tokens = []
        i = 0
        while i < len(working):
            matched = False
            for chunk in sorted(IPA_MULTI, key=len, reverse=True):
                if working[i:i + len(chunk)] == chunk:
                    tokens.append(chunk)
                    i += len(chunk)
                    matched = True
                    break
            if matched:
                continue
            tokens.append(working[i])
            i += 1
        return [t for t in tokens if t]

    working = text.replace(" ", "")
    for src, tgt in ROMAN_EQUIV.items():
        working = working.replace(src, tgt)
    tokens = []
    i = 0
    while i < len(working):
        matched = False
        for chunk in sorted(ROMAN_MULTI + list(ROMAN_EQUIV.values()), key=len, reverse=True):
            if working[i:i + len(chunk)] == chunk:
                tokens.append(chunk)
                i += len(chunk)
                matched = True
                break
        if matched:
            continue
        tokens.append(working[i])
        i += 1
    return [t for t in tokens if t]


def token_features(token: str) -> Dict[str, str]:
    if token in CLASS_MAP:
        return CLASS_MAP[token]
    if token in VOWELS or re.fullmatch(r"[aeiou]", token):
        return {"class": "vowel", "manner": "vowel", "place": "vowel", "voice": "voiced"}
    return {"class": "unknown", "manner": "unknown", "place": "unknown", "voice": "unknown"}


def consonants_only(tokens: List[str]) -> List[str]:
    return [t for t in tokens if token_features(t).get("class") == "consonant"]


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
        if token_features(t).get("class") == "consonant":
            cluster.append(t)
        elif cluster:
            break
        elif token_features(t).get("class") == "vowel":
            break
    return cluster


def final_cluster(tokens: List[str]) -> List[str]:
    cluster = []
    for t in reversed(tokens):
        if token_features(t).get("class") == "consonant":
            cluster.insert(0, t)
        elif cluster:
            break
        elif token_features(t).get("class") == "vowel":
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
    existing_idx = next((i for i, item in enumerate(st.session_state.observations) if item.id == obs.id), None)
    if existing_idx is None:
        st.session_state.observations.append(obs)
    else:
        st.session_state.observations[existing_idx] = obs


def get_observation_by_id(obs_id: str) -> Optional[Observation]:
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


def confidence_label(score: int) -> str:
    if score >= 5:
        return "strong repeated evidence"
    if score >= 3:
        return "moderate repeated evidence"
    return "tentative evidence"


def detect_patterns(obs: Observation) -> List[Tuple[str, str]]:
    target_tokens = tokenise_phonology(obs.target, obs.target_format)
    real_tokens = tokenise_phonology(obs.realization, obs.realization_format)
    if not target_tokens or not real_tokens:
        return []

    findings = []
    target_first = first_consonant(target_tokens)
    real_first = first_consonant(real_tokens)
    target_last = final_consonant(target_tokens)
    real_last = final_consonant(real_tokens)
    target_init_cluster = initial_cluster(target_tokens)
    real_init_cluster = initial_cluster(real_tokens)
    target_final_cluster = final_cluster(target_tokens)
    real_final_cluster = final_cluster(real_tokens)

    tf = token_features(target_first) if target_first else {}
    rf = token_features(real_first) if real_first else {}
    tlf = token_features(target_last) if target_last else {}
    rlf = token_features(real_last) if real_last else {}

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

    for obs in st.session_state.observations:
        category_counter[obs.category] += 1
        if obs.context.strip():
            contexts.append(obs.context.strip())
        findings = detect_patterns(obs)
        all_findings.extend(findings)
        for pattern, explanation in findings:
            evidence_by_pattern[pattern].append(
                {
                    "observation_id": obs.id,
                    "target": obs.target,
                    "realization": obs.realization,
                    "explanation": explanation,
                    "notes": obs.notes,
                }
            )

    ranked_patterns = []
    for pattern, items in evidence_by_pattern.items():
        ranked_patterns.append(
            {
                "pattern": pattern,
                "count": len(items),
                "confidence": confidence_label(len(items)),
                "evidence": items,
            }
        )
    ranked_patterns.sort(key=lambda x: x["count"], reverse=True)

    reasoning_lines = [
        "The summary below stays descriptive first and inferential second.",
        "Repeated target–realisation relationships are weighted more heavily than isolated striking examples.",
        "Approximate Roman inputs are accepted, but IPA entries usually allow cleaner pattern detection.",
        "This remains a working analysis and should be checked against broader sampling, position effects, and intelligibility impact.",
    ]

    next_questions = [
        "Are the same contrasts reduced across multiple lexical items?",
        "Is the pattern stable across positions, tasks, and levels of support?",
        "Does the pattern affect intelligibility enough to change priority?",
        "Would broader sampling strengthen or weaken the current interpretation?",
    ]

    return {
        "category_counter": category_counter,
        "contexts": contexts,
        "ranked_patterns": ranked_patterns,
        "reasoning": reasoning_lines,
        "next_questions": next_questions,
        "all_findings_count": len(all_findings),
    }


def export_observations_json() -> str:
    payload = {
        "app": "Decision Atlas",
        "version": "1.0",
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
    for tag in entry.tags:
        pill(tag, "purple" if tag in {"education", "system map"} else "blue")

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

with st.sidebar:
    st.markdown("## Atlas controls")
    st.write("This build separates clinical reasoning from educational content and keeps the language intentionally cautious.")

    if st.button("Clear all observations"):
        st.session_state.observations = []
        st.session_state.analysis_requested = False
        st.session_state.edit_observation_id = None
        st.rerun()

    st.markdown("---")
    st.markdown("### Export / import")
    st.download_button(
        "Export observations as JSON",
        data=export_observations_json(),
        file_name="decision_atlas_observations.json",
        mime="application/json",
    )
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
    st.markdown("### Reliability commitments")
    for rule in HEDGING_RULES:
        st.write(f"- {rule}")

clinical_tab, education_tab = st.tabs(["Clinical Reasoning", "Education"])

with clinical_tab:
    left, right = st.columns([1.1, 1.2])

    with left:
        card_start("Input & Observations")
        st.write("Add target–realisation pairs, contextual notes, and significance statements before moving into analysis.")
        info_box(
            "You can enter the target and the realisation in <strong>IPA</strong> or in <strong>Approximation / Roman</strong>. The app will try to interpret both, but IPA will usually support more precise matching.",
            "info",
        )

        editing_obs = get_observation_by_id(st.session_state.edit_observation_id) if st.session_state.edit_observation_id else None

        with st.form("observation_form", clear_on_submit=editing_obs is None):
            category = st.selectbox(
                "Observation type",
                [
                    "Speech pattern",
                    "Contrast impact",
                    "Intelligibility",
                    "Context / task effect",
                    "Developmental consideration",
                    "Other",
                ],
                index=[
                    "Speech pattern",
                    "Contrast impact",
                    "Intelligibility",
                    "Context / task effect",
                    "Developmental consideration",
                    "Other",
                ].index(editing_obs.category) if editing_obs else 0,
            )

            c1, c2 = st.columns(2)
            with c1:
                target = st.text_input("Target", value=editing_obs.target if editing_obs else "", placeholder="e.g. /kæt/ or cat")
                target_format = st.selectbox(
                    "Target format",
                    ["IPA", "Approximation / Roman"],
                    index=0 if editing_obs and editing_obs.target_format == "IPA" else 1 if editing_obs else 1,
                )
            with c2:
                realization = st.text_input("Realisation", value=editing_obs.realization if editing_obs else "", placeholder="e.g. /tæt/ or tat")
                realization_format = st.selectbox(
                    "Realisation format",
                    ["IPA", "Approximation / Roman"],
                    index=0 if editing_obs and editing_obs.realization_format == "IPA" else 1 if editing_obs else 1,
                )

            context = st.text_input(
                "Context / position / task",
                value=editing_obs.context if editing_obs else "",
                placeholder="e.g. word-initial, single-word naming, spontaneous speech",
            )
            notes = st.text_area(
                "Observation notes",
                value=editing_obs.notes if editing_obs else "",
                placeholder="Describe what was observed, including consistency, contrast effects, or variability.",
                height=110,
            )
            significance = st.text_area(
                "Why this may matter",
                value=editing_obs.significance if editing_obs else "",
                placeholder="e.g. This may reduce the velar–coronal place contrast and affect intelligibility.",
                height=100,
            )

            save_label = "Update observation" if editing_obs else "Add observation"
            submitted = st.form_submit_button(save_label)
            if submitted:
                if target.strip() and realization.strip():
                    new_obs = Observation(
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
                    )
                    add_or_update_observation(new_obs)
                    st.session_state.analysis_requested = False
                    st.session_state.edit_observation_id = None
                    st.success("Observation saved.")
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
            info_box(
                f"<strong>Not enough observations to build a reliable analysis.</strong><br>You currently have {observation_count()} observation(s). Add {needed} more to unlock a fuller reasoning summary.",
                "warning",
            )
        else:
            info_box(
                "<strong>Enough observations to begin a cautious analysis.</strong><br>Check analysis now or continue adding observations to strengthen the pattern picture.",
                "success",
            )

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
                        if st.button("Delete", key=f"delete_{obs.id}"):
                            delete_observation(obs.id)
                            st.rerun()
        card_end()

    with right:
        card_start("Analysis & Reasoning")
        st.write("This section uses repeated target–realisation relationships, not only keyword matching.")
        a1, a2 = st.columns(2)
        with a1:
            if st.button("Check analysis now"):
                st.session_state.analysis_requested = True
        with a2:
            if st.button("Continue adding observations"):
                st.session_state.analysis_requested = False

        if not ready_for_analysis():
            info_box(
                "There are not yet enough observations to build a reliable analysis summary. Keep collecting observations across pattern, contrast, intelligibility, and context.",
                "warning",
            )
        elif st.session_state.analysis_requested:
            summary = build_analysis_summary()
            info_box(
                "This is a cautious working analysis. It is designed to support reasoning, not replace full assessment or judgement.",
                "info",
            )

            st.markdown("### Overview")
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
            info_box(
                "Ready when you are. Once enough observations are present, choose ‘Check analysis now’ to generate a cautious working summary.",
                "info",
            )
        card_end()

with education_tab:
    edu_left, edu_right = st.columns([1.15, 1])

    with edu_left:
        card_start("System Map")
        query = st.text_input("Search process", placeholder="Try: velar fronting, FCD, cluster reduction")
        selected_tags = st.multiselect("Filter by theme", sorted({tag for entry in PROCESS_DB for tag in entry.tags}))

        filtered = PROCESS_DB
        if query.strip():
            q = query.strip().lower()
            filtered = [
                entry for entry in filtered
                if q in entry.name.lower()
                or any(q in alias.lower() for alias in entry.aliases)
                or q in entry.short_definition.lower()
                or any(q in tag.lower() for tag in entry.tags)
            ]
        if selected_tags:
            filtered = [entry for entry in filtered if all(tag in entry.tags for tag in selected_tags)]

        st.write(f"Showing {len(filtered)} pattern(s).")
        if filtered:
            for entry in filtered:
                with st.container(border=True):
                    render_process_entry(entry)
        else:
            info_box("No matching process found. Try a broader search term.", "warning")
        card_end()

    with edu_right:
        card_start("Educational Exploration")
        st.write("Use this section to practise thinking carefully without turning heuristics into rigid rules.")

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
        user_text = st.text_area(
            "Paste an explanation to check whether it sounds too absolute",
            placeholder="Example: Velar fronting always means the child cannot produce velars.",
            height=140,
        )
        if user_text.strip():
            findings = reliability_scan(user_text)
            if findings:
                info_box("This wording may be too strong or too absolute.", "danger")
                for item in findings:
                    st.write(f"- {item}")
                st.markdown("**Safer direction**")
                st.write("Try rewriting the statement so it separates observation from interpretation and uses context-sensitive wording such as ‘may’, ‘can’, or ‘often’. ")
            else:
                info_box("No obvious red-flag overclaims detected in the wording you pasted.", "success")
                st.write("That does not guarantee correctness, but the phrasing does not immediately look overly absolute.")

        st.markdown("### Example contrast")
        st.markdown("**Overstated**")
        st.write("Velar fronting means the child cannot produce velars and is abnormal after a certain age.")
        st.markdown("**More reliable educational wording**")
        st.write("Velar fronting describes a pattern in which target velars may be realised as more anterior outputs. Its significance depends on age, consistency, intelligibility impact, linguistic background, and the child’s wider phonological system.")
        card_end()
