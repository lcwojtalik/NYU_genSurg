import streamlit as st
import pandas as pd

st.title("Resident Block Schedule Generator")

st.sidebar.header("Input Method")
input_mode = st.sidebar.radio("Choose how to enter data:", ["Upload CSVs", "Enter Manually"])

residents_df = None
rotations_df = None
rotation_prefs_df = None
vacation_prefs_df = None

# Initialize session state for each data section if not already present
# This sets up the resident data table with required columns
st.session_state.setdefault("resident_data", pd.DataFrame(columns=["Last Name", "First Name", "PGY", "Total Subblocks", "Home Program", "Eligible Rotations", "Start Block", "End Block"]))
st.session_state.setdefault("rotation_data", pd.DataFrame(columns=[
    "Rotation Name", "Duration", "PGY-1 Req", "PGY-1 Opt", "PGY-2 Req", "PGY-2 Opt",
    "PGY-3 Req", "PGY-3 Opt", "PGY-4 Req", "PGY-4 Opt", "PGY-5 Req", "PGY-5 Opt",
    "Total Needed", "Flexible", "Rotation Type", "Difficulty"
]))
st.session_state.setdefault("rotation_prefs", pd.DataFrame(columns=[
    "Last Name", "First Name", "PGY", "Preferred Rotation 1", "Preferred Rotation 2", "Preferred Rotation 3"
]))
st.session_state.setdefault("vacation_prefs", pd.DataFrame(columns=[
    "Last Name", "First Name", "PGY",
    "Pref1 (H1)", "Pref2 (H1)", "Pref3 (H1)",
    "Pref1 (H2)", "Pref2 (H2)", "Pref3 (H2)"
]))

# If the user chooses to upload CSVs, load each into session state
if input_mode == "Upload CSVs":
    st.sidebar.header("Upload Input Files")
    residents_file = st.sidebar.file_uploader("Upload residents.csv", type=["csv"])
    rotations_file = st.sidebar.file_uploader("Upload rotations.csv", type=["csv"])
    vacation_prefs_file = st.sidebar.file_uploader("Upload vacation_preferences.csv", type=["csv"])
    rotation_prefs_file = st.sidebar.file_uploader("Upload rotation_preferences.csv", type=["csv"])
    requirements_file = st.sidebar.file_uploader("Upload requirements.csv", type=["csv"])

    if residents_file:
        st.session_state.resident_data = pd.read_csv(residents_file)
    if rotations_file:
        st.session_state.rotation_data = pd.read_csv(rotations_file)
    if rotation_prefs_file:
        st.session_state.rotation_prefs = pd.read_csv(rotation_prefs_file)
    if vacation_prefs_file:
        st.session_state.vacation_prefs = pd.read_csv(vacation_prefs_file)

st.subheader("Manage Resident Data")
# Appends a blank row to the resident data table when clicked
if st.button("➕ Add Resident Row"):
    st.session_state.resident_data.loc[len(st.session_state.resident_data)] = ["", "", 1, 26, "General Surgery", "", 1, 13]
if st.button("❌ Delete Last Resident") and not st.session_state.resident_data.empty:
    st.session_state.resident_data.drop(index=st.session_state.resident_data.index[-1], inplace=True)
# Displays and allows interactive editing of the resident data table
residents_df = st.data_editor(st.session_state.resident_data, num_rows="dynamic", use_container_width=True)
# Enables exporting the currently edited resident data to a downloadable CSV file
st.download_button("⬇️ Download Residents CSV", residents_df.to_csv(index=False), file_name="residents.csv")

st.subheader("Manage Rotation Data")
if st.button("➕ Add Rotation Row"):
    st.session_state.rotation_data.loc[len(st.session_state.rotation_data)] = ["", 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "No", "", 2]
if st.button("❌ Delete Last Rotation") and not st.session_state.rotation_data.empty:
    st.session_state.rotation_data.drop(index=st.session_state.rotation_data.index[-1], inplace=True)
rotations_df = st.data_editor(st.session_state.rotation_data, num_rows="dynamic", use_container_width=True)
st.download_button("⬇️ Download Rotations CSV", rotations_df.to_csv(index=False), file_name="rotations.csv")

st.subheader("Manage Rotation Preferences")
if st.button("➕ Add Preference Row"):
    st.session_state.rotation_prefs.loc[len(st.session_state.rotation_prefs)] = ["", "", 1, "", "", ""]
if st.button("❌ Delete Last Preference") and not st.session_state.rotation_prefs.empty:
    st.session_state.rotation_prefs.drop(index=st.session_state.rotation_prefs.index[-1], inplace=True)
rotation_prefs_df = st.data_editor(st.session_state.rotation_prefs, num_rows="dynamic", use_container_width=True)
st.download_button("⬇️ Download Rotation Preferences CSV", rotation_prefs_df.to_csv(index=False), file_name="rotation_preferences.csv")

st.subheader("Manage Vacation Preferences")
if st.button("➕ Add Vacation Preference Row"):
    st.session_state.vacation_prefs.loc[len(st.session_state.vacation_prefs)] = ["", "", 1, "", "", "", "", "", ""]
if st.button("❌ Delete Last Vacation Preference") and not st.session_state.vacation_prefs.empty:
    st.session_state.vacation_prefs.drop(index=st.session_state.vacation_prefs.index[-1], inplace=True)
vacation_prefs_df = st.data_editor(st.session_state.vacation_prefs, num_rows="dynamic", use_container_width=True)
st.download_button("⬇️ Download Vacation Preferences CSV", vacation_prefs_df.to_csv(index=False), file_name="vacation_preferences.csv")

# Display data summaries before schedule generation
if residents_df is not None:
    st.subheader("Resident Roster")
    st.dataframe(residents_df)

