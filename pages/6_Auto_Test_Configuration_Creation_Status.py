import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
import os
import time

# Set page configuration
st.set_page_config(layout="wide")
st.title("Auto Test Configuration Creation Status")
st.header("First Draft.")
st.write("Reference. Auto mailing 되고 있는 사항 표시")

# Display image
image_path = './Images/Plan_Auto_Test_Configuration_Creation_Status.JPG'
try:
    image = Image.open(image_path)
    st.image(image, caption='Sample Image', width=500)  # Increased width for better visibility
except FileNotFoundError:
    st.error("Image file not found.")


def get_folder_names(path):
    try:
        folder_names = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
        return folder_names
    except FileNotFoundError:
        return f"Error: The directory {path} does not exist."
    except PermissionError:
        return f"Error: Permission denied to access the directory {path}."


def fcid_list_existing_test_configuration_sheet_flex():
    path = '\\\\pkor33file01\\LMK\\Manufacturing\\Application\\Test_Configuration_Sheet_FLEX'
    get_list = get_folder_names(path)
    return get_list


def highlight_row(row, fcid_list_existing_sheet):
    if str(row['FCID']) in fcid_list_existing_sheet:
        return ['background-color: lime'] * len(row)
    else:
        return ['background-color: pink'] * len(row)


# File paths
lpr_401_excel_file_path_name = "\\\\pkor33file01\\LMK\\Manufacturing\\Application\\Test_Config_Sheet_Automatic_Generator\\LPR\\LPR_POM_401_FLEX.XLSX"
lpr_416_excel_file_path_name = "\\\\pkor33file01\\LMK\\Manufacturing\\Application\\Test_Config_Sheet_Automatic_Generator\\LPR\\LPR_POM_416_FLEX.XLSX"

# Load and process data
try:
    df_401 = pd.read_excel(lpr_401_excel_file_path_name)
    df_416 = pd.read_excel(lpr_416_excel_file_path_name)

    exclusion_phrase = 'RFC_'

    df_filtered_exclude_rfc_401 = df_401[~df_401['LPR Product'].str.contains(exclusion_phrase)]
    df_filtered_exclude_rfc_416 = df_416[~df_416['LPR Product'].str.contains(exclusion_phrase)]

    reference_date_2w_before = datetime.now() - timedelta(weeks=1)
    reference_date_2w_after = datetime.now() + timedelta(weeks=2)

    date_column = 'P09-Pln Launch'

    df_filtered_exclude_rfc_401.loc[:, date_column] = pd.to_datetime(df_filtered_exclude_rfc_401[date_column])
    df_filtered_exclude_rfc_416.loc[:, date_column] = pd.to_datetime(df_filtered_exclude_rfc_416[date_column])

    filtered_df_401 = df_filtered_exclude_rfc_401[
        (df_filtered_exclude_rfc_401[date_column] <= reference_date_2w_after) & (
                    df_filtered_exclude_rfc_401[date_column] >= reference_date_2w_before)]
    filtered_df_416 = df_filtered_exclude_rfc_416[
        (df_filtered_exclude_rfc_416[date_column] <= reference_date_2w_after) & (
                    df_filtered_exclude_rfc_416[date_column] >= reference_date_2w_before)]

    golden_sheet_generation_info_selected_columns = ['P09-Pln Launch', 'FCID', 'LPR Product', 'LPR Serial No']

    result_golden_sheet_generation_info_df_401 = filtered_df_401[golden_sheet_generation_info_selected_columns]
    result_golden_sheet_generation_info_df_416 = filtered_df_416[golden_sheet_generation_info_selected_columns]

    data_1 = pd.DataFrame(result_golden_sheet_generation_info_df_401)
    data_2 = pd.DataFrame(result_golden_sheet_generation_info_df_416)

    data_1 = data_1.reset_index(drop=True)
    data_2 = data_2.reset_index(drop=True)

    data_1 = data_1.sort_values(by='P09-Pln Launch').reset_index(drop=True)  # Reset index to remove index column
    data_2 = data_2.sort_values(by='P09-Pln Launch').reset_index(drop=True)  # Reset index to remove index column

    # Remove time part from date
    data_1['P09-Pln Launch'] = data_1['P09-Pln Launch'].dt.strftime('%Y-%m-%d')
    data_2['P09-Pln Launch'] = data_2['P09-Pln Launch'].dt.strftime('%Y-%m-%d')

    # Remove commas from FCID column
    data_1['FCID'] = data_1['FCID'].astype(str).str.replace(',', '')
    data_2['FCID'] = data_2['FCID'].astype(str).str.replace(',', '')

    if st.button('Run Action'):
        start_time = time.time()

        fcid_list_existing = fcid_list_existing_test_configuration_sheet_flex()

        styled_df_401 = data_1.style.apply(highlight_row, axis=1, fcid_list_existing_sheet=fcid_list_existing)
        styled_df_416 = data_2.style.apply(highlight_row, axis=1, fcid_list_existing_sheet=fcid_list_existing)

        end_time = time.time()
        elapsed_time = end_time - start_time

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(styled_df_401, height=2000, width=500)  # Adjust height and width as needed

        with col2:
            st.dataframe(styled_df_416, height=2000, width=500)  # Adjust height and width as needed

        st.write(f"Time taken: {elapsed_time:.2f} seconds")

    else:
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(data_1, height=2000, width=500)  # Adjust height and width as needed

        with col2:
            st.dataframe(data_2, height=2000, width=500)  # Adjust height and width as needed

except FileNotFoundError:
    st.error("Excel file not found.")
except Exception as e:
    st.error(f"An error occurred: {e}")