import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional

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
# CONTENT MODEL
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

if "observations" not in st.session_state:
    st.session_state.observations = []
if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False


# ============================================================
# HELPERS
# ============================================================

def pill(text: str, tone: str = "blue"):
    tones = {
        "blue": ("#dbeafe", "#1d4ed8"),
        "purple": ("#ede9fe", "#6d28d9"),
        "green": ("#dcfce7", "#166534"),
        "amber": ("#fef3c7", "#92400e"),
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


def add_observation(category: str, observation: str, significance: str):
    st.session_state.observations.append(
        {
            "category": category,
            "observation": observation.strip(),
            "significance": significance.strip(),
        }
    )


def observation_count() -> int:
    return len(st.session_state.observations)


def ready_for_analysis() -> bool:
    return observation_count() >= ANALYSIS_THRESHOLD


def build_analysis_summary() -> Dict[str, List[str] | str]:
    observations = st.session_state.observations
    categories = sorted({obs['category'] for obs in observations})
    category_summary = {cat: [] for cat in categories}
    for obs in observations:
        category_summary[obs['category']].append(obs['observation'])

    repeated_terms = []
    text_blob = " ".join(obs["observation"].lower() for obs in observations)
    for entry in PROCESS_DB:
        for keyword in [entry.name.lower(), *[a.lower() for a in entry.aliases]]:
            if keyword in text_blob:
                repeated_terms.append(entry.name)
                break

    if not repeated_terms:
        repeated_terms = ["No direct process label detected from free-text observations yet."]

    reasoning_lines = [
        "The observations are enough to begin a cautious working analysis, but they should still be interpreted in context.",
        "The summary below is descriptive first and inferential second.",
    ]

    return {
        "categories": categories,
        "category_summary": category_summary,
        "possible_patterns": repeated_terms,
        "reasoning": reasoning_lines,
    }


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
# HEADER + SIDEBAR
# ============================================================

render_header()

with st.sidebar:
    st.markdown("## Atlas controls")
    st.write("This build separates clinical reasoning from educational content and keeps the language intentionally cautious.")
    if st.button("Clear all observations"):
        st.session_state.observations = []
        st.session_state.analysis_requested = False
        st.rerun()

    st.markdown("---")
    st.markdown("### Reliability commitments")
    for rule in HEDGING_RULES:
        st.write(f"- {rule}")


# ============================================================
# TABS
# ============================================================

clinical_tab, education_tab = st.tabs(["Clinical Reasoning", "Education"])

with clinical_tab:
    left, right = st.columns([1.05, 1.2])

    with left:
        card_start("Input & Observations")
        st.write("Add structured observations before moving into analysis.")
        with st.form("add_observation_form", clear_on_submit=True):
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
            )
            observation_text = st.text_area(
                "Observation",
                placeholder="Example: Velars are often realised as alveolar outputs in word-initial position.",
                height=120,
            )
            significance_text = st.text_area(
                "Why this may matter",
                placeholder="Example: This may reduce the velar–coronal place contrast across several words.",
                height=100,
            )
            submitted = st.form_submit_button("Add observation")

            if submitted:
                if observation_text.strip():
                    add_observation(category, observation_text, significance_text)
                    st.session_state.analysis_requested = False
                    st.success("Observation added.")
                else:
                    st.error("Please enter an observation before adding it.")

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
                with st.expander(f"Observation {idx}: {obs['category']}"):
                    st.write(f"**Observation:** {obs['observation']}")
                    if obs['significance']:
                        st.write(f"**Why it may matter:** {obs['significance']}")
        card_end()

    with right:
        card_start("Analysis & Reasoning")
        st.write("This section stays descriptive first and interpretive second.")

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
            st.markdown("### Category overview")
            for category in summary["categories"]:
                pill(category, "blue")
                for item in summary["category_summary"][category]:
                    st.write(f"- {item}")

            st.markdown("### Possible pattern links")
            for pattern in summary["possible_patterns"]:
                pill(pattern, "amber")

            st.markdown("### Reasoning frame")
            for line in summary["reasoning"]:
                st.write(f"- {line}")

            st.markdown("### Next questions")
            next_questions = [
                "Is the pattern consistent across positions and words?",
                "Which contrasts appear reduced, and in which contexts?",
                "Is intelligibility impacted enough to prioritise this pattern?",
                "What additional sampling would strengthen or weaken this interpretation?",
            ]
            for q in next_questions:
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
