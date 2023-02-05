import pandas as pd
import streamlit as st

# Load the files into a Pandas dataframe
@st.cache
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# UI for file upload
st.set_page_config(page_title="File Filter and Download", page_icon=":clipboard:", layout="wide")
files = st.file_uploader("Upload multiple files", type=["csv"], allow_multiple=True)

if files:
    # Store all the dataframes in a dictionary
    dfs = {}
    for file in files:
        file_name = file.name
        df = load_data(file)
        dfs[file_name] = df
        st.write(f"{file_name} data preview:")
        st.write(df.head())

    # UI for filter options
    filter_value = st.text_input("Enter filter value")
    if filter_value:
        filtered_dfs = {}
        for file_name, df in dfs.items():
            filtered_df = df[df["column_name"] == filter_value]
            filtered_dfs[file_name] = filtered_df
            st.write(f"{file_name} data after filter:")
            st.write(filtered_df)

        # UI for download options
        if st.button("Download filtered data as Excel"):
            with pd.ExcelWriter("filtered_data.xlsx") as writer:
                for file_name, filtered_df in filtered_dfs.items():
                    filtered_df.to_excel(writer, sheet_name=file_name, index=False)
            st.write("Excel file downloaded")
