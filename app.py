import streamlit as st
import pandas as pd

st.title("Resident Block Schedule Generator")

st.sidebar.header("Input Method")
input_mode = st.sidebar.radio("Choose how to enter data:", ["Upload CSVs", "Enter Manually"])

residents_df = None
rotations_df = None

if input_mode == "Upload CSVs":
    st.sidebar.header("Upload Input Files")
    residents_file = st.sidebar.file_uploader("Upload residents.csv", type=["csv"])
    rotations_file = st.sidebar.file_uploader("Upload rotations.csv", type=["csv"])
    vacation_prefs_file = st.sidebar.file_uploader("Upload vacation_preferences.csv", type=["csv"])
    rotation_prefs_file = st.sidebar.file_uploader("Upload rotation_preferences.csv", type=["csv"])
    requirements_file = st.sidebar.file_uploader("Upload requirements.csv", type=["csv"])

    if residents_file:
        residents_df = pd.read_csv(residents_file)
    if rotations_file:
        rotations_df = pd.read_csv(rotations_file)

else:
    st.subheader("Enter Resident Data")
    if "resident_data" not in st.session_state:
        st.session_state.resident_data = pd.DataFrame(columns=["Last Name", "First Name", "PGY", "Total Subblocks", "Home Program", "Eligible Rotations"])

    if st.button("➕ Add Resident Row"):
        st.session_state.resident_data.loc[len(st.session_state.resident_data)] = ["", "", 1, 26, "General Surgery", ""]

    residents_df = st.data_editor(st.session_state.resident_data, num_rows="dynamic", use_container_width=True)
    st.download_button("⬇️ Download Residents CSV", residents_df.to_csv(index=False), file_name="residents.csv")

    st.subheader("Enter Rotation Data")
    if "rotation_data" not in st.session_state:
        st.session_state.rotation_data = pd.DataFrame(columns=[
            "Rotation Name", "Duration", "PGY-1 Req", "PGY-1 Opt", "PGY-2 Req", "PGY-2 Opt",
            "PGY-3 Req", "PGY-3 Opt", "PGY-4 Req", "PGY-4 Opt", "PGY-5 Req", "PGY-5 Opt",
            "Total Needed", "Flexible", "Rotation Type", "Difficulty"
        ])

    if st.button("➕ Add Rotation Row"):
        st.session_state.rotation_data.loc[len(st.session_state.rotation_data)] = ["", 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "No", "", 2]

    rotations_df = st.data_editor(st.session_state.rotation_data, num_rows="dynamic", use_container_width=True)
    st.download_button("⬇️ Download Rotations CSV", rotations_df.to_csv(index=False), file_name="rotations.csv")

# Display data summaries before schedule generation
if residents_df is not None:
    st.subheader("Resident Roster")
    st.dataframe(residents_df)

if rotations_df is not None:
    st.subheader("Rotation Details")
    st.dataframe(rotations_df)

st.markdown("---")
if residents_df is not None and rotations_df is not None:
    st.subheader("Next Step")
    st.info("Scheduling engine coming soon: will use these inputs to generate a fair, preference-aware, ACGME-compliant yearly schedule.")
else:
    st.warning("Please complete resident and rotation input to proceed.")
