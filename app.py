
import streamlit as st
import pandas as pd

st.title("Resident Block Schedule Generator")

st.sidebar.header("Upload Input Files")
residents_file = st.sidebar.file_uploader("Upload residents.csv", type=["csv"])
rotations_file = st.sidebar.file_uploader("Upload rotations.csv", type=["csv"])
vacation_prefs_file = st.sidebar.file_uploader("Upload vacation_preferences.csv", type=["csv"])
rotation_prefs_file = st.sidebar.file_uploader("Upload rotation_preferences.csv", type=["csv"])
requirements_file = st.sidebar.file_uploader("Upload requirements.csv", type=["csv"])

if residents_file and rotations_file:
    residents_df = pd.read_csv(residents_file)
    rotations_df = pd.read_csv(rotations_file)

    st.subheader("Resident Roster")
    st.dataframe(residents_df)

    st.subheader("Rotation Details")
    st.dataframe(rotations_df)

    if vacation_prefs_file:
        vacation_prefs_df = pd.read_csv(vacation_prefs_file)
        st.subheader("Vacation Preferences")
        st.dataframe(vacation_prefs_df)

    if rotation_prefs_file:
        rotation_prefs_df = pd.read_csv(rotation_prefs_file)
        st.subheader("Rotation Preferences")
        st.dataframe(rotation_prefs_df)

    if requirements_file:
        requirements_df = pd.read_csv(requirements_file)
        st.subheader("ACGME Requirements")
        st.dataframe(requirements_df)

    st.markdown("---")
    st.subheader("Next Step")
    st.info("Scheduling engine coming soon: will use these inputs to generate a fair, preference-aware, ACGME-compliant yearly schedule.")

else:
    st.warning("Please upload at least residents.csv and rotations.csv to begin.")
