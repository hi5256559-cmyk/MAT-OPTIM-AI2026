
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="MAT-OPTIM AI",
    page_icon="⚙️",
    layout="wide"
)

BASE_DIR = Path(__file__).parent

@st.cache_data
def load_csv(filename):
    return pd.read_csv(BASE_DIR / filename)

try:
    materials = load_csv("materials.csv")
    fatigue_data = load_csv("fatigue_data.csv")
except Exception as error:
    st.error("A required CSV file could not be loaded.")
    st.code(str(error))
    st.stop()

st.title("⚙️ MAT-OPTIM AI")
st.subheader("Engineering Materials Selection Platform")

st.warning(
    "Educational prototype. Results are preliminary "
    "and are not certified engineering recommendations."
)

mode = st.sidebar.radio(
    "Choose a section",
    [
        "Simple Mode",
        "Expert Mode",
        "Fatigue Analysis",
        "Materials Database"
    ]
)

if mode == "Simple Mode":

    st.header("Simple Mode")

    problem = st.text_area("Describe your problem:")

    priority = st.selectbox(
        "Main priority",
        [
            "High strength",
            "Low weight",
            "Low cost",
            "Corrosion resistance",
            "Heat resistance"
        ]
    )

    if st.button("Find suitable materials"):

        if not problem.strip():
            st.warning("Describe your problem first.")

        else:
            if priority == "High strength":
                results = materials.sort_values(
                    "Tensile_Strength_MPa",
                    ascending=False
                )

            elif priority == "Low weight":
                results = materials.sort_values(
                    "Density_g_cm3",
                    ascending=True
                )

            elif priority == "Low cost":
                results = materials.sort_values(
                    "Cost_Level",
                    ascending=True
                )

            elif priority == "Corrosion resistance":
                results = materials[
                    materials["Corrosion_Resistance"] == "High"
                ]

            else:
                results = materials[
                    materials["Heat_Resistance"] == "High"
                ]

            st.subheader("Suggested materials")
            st.dataframe(results.head(5))

            st.caption(
                "Suggestions are based on database filtering. "
                "The written problem is not yet interpreted by AI."
            )

elif mode == "Expert Mode":

    st.header("Expert Mode")

    min_strength = st.number_input(
        "Minimum tensile strength (MPa)",
        min_value=0,
        value=100
    )

    max_density = st.number_input(
        "Maximum density (g/cm3)",
        min_value=0.1,
        value=8.0
    )

    results = materials[
        (materials["Tensile_Strength_MPa"] >= min_strength)
        &
        (materials["Density_g_cm3"] <= max_density)
    ]

    st.subheader("Matching materials")
    st.dataframe(results)

    st.write("Number of materials:", len(results))

elif mode == "Fatigue Analysis":

    st.header("Fatigue Analysis")

    st.write(
        "Preliminary fatigue screening using reference values."
    )

    selected = st.selectbox(
        "Choose material",
        fatigue_data["Material"].tolist()
    )

    row = fatigue_data[
        fatigue_data["Material"] == selected
    ].iloc[0]

    stress = st.number_input(
        "Applied stress amplitude (MPa)",
        min_value=0.0,
        value=100.0
    )

    cycles = st.number_input(
        "Required number of cycles",
        min_value=1,
        value=1000000
    )

    limit = float(row["Reference_Endurance_Limit_MPa"])
    reference_cycles = int(row["Reference_Cycles"])

    st.write("Reference endurance limit:", limit, "MPa")

    if st.button("Evaluate fatigue"):

        if stress <= 0:
            st.warning("Enter a stress greater than zero.")

        elif stress > limit:
            st.warning(
                "Applied stress exceeds the reference endurance limit. "
                "Further fatigue analysis is required."
            )

        elif cycles >= reference_cycles:
            st.success(
                "Preliminary screening: stress is below the "
                "reference endurance limit."
            )

        else:
            st.info(
                "A material-specific S-N curve is needed "
                "for a reliable fatigue life estimate."
            )

    st.caption(
        "Reference values are illustrative placeholders, "
        "not certified design values. This section does not "
        "predict fatigue life."
    )

    st.subheader("Fatigue reference data")
    st.dataframe(fatigue_data)

elif mode == "Materials Database":

    st.header("Materials Database")

    st.dataframe(materials)

    st.write("Total materials:", len(materials))

    st.download_button(
        "Download database",
        materials.to_csv(index=False).encode("utf-8"),
        "materials.csv",
        "text/csv"
    )

st.divider()

st.caption(
    "MAT-OPTIM AI | Engineering Materials Platform"
)
