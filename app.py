import streamlit as st
import pandas as pd

from algorithms.fifo import fifo_page_replacement
from algorithms.lru import lru_page_replacement
from algorithms.optimal import optimal_page_replacement


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VM Lab | Virtual Memory Simulator",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM STREAMLIT THEME
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #07111f;
        }

        .main .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        section[data-testid="stSidebar"] {
            background-color: #091522;
            border-right: 1px solid #1e293b;
        }

        h1, h2, h3 {
            color: #f8fafc !important;
        }

        p, label {
            color: #94a3b8;
        }

        .stMetric {
            background-color: #0d1b2a;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 12px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #0d1b2a;
            border-color: #1e293b;
            border-radius: 14px;
        }

        .stButton > button {
            border-radius: 9px;
            font-weight: 700;
        }

        button[data-baseweb="tab"] {
            font-weight: 700;
        }

        .section-title {
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            color: #22d3ee;
            text-transform: uppercase;
            margin-top: 25px;
        }

        .sequence-box {
            background-color: #0b1726;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 15px;
            font-family: monospace;
            font-size: 1rem;
            color: #67e8f9;
        }

        .footer-text {
            text-align: center;
            color: #475569;
            font-size: 0.7rem;
            margin-top: 35px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def parse_reference_string(value):

    value = value.strip()

    if not value:
        return []

    if " " in value:

        try:
            return [int(x) for x in value.split()]
        except ValueError:
            return []

    if value.isdigit():

        return [int(x) for x in value]

    return []


def calculate_rate(value, total):

    if total == 0:
        return 0

    return (value / total) * 100


def run_algorithm(name, reference_string, frame_count):

    if name == "FIFO":

        return fifo_page_replacement(
            reference_string,
            frame_count
        )

    if name == "LRU":

        return lru_page_replacement(
            reference_string,
            frame_count
        )

    return optimal_page_replacement(
        reference_string,
        frame_count
    )


def create_trace_dataframe(
    reference_string,
    result,
    frame_count
):

    rows = []

    for index in range(len(reference_string)):

        row = {
            "Step": index + 1,
            "Page": reference_string[index]
        }

        frames = result["frame_history"][index]

        for frame_index in range(frame_count):

            if frame_index < len(frames):

                row[f"Frame {frame_index + 1}"] = (
                    frames[frame_index]
                )

            else:

                row[f"Frame {frame_index + 1}"] = "—"

        row["Status"] = result["status"][index]

        rows.append(row)

    return pd.DataFrame(rows)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💾 VM LAB")

    st.caption("OPERATING SYSTEMS LABORATORY")

    st.divider()

    st.subheader("Simulation Control")

    reference_input = st.text_input(
        "Reference String",
        value="7 0 1 2 0 3 0 4",
        help=(
            "Enter pages separated by spaces or use a "
            "compact sequence such as 70120304."
        )
    )

    frame_count = st.number_input(
        "Physical Memory Frames",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    mode = st.selectbox(
        "Analysis Mode",
        [
            "Compare All",
            "FIFO",
            "LRU",
            "Optimal"
        ]
    )

    run_simulation = st.button(
        "▶ RUN SIMULATION",
        use_container_width=True,
        type="primary"
    )

    st.divider()

    st.subheader("Algorithms")

    with st.expander("FIFO"):

        st.write(
            "First-In, First-Out replaces the page "
            "that entered memory first."
        )

    with st.expander("LRU"):

        st.write(
            "Least Recently Used replaces the page "
            "that has not been used recently."
        )

    with st.expander("OPTIMAL"):

        st.write(
            "Optimal replaces the page whose next use "
            "is farthest in the future."
        )

    st.divider()

    st.success("Simulation engine ready")


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1]
)

with header_left:

    st.caption(
        "OPERATING SYSTEMS / MEMORY MANAGEMENT"
    )

    st.title(
        "Virtual Memory Simulator"
    )

    st.write(
        "Explore page replacement decisions, physical "
        "memory states, and algorithm performance."
    )

with header_right:

    st.success("● LIVE ENGINE")


# ============================================================
# VALIDATE INPUT
# ============================================================

reference_string = parse_reference_string(
    reference_input
)


if not reference_string:

    st.warning(
        "Please enter a valid reference string."
    )

    st.info(
        "Examples: `7 0 1 2 0 3 0 4` or `70120304`."
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "simulation_run" not in st.session_state:

    st.session_state.simulation_run = False


if run_simulation:

    st.session_state.simulation_run = True


# ============================================================
# BEFORE SIMULATION
# ============================================================

if not st.session_state.simulation_run:

    st.markdown(
        '<div class="section-title">'
        'Memory Engine'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Simulation Configuration"
    )

    config_columns = st.columns(3)

    with config_columns[0]:

        with st.container(border=True):

            st.metric(
                "REFERENCE PAGES",
                len(reference_string)
            )

            st.caption(
                "Total page requests"
            )

    with config_columns[1]:

        with st.container(border=True):

            st.metric(
                "PHYSICAL FRAMES",
                frame_count
            )

            st.caption(
                "Available memory slots"
            )

    with config_columns[2]:

        with st.container(border=True):

            st.metric(
                "ANALYSIS MODE",
                mode
            )

            st.caption(
                "Selected strategy"
            )

    st.markdown(
        '<div class="section-title">'
        'Execution Timeline'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Page Request Sequence"
    )

    timeline_columns = st.columns(
        len(reference_string)
    )

    for index, page in enumerate(reference_string):

        with timeline_columns[index]:

            with st.container(border=True):

                st.caption(
                    f"STEP {index + 1}"
                )

                st.markdown(
                    f"### {page}"
                )

    st.divider()

    st.info(
        "Memory Engine Ready\n\n"
        "Your virtual memory environment is configured. "
        "Click **RUN SIMULATION** to observe page requests "
        "moving through physical memory."
    )

    st.caption(
        "REFERENCE STREAM  →  FRAME ALLOCATION  "
        "→  PAGE REPLACEMENT"
    )

    st.stop()


# ============================================================
# RUN ALL ALGORITHMS
# ============================================================

all_results = {}

for algorithm in [
    "FIFO",
    "LRU",
    "Optimal"
]:

    all_results[algorithm] = run_algorithm(
        algorithm,
        reference_string,
        frame_count
    )


# ============================================================
# ACTIVE SIMULATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Active Simulation'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Current Reference Stream"
)

st.code(
    " → ".join(
        str(page)
        for page in reference_string
    ),
    language="text"
)


# ============================================================
# SUMMARY
# ============================================================

summary_columns = st.columns(3)

with summary_columns[0]:

    st.metric(
        "REFERENCES",
        len(reference_string)
    )

with summary_columns[1]:

    st.metric(
        "FRAMES",
        frame_count
    )

with summary_columns[2]:

    st.metric(
        "MODE",
        mode
    )


# ============================================================
# ALGORITHM COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Performance Arena'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Algorithm Comparison"
)


fault_counts = {
    algorithm: all_results[algorithm]["page_faults"]
    for algorithm in all_results
}

minimum_faults = min(
    fault_counts.values()
)

best_algorithms = [
    algorithm
    for algorithm, faults in fault_counts.items()
    if faults == minimum_faults
]


comparison_columns = st.columns(3)


for index, algorithm in enumerate(
    ["FIFO", "LRU", "Optimal"]
):

    result = all_results[algorithm]

    faults = result["page_faults"]

    hits = result["page_hits"]

    hit_rate = calculate_rate(
        hits,
        len(reference_string)
    )

    with comparison_columns[index]:

        with st.container(border=True):

            st.subheader(
                algorithm
            )

            if algorithm in best_algorithms:

                st.success(
                    "★ BEST RESULT"
                )

            else:

                st.caption(
                    "PAGE REPLACEMENT ALGORITHM"
                )

            metric_columns = st.columns(2)

            with metric_columns[0]:

                st.metric(
                    "PAGE FAULTS",
                    faults
                )

            with metric_columns[1]:

                st.metric(
                    "PAGE HITS",
                    hits
                )

            st.progress(
                hit_rate / 100
            )

            st.caption(
                f"Hit Rate: {hit_rate:.1f}%"
            )