if rotations_df is not None:
    st.subheader("Rotation Details")
    st.dataframe(rotations_df)

if rotation_prefs_df is not None:
    st.subheader("Rotation Preferences")
    st.dataframe(rotation_prefs_df)

if vacation_prefs_df is not None:
    st.subheader("Vacation Preferences")
    st.dataframe(vacation_prefs_df)

st.markdown("---")
if residents_df is not None and rotations_df is not None:
    st.subheader("Next Step")

    if st.button("🧠 Generate Blank Schedule"):
        # Define 26 subblock columns
        subblocks = [f"Block{i}{suffix}" for i in range(1, 14) for suffix in ["A", "B"]]

        # Create blank schedule for each resident
        schedule = pd.DataFrame(columns=["Last Name", "First Name"] + subblocks)
        for _, row in residents_df.iterrows():
            resident_row = {"Last Name": row["Last Name"], "First Name": row["First Name"]}
            for sub in subblocks:
                resident_row[sub] = ""
            schedule = pd.concat([schedule, pd.DataFrame([resident_row])], ignore_index=True)

        st.subheader("🗓️ Initial Blank Schedule")
st.dataframe(schedule, use_container_width=True)
st.download_button("⬇️ Download Final Schedule", schedule.to_csv(index=False), file_name="final_schedule.csv")

# Assign vacations based on preferences
def assign_vacations(schedule, prefs):
    subblocks = [f"Block{i}{suffix}" for i in range(1, 14) for suffix in ["A", "B"]]
    h1_blocks = subblocks[:12]  # Block1A to Block6B
    h2_blocks = subblocks[12:]  # Block7A to Block13B

    assigned = set()

    for idx, row in prefs.iterrows():
        full_name = (row['Last Name'], row['First Name'])
        sched_idx = schedule[(schedule['Last Name'] == full_name[0]) & (schedule['First Name'] == full_name[1])].index

        if not sched_idx.empty:
            i = sched_idx[0]
            # H1 vacation
            for pref in [row['Pref1 (H1)'], row['Pref2 (H1)'], row['Pref3 (H1)']]:
                if pref in h1_blocks and schedule[pref].isna().sum() > 0 and schedule.loc[i, pref] == "":
                    schedule.loc[i, pref] = "Vacation"
                    break
            # H2 vacation
            for pref in [row['Pref1 (H2)'], row['Pref2 (H2)'], row['Pref3 (H2)']]:
                if pref in h2_blocks and schedule[pref].isna().sum() > 0 and schedule.loc[i, pref] == "":
                    schedule.loc[i, pref] = "Vacation"
                    break
    return schedule

if st.button("📅 Assign Vacations"):
    schedule = assign_vacations(schedule, vacation_prefs_df)
    st.success("Vacations assigned!")
    st.dataframe(schedule, use_container_width=True)
st.download_button("⬇️ Download Final Schedule", schedule.to_csv(index=False), file_name="final_schedule.csv")

# Assign basic rotations following vacation assignment
def assign_basic_rotations(schedule, residents_df, rotations_df):
    subblocks = [f"Block{i}{suffix}" for i in range(1, 14) for suffix in ["A", "B"]]

    # Track how many times each rotation is assigned per PGY level
    rotation_counts = {f"PGY-{lvl}": {} for lvl in range(1, 6)}

    # Track required rotation completion per resident
    required_tracker = {}

    for idx, res in residents_df.iterrows():
        res_name = (res['Last Name'], res['First Name'])
        pgy = int(res['PGY'])
        sched_idx = schedule[(schedule['Last Name'] == res_name[0]) & (schedule['First Name'] == res_name[1])].index
        if sched_idx.empty:
            continue
        i = sched_idx[0]

        # Create tracker of required rotations for this resident
        required_rotations = rotations_df[rotations_df[f"PGY-{pgy} Req"] > 0]
        required_tracker[i] = {
            row['Rotation Name']: row[f"PGY-{pgy} Req"] for _, row in required_rotations.iterrows()
        }

        for block in subblocks:
            block_num = int(block.replace("Block", "")[0:-1])
            if schedule.loc[i, block] == "" and res['Start Block'] <= block_num <= res['End Block']:
                eligible = rotations_df[
                    (rotations_df[f"PGY-{pgy} Req"] > 0) | (rotations_df[f"PGY-{pgy} Opt"] > 0)
                ].copy()

                if not eligible.empty:
                    # Prioritize unmet required rotations
                    def score_fn(row):
                        name = row['Rotation Name']
                        req_left = required_tracker[i].get(name, 0)
                        fairness = rotation_counts[f"PGY-{pgy}"].get(name, 0)
                        return (req_left == 0, fairness)  # Sort by unmet requirement, then fairness

                    eligible['score'] = eligible.apply(score_fn, axis=1)
                    eligible = eligible.sort_values(by='score')

                    rotation = eligible.iloc[0]
                    rotation_name = rotation['Rotation Name']
                    schedule.loc[i, block] = rotation_name

                    # Update counters
                    rotation_counts[f"PGY-{pgy}"][rotation_name] = rotation_counts[f"PGY-{pgy}"].get(rotation_name, 0) + 1
                    if rotation_name in required_tracker[i] and required_tracker[i][rotation_name] > 0:
                        required_tracker[i][rotation_name] -= 1

    return schedule

if st.button("📌 Assign Basic Rotations"):
    schedule = assign_basic_rotations(schedule, residents_df, rotations_df)
    st.success("Basic rotations assigned!")
    st.dataframe(schedule, use_container_width=True)
st.download_button("⬇️ Download Final Schedule", schedule.to_csv(index=False), file_name="final_schedule.csv")
else:
    st.warning("Please complete resident and rotation input to proceed.")
