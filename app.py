import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="MAT-OPTIM AI",
    page_icon="⚙️",
    layout="wide"
)

@st.cache_data
def load_materials():
    file_path = Path(__file__).parent / "materials.csv"
    return pd.read_csv(file_path)

try:
    materials = load_materials()
except Exception as error:
    st.error("Unable to load materials.csv")
    st.code(str(error))
    st.stop()

st.title("⚙️ MAT-OPTIM AI")
st.subheader("Intelligent Material Selection and Optimization Platform")
st.write(
    "A platform that helps engineers, technicians and non-specialists "
    "select suitable engineering materials."
)
st.divider()

mode = st.sidebar.radio(
    "Choose your mode",
    ["Simple Mode", "Expert Mode", "Materials Database"]
)

if mode == "Simple Mode":
    st.header("🔍 Simple Mode")
    st.write("Describe your problem and receive material suggestions.")

    problem = st.text_area(
        "Describe your problem:",
        placeholder="Example: I need a lightweight and strong material..."
    )

    priority = st.selectbox(
        "What is your main priority?",
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
            st.warning("Please describe your problem first.")
        else:
            st.info(
                "Your description has been received. "
                "Suggestions are based on the selected priority."
            )

            if priority == "High strength":
                results = materials.sort_values(
                    by="Tensile_Strength_MPa", ascending=False
                )
            elif priority == "Low weight":
                results = materials.sort_values(
                    by="Density_g_cm3", ascending=True
                )
            elif priority == "Low cost":
                results = materials.sort_values(
                    by="Cost_Level", ascending=True
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
            st.dataframe(results.head(5), use_container_width=True)
            st.caption(
                "These are preliminary database-based suggestions, "
                "not a certified engineering recommendation."
            )

elif mode == "Expert Mode":
    st.header("🧑‍🔬 Expert Mode")
    st.write("Filter materials according to engineering requirements.")

    min_strength = st.number_input(
        "Minimum tensile strength (MPa)", min_value=0, value=100
    )
    max_density = st.number_input(
        "Maximum density (g/cm³)", min_value=0.1, value=8.0
    )

    results = materials[
        (materials["Tensile_Strength_MPa"] >= min_strength)
        & (materials["Density_g_cm3"] <= max_density)
    ]

    st.subheader("Matching materials")
    st.dataframe(results, use_container_width=True)
    st.write("Number of matching materials:", len(results))

elif mode == "Materials Database":
    st.header("📚 Materials Database")
    st.dataframe(materials, use_container_width=True)
    st.write("Total number of materials:", len(materials))

    st.download_button(
        label="Download materials database",
        data=materials.to_csv(index=False).encode("utf-8"),
        file_name="materials.csv",
        mime="text/csv"
    )

st.divider()
st.caption("MAT-OPTIM AI | Engineering Materials Selection Platform")