# ============================================================
# PERFORMANCE LEADER
# ============================================================

if len(best_algorithms) == 1:

    winner_name = best_algorithms[0]

else:

    winner_name = " + ".join(
        best_algorithms
    )


st.success(
    f"🏆 Performance Leader: {winner_name}  |  "
    f"{minimum_faults} page faults across "
    f"{len(reference_string)} references."
)


# ============================================================
# EXECUTION TIMELINE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Execution Timeline'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Page Request Sequence"
)

timeline_columns = st.columns(
    len(reference_string)
)

for index, page in enumerate(reference_string):

    with timeline_columns[index]:

        with st.container(border=True):

            st.caption(
                f"STEP {index + 1}"
            )

            st.markdown(
                f"### {page}"
            )


# ============================================================
# PHYSICAL MEMORY
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Physical Memory'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Memory State Matrix"
)

fifo_tab, lru_tab, optimal_tab = st.tabs(
    [
        "FIFO",
        "LRU",
        "OPTIMAL"
    ]
)


# ============================================================
# FIFO MEMORY
# ============================================================

with fifo_tab:

    st.caption(
        "First-In, First-Out — replace the oldest resident page."
    )

    fifo_result = all_results["FIFO"]

    fifo_table = create_trace_dataframe(
        reference_string,
        fifo_result,
        frame_count
    )

    st.dataframe(
        fifo_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# LRU MEMORY
# ============================================================

with lru_tab:

    st.caption(
        "Least Recently Used — replace the least recently accessed page."
    )

    lru_result = all_results["LRU"]

    lru_table = create_trace_dataframe(
        reference_string,
        lru_result,
        frame_count
    )

    st.dataframe(
        lru_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# OPTIMAL MEMORY
# ============================================================

with optimal_tab:

    st.caption(
        "Optimal — replace the page needed farthest in the future."
    )

    optimal_result = all_results["Optimal"]

    optimal_table = create_trace_dataframe(
        reference_string,
        optimal_result,
        frame_count
    )

    st.dataframe(
        optimal_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# STEP INSPECTOR
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Step Inspector'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Frame-by-Frame Decision Analysis"
)


inspector_algorithm = st.selectbox(
    "Algorithm",
    [
        "FIFO",
        "LRU",
        "Optimal"
    ],
    key="inspector_algorithm"
)


inspector_step = st.slider(
    "Reference Step",
    min_value=1,
    max_value=len(reference_string),
    value=1,
    key="inspector_step"
)


inspector_result = all_results[
    inspector_algorithm
]

step_index = inspector_step - 1

current_page = reference_string[
    step_index
]

current_status = inspector_result[
    "status"
][step_index]

current_frames = inspector_result[
    "frame_history"
][step_index]


inspector_columns = st.columns(3)


with inspector_columns[0]:

    st.metric(
        "CURRENT STEP",
        inspector_step
    )

with inspector_columns[1]:

    st.metric(
        "REQUESTED PAGE",
        current_page
    )

with inspector_columns[2]:

    if current_status == "Hit":

        st.metric(
            "RESULT",
            "HIT"
        )

    else:

        st.metric(
            "RESULT",
            "FAULT"
        )


# ============================================================
# CURRENT MEMORY STATE
# ============================================================

st.subheader(
    "Current Memory State"
)

frame_columns = st.columns(
    frame_count
)


for index in range(frame_count):

    with frame_columns[index]:

        with st.container(border=True):

            st.caption(
                f"FRAME {index + 1}"
            )

            if index < len(current_frames):

                st.markdown(
                    f"## {current_frames[index]}"
                )

                st.success(
                    "OCCUPIED"
                )

            else:

                st.markdown(
                    "## —"
                )

                st.caption(
                    "EMPTY"
                )


# ============================================================
# ALGORITHM INSIGHT
# ============================================================

if current_status == "Hit":

    insight_text = (
        f"Page {current_page} was already present "
        f"in physical memory. No replacement was required."
    )

else:

    if inspector_algorithm == "FIFO":

        insight_text = (
            f"Page {current_page} caused a page fault. "
            f"FIFO replaces the page that entered memory first."
        )

    elif inspector_algorithm == "LRU":

        insight_text = (
            f"Page {current_page} caused a page fault. "
            f"LRU replaces the page that has been used least recently."
        )

    else:

        insight_text = (
            f"Page {current_page} caused a page fault. "
            f"Optimal replaces the page whose next use is "
            f"farthest in the future."
        )


st.info(
    f"💡 **Algorithm Insight**\n\n{insight_text}"
)


# ============================================================
# ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Performance Analysis"
)


analytics_data = []


for algorithm in [
    "FIFO",
    "LRU",
    "Optimal"
]:

    result = all_results[algorithm]

    faults = result["page_faults"]

    hits = result["page_hits"]

    fault_rate = calculate_rate(
        faults,
        len(reference_string)
    )

    hit_rate = calculate_rate(
        hits,
        len(reference_string)
    )

    analytics_data.append(
        {
            "Algorithm": algorithm,
            "Page Faults": faults,
            "Page Hits": hits,
            "Fault Rate": f"{fault_rate:.1f}%",
            "Hit Rate": f"{hit_rate:.1f}%"
        }
    )


analytics_df = pd.DataFrame(
    analytics_data
)


analytics_columns = st.columns(2)


with analytics_columns[0]:

    with st.container(border=True):

        st.markdown(
            "### Page Fault Comparison"
        )

        chart_df = analytics_df.set_index(
            "Algorithm"
        )[
            ["Page Faults", "Page Hits"]
        ]

        st.bar_chart(
            chart_df
        )


with analytics_columns[1]:

    with st.container(border=True):

        st.markdown(
            "### Performance Table"
        )

        st.dataframe(
            analytics_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# DETAILED TRACE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Detailed Trace'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Complete Execution History"
)


for algorithm in [
    "FIFO",
    "LRU",
    "Optimal"
]:

    result = all_results[algorithm]

    faults = result["page_faults"]

    hits = result["page_hits"]

    with st.expander(
        f"{algorithm}  ·  {faults} faults  ·  {hits} hits"
    ):

        trace_df = create_trace_dataframe(
            reference_string,
            result,
            frame_count
        )

        st.dataframe(
            trace_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ALGORITHM REFERENCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Algorithm Reference'
    '</div>',
    unsafe_allow_html=True
)

st.subheader(
    "How Each Strategy Works"
)


reference_columns = st.columns(3)


with reference_columns[0]:

    with st.container(border=True):

        st.markdown(
            "### FIFO"
        )

        st.caption(
            "QUEUE BASED"
        )

        st.write(
            "The page that entered physical memory first "
            "is removed first."
        )


with reference_columns[1]:

    with st.container(border=True):

        st.markdown(
            "### LRU"
        )

        st.caption(
            "RECENCY BASED"
        )

        st.write(
            "The page that has not been accessed for the "
            "longest period is removed."
        )


with reference_columns[2]:

    with st.container(border=True):

        st.markdown(
            "### OPTIMAL"
        )

        st.caption(
            "FUTURE BASED"
        )

        st.write(
            "The page whose next reference occurs farthest "
            "in the future is removed."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "VM LAB · VIRTUAL MEMORY & PAGE REPLACEMENT "
    "ALGORITHM SIMULATOR · OPERATING SYSTEMS PROJECT"
)