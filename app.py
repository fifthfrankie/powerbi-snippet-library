import streamlit as st
import pandas as pd
import os
import zipfile
import json
from io import BytesIO
import shutil

# Snippet Library Path
SNIPPETS_DIR = "snippets"
os.makedirs(SNIPPETS_DIR, exist_ok=True)

# Initialize Snippet Library
if "snippets" not in st.session_state:
    st.session_state.snippets = pd.DataFrame(columns=["Type", "Name", "Description", "Content"])

# Load Existing Snippets
def load_snippets():
    if os.path.exists(os.path.join(SNIPPETS_DIR, "snippets.csv")):
        # Load the CSV file
        snippets_df = pd.read_csv(os.path.join(SNIPPETS_DIR, "snippets.csv"))
        # Ensure the 'Description' column exists
        if "Description" not in snippets_df.columns:
            snippets_df["Description"] = ""  # Add an empty Description column
        # Update the session state
        st.session_state.snippets = snippets_df

# Save Snippets
def save_snippets():
    st.session_state.snippets.to_csv(os.path.join(SNIPPETS_DIR, "snippets.csv"), index=False)

# Add a Snippet
def add_snippet(snippet_type, name, description, content):
    new_snippet = pd.DataFrame([[snippet_type, name, description, content]], columns=["Type", "Name", "Description", "Content"])
    st.session_state.snippets = pd.concat([st.session_state.snippets, new_snippet], ignore_index=True)
    save_snippets()

# Remove a Snippet
def remove_snippet(index):
    st.session_state.snippets = st.session_state.snippets.drop(index).reset_index(drop=True)
    save_snippets()

# Inject Snippets into PBIT
def inject_snippets_into_pbit(pbit_file, selected_snippets):
    with zipfile.ZipFile(pbit_file, 'r') as zip_ref:
        zip_ref.extractall("temp_template")
    # Locate the DataModelSchema file
    schema_path = os.path.join("temp_template", "DataModelSchema")
    with open(schema_path, "r") as f:
        schema = json.load(f)
    # Inject selected snippets
    for snippet in selected_snippets:
        snippet_content = st.session_state.snippets.loc[
            st.session_state.snippets["Name"] == snippet, "Content"
        ].values[0]
        # Example: Add DAX measure
        schema["model"]["tables"][0]["measures"].append({
            "name": snippet,
            "expression": snippet_content
        })
    # Save the modified schema
    with open(schema_path, "w") as f:
        json.dump(schema, f)
    # Repackage the PBIT file
    output_pbit = BytesIO()
    with zipfile.ZipFile(output_pbit, 'w') as zip_ref:
        for root, _, files in os.walk("temp_template"):
            for file in files:
                zip_ref.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), "temp_template")
                )
    # Clean up
    shutil.rmtree("temp_template")
    return output_pbit.getvalue()

# Load Snippets on App Start
load_snippets()

# Streamlit App
st.title("Power BI Snippet Library")

# Sidebar for Adding Snippets
with st.sidebar:
    st.header("Add a New Snippet")
    
    if "snippet_name" not in st.session_state:
        st.session_state.snippet_name = ""
    if "snippet_description" not in st.session_state:
        st.session_state.snippet_description = ""
    if "snippet_content" not in st.session_state:
        st.session_state.snippet_content = ""

    with st.form(key="add_snippet_form"):
        snippet_type = st.selectbox("Snippet Type", ["DAX", "Power Query"])
        snippet_name = st.text_input("Snippet Name", value=st.session_state.snippet_name, key="snippet_name_input")
        snippet_description = st.text_input("Snippet Description", value=st.session_state.snippet_description, key="snippet_description_input")
        snippet_content = st.text_area("Paste Snippet Here", value=st.session_state.snippet_content, key="snippet_content_input")
        
        submitted = st.form_submit_button("Add Snippet")
        if submitted:
            if snippet_name and snippet_content:
                add_snippet(snippet_type, snippet_name, snippet_description, snippet_content)
                st.success(f"Snippet '{snippet_name}' added!")
                # Clear the form fields by resetting session state -- not working?
                st.session_state.snippet_name = ""
                st.session_state.snippet_description = ""
                st.session_state.snippet_content = ""
            else:
                st.error("Please provide a name and content for the snippet.")

# Main Area for Browsing and Managing Snippets
st.header("Browse and Manage Snippets")
search_query = st.text_input("Search Snippets (Name or Description)")
filtered_snippets = st.session_state.snippets
if search_query:
    filtered_snippets = st.session_state.snippets[
        st.session_state.snippets["Name"].str.contains(search_query, case=False) |
        st.session_state.snippets["Description"].str.contains(search_query, case=False)
    ]

if not filtered_snippets.empty:
    # Multi-select for Snippets
    selected_snippets = st.multiselect(
        "Select Snippets to Ingest",
        filtered_snippets["Name"].unique()
    )
    # Upload PBIT File
    uploaded_file = st.file_uploader("Upload a Power BI Template (.PBIT)", type="pbit")
    if uploaded_file and selected_snippets:
        if st.button("Inject Snippets into PBIT"):
            modified_pbit = inject_snippets_into_pbit(uploaded_file, selected_snippets)
            st.success("Snippets injected successfully!")
            st.download_button(
                label="Download Modified PBIT",
                data=modified_pbit,
                file_name="modified_template.pbit",
                mime="application/zip"
            )
    # Display Snippets with Remove Option
    for index, row in filtered_snippets.iterrows():
        with st.expander(f"{row['Type']}: {row['Name']}"):
            st.markdown(f"**Description:** {row['Description']}")
            st.code(row["Content"], language="text")
            if st.button(f"Remove {row['Name']}", key=f"remove_{index}"):  # Unique key using index
                remove_snippet(index)
                st.success(f"Snippet '{row['Name']}' removed!")
                st.rerun()  # Refresh the app
else:
    st.info("No snippets found. Add some using the sidebar!")