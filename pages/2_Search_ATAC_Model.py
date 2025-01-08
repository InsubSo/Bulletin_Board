import streamlit as st
import pandas as pd
import sqlite3
import os

# Streamlit emoji shortcodes
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/


# Function to get a database connection
def get_db_connection():
    try:
        conn = sqlite3.connect(path_database_lmk_public + name_database_flex_model)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None


def create_database_table():
    # Ensure the directory exists
    os.makedirs(path_database_lmk_public, exist_ok=True)

    # Create the table if it doesn't exist
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                POM TEXT,
                LPR_Model_Name TEXT,
                Type_Class TEXT,
                ATAC_Model_Number TEXT,
                ATAC_Spec_Model TEXT,
                UI_Software TEXT,
                ACA_CFG_Model TEXT,
                Remark TEXT
            )
        ''')
        conn.commit()
        conn.close()


def add_model():
    new_model = {
        'POM': st.session_state.pom,
        'LPR_Model_Name': st.session_state.lpr_model_name,
        'Type_Class': st.session_state.type_class,
        'ATAC_Model_Number': st.session_state.model_number,
        'ATAC_Spec_Model': st.session_state.spec_model,
        'UI_Software': st.session_state.ui_software,
        'ACA_CFG_Model': st.session_state.aca_cfg_model,
        'Remark': st.session_state.model_description
    }

    # Insert the new model into the database
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO models (POM, LPR_Model_Name, Type_Class, ATAC_Model_Number, ATAC_Spec_Model, UI_Software, ACA_CFG_Model, Remark)
                VALUES (:POM, :LPR_Model_Name, :Type_Class, :ATAC_Model_Number, :ATAC_Spec_Model, :UI_Software, :ACA_CFG_Model, :Remark)
            ''', new_model)
            conn.commit()
        except sqlite3.Error as e:
            st.error(f"Error inserting into database: {e}")
        finally:
            conn.close()
    # st.success("Model added successfully!")
    return "Model added successfully!"


def sidebar_for_model_registration_form():
    # 페이지 레이아웃 설정 (스크립트의 첫 번째 Streamlit 명령어로)
    st.set_page_config(layout="wide")

    # Sidebar for model registration form
    with st.sidebar:
        st.title(":card_file_box: Flex Model Registration")

        pom_options = ["401 HVM", "416 UPL"]
        selected_pom = st.selectbox("POM", pom_options, key='pom')

        lpr_model_options = {
            "401 HVM": [
                "23FLEXFSE-K", "23FLEXFS-K", "23FLEXFL-K", "23FLEXFL_AMMP-K","23FLEXFX-K",
                "23FLEXGL-K", "23FLEXGB-K", "23FLEXGS",
                "23FLEXHX","23FLEXHXE", "23FLEXHXE_CRYO", "23FLEXHXPL_CRYO", "23FLEXJXP"
            ],
            "416 UPL": [
                "FLEXGX/GXE-HXPL", "FLEXHXPL-HXPLC", "FLEXHXPLHXE_CM", "FLEXHX_PLUS-HXE"
            ]
        }
        st.selectbox("LPR Model Name", lpr_model_options[selected_pom], key='lpr_model_name')


        type_class_options = ["RF Cart", "Top plate", "Bias", "PM"]
        selected_type_class = st.selectbox("Type Class", type_class_options, key='type_class')

        atac_model_options = {
            "RF Cart": ["2300RFCart", "FlexGSRFCart", "FlexHXPlusRFCart", "FLEXJXPRFCart"],
            "Top plate": ["ExelanTopPlate"],
            "Bias": [
                "FlexFSeriesBiasElectrode", "FlexFLSeriesBiasElectrode", "FlexGLSeriesBiasElectrode",
                "FlexGBBiasElectrode", "FlexGSBiasElectrode", "FlexHXEBiasElectrode",
                "FlexHSeriesBiasElectrode", "FlexJXPBiasElectrode", "FlexHXPlusBiasElectrode"
            ],
            "PM": [
                "FlexFSeries", "FlexFLSeries", "FlexGLSeries", "FlexGBPM",
                "FlexGS", "FlexHXEPM", "FlexHSeries", "FlexJXP"
            ]
        }
        selected_model_number = st.selectbox("ATAC Model Number", atac_model_options[selected_type_class], key='model_number')

        # Dictionary to map ATAC Model Number to ATAC Spec Model options
        atac_spec_model_options = {
            "2300RFCart": ["Dielectric Exelan Flex RF Cart", "DielectricRFCart_GL","DielectricRFCart_HSeries-CIP_Gen_Firmware_Checking"],
            "FlexGSRFCart": ["FlexGSRFCart_UI-SP13-439"],
            "FlexHXPlusRFCart": ["DielectricRFCart_HXPlus"],
            "FLEXJXPRFCart": ["FlexJXP_UI-SP19-527"],
            "ExelanTopPlate": ["100A_Universal_Top_Plate", "FlexGL_Top_Plate", "Universal_Top_Plate_16CAM-HXPlus", "Universal_Top_Plate_HX_HX+_HXE-Razor", "Universal_Top_Plate_HX-HXPLUS", "FlexJXP_1.8.4-SP19-527"],
            "FlexFSeriesBiasElectrode": ["CW184_SP10_356_Rel_FSE_ONLY", "CW184_SP8_310_Rel"],
            "FlexFLSeriesBiasElectrode": ["FlexFLSeriesBiasElectrode"],
            "FlexGLSeriesBiasElectrode": ["FlexGLMZESC_Post_BQ"],
            "FlexGBBiasElectrode": ["FlexGB_BiasElectrode"],
            "FlexGSBiasElectrode": ["CW184_SP24_598"],
            "FlexHXEBiasElectrode": ["CW184_SP17-510_FlexHXEBiasElectrode_NoCryo", "FlexHXEBiasElectrodeCRYO"],
            "FlexHSeriesBiasElectrode": ["FlexHSeriesBiasElectrode_Corvus"],
            "FlexJXPBiasElectrode": ["FLEX_JXP"],
            "FlexHXPlusBiasElectrode": ["FlexHXPlusBiasElectrode_Cryo", "FlexHXPlus - Blankoff", "FlexHXPlus", "FlexHXPlusBiasElectrodeTES20_40"],
            "FlexFSeries": ["CW184_SP24_598_FLFSE_LMK", "CW184_SP24_598_FLFL_AMMP_LMK", "CW184_SP24_598_FLFX_LMK"],
            "FlexFLSeries": ["CW184_SP24_598_FlexFL_MZESC_LMK", "CW184_SP24_598_FlexFL_MZESC_AMMP_LMK", "CW184_SP24_598_FlexFL_MZESC_LMK_ESC_Blank"],
            "FlexGLSeries": ["CW184_SP24_598_FLGL_LMK"],
            "FlexGBPM": ["184_SP24-598_x10_CPU_FlexGB_MZESC"],
            "FlexGS": ["FlexGS_1.8.4_UI-SP30-B9_NoTCU"],
            "FlexHXEPM": ["CW184_SP24-598", "CW184_SP27-HF2-Razor_NoTCU", "CW184_SP30_B9-Release_NoTCU"],
            "FlexHSeries": ["184_SP24-598_X10_CPU-FlexHSeries_HX_NoTCU"],
            "FlexJXP": ["FlexJXP_1.8.4_UI-SP24-598"]
        }
        st.selectbox("ATAC Spec Model", atac_spec_model_options.get(selected_model_number, []), key='spec_model')

        st.selectbox("UI Software", [
            'Version_1.8.4_SP8-310', 'Version_1.8.4-SP10-356', 'Version_1.8.4-SP12-414', 'Version_1.8.4-SP13-HF2a',
            'Version_1.8.4-SP13-439', 'Version_1.8.4-SP13-HF5-', 'Version_1.8.4-SP16-HF1-',
            'Version_1.8.4-SP17-510', 'Version_1.8.4-SP19-527', 'Version_1.8.4-SP21-555',
            'Version_1.8.4-SP22-B5-', 'Version_1.8.4-SP24-598', 'Version_1.8.4-SP27-628',
            'Version_1.8.4-SP30-B9_', 'Version_1.8.4-SP30-HF3-'
        ], key='ui_software')

        aca_cfg_model_options = {
            "RF Cart": [
                "", "Flex FSE-RF", "Flex FS-RF", "Flex FLFL-RF",
                "Flex FLGB-RF", "Flex FLGS-RF",
                "Flex HX-RF", "Flex FLHXE-RF",
                'Flex HX+-RF',
                "Flex HXE CRYO-RF", "Flex HXPlus CRYO-RF",
                "Flex JXP-RF",
            ],
            "Top plate": [
                "Flex FSE-TP", "Flex FS-TP","Flex FLFS-TP", "Flex FLFL-TP", "Flex FLFX-TP",
                "Flex FLGL-TP","Flex FLGB-TP", "Flex FLGS-TP",
                "Flex HX-TP", "Flex FLHXE-TP(Pinstripe)",
                "Flex HXE CRYO-TP", "Flex HXPlus CRYO-TP",
                "Flex HX+-TP", "Flex HX+-TP(Pinstripe)",
                "Flex JXP-TP",
            ],
            "Bias": [
                "Flex FSE-BE", "Flex FS-BE", "Flex FLFS-BE", "Flex FLFL-BE", "Flex FLFX-BE",
                "Flex FLGL-BE", "Flex FLGB-BE", "Flex FLGS-BE",
                "Flex HXE-BE", "Flex HX-BE", "Flex FLHXE-BE", "Flex HXE-BE",
                "Flex HXE CRYO-BE", "Flex HXPlus CRYO-BE",
                "Flex HX-PLUS-BE",
                "Flex JXP-BE",
            ],
            "PM": [
                "Flex FSE-PM", "Flex FS-PM", "Flex FLFS-PM", "Flex FLFL-PM", "Flex FLFX-PM",
                "Flex FLGL-PM", "Flex FLGB-PM", "Flex FLGS-PM",
                "Flex HX-PM",  "Flex FLHXE-PM",
                "Flex HXE CRYO-PM",
                "Flex JXP-PM",
            ]
        }
        st.selectbox("ACA CFG Model", aca_cfg_model_options[selected_type_class], key='aca_cfg_model')


        st.text_area("Remark", key='model_description')
        st.button("Add Model", on_click=add_model)


# Function to filter LPR Model Name
def filter_lpr_model_name():
    # Apply custom CSS to change the color of selected items in the multiselect
    st.markdown("""
        <style>
        .stMultiSelect [data-baseweb="tag"] {
            background-color: limegreen !important;
        }
        div.stButton > button {
            background-color: springgreen !important;
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Filter LPR Model Name
    st.title(":card_index_dividers: Search ATAC Model Index by Filtering LPR Model Name")

    filter_lpr_model_names = st.multiselect("Showing all the items listed. When you select them ,"
                                            "It will indicated only that.", [
        "23FLEXFSE-K", "23FLEXFS-K", "23FLEXFL-K", "23FLEXFL_AMMP-K",
        "23FLEXFX-K", "23FLEXGL-K", "23FLEXGB-K", "23FLEXGS", "23FLEXHX",
        "23FLEXHXE", "23FLEXHXE_CRYO", "23FLEXHXPL_CRYO", "23FLEXJXP",
        "FLEXGX/GXE-HXPL", "FLEXHXPL-HXPLC", "FLEXHXPLHXE_CM", "FLEXHX_PLUS-HXE"
    ], default=[], placeholder="Select LPR Model Name to filter")

    # Fetch all models from the database
    conn = get_db_connection()
    models = []
    if conn:
        try:
            c = conn.cursor()
            if not filter_lpr_model_names:
                c.execute('SELECT * FROM models')
            else:
                query = 'SELECT * FROM models WHERE LPR_Model_Name IN ({})'.format(
                    ','.join('?' for _ in filter_lpr_model_names))
                c.execute(query, filter_lpr_model_names)
            models = c.fetchall()
        except sqlite3.Error as e:
            st.error(f"Error fetching from database: {e}")
        finally:
            conn.close()

    # Create DataFrame
    df_models = pd.DataFrame(models, columns=['ID', 'POM', 'LPR Model Name', 'Type Class', 'ATAC Model Number',
                                              'ATAC Spec Model', 'UI Software', 'ACA CFG Model', 'Remark'])

    # Add 'Delete' column with checkboxes
    df_models['Delete'] = False

    # Display DataFrame with checkboxes for deletion in the table, hiding the 'ID' column
    edited_df = st.data_editor(df_models, use_container_width=True, hide_index=True,
                               column_config={'ID': {'hidden': True}, 'POM': {'hidden': True}})

    # Delete selected models when the button is clicked
    if st.button(label="Delete Selected Models", use_container_width=True):
        delete_ids = edited_df[edited_df['Delete'] == True]['ID'].tolist()
        if delete_ids:
            delete_models(delete_ids)
            st.rerun()
        else:
            st.warning("No models selected for deletion.")


# Function to delete models by ids
def delete_models(model_ids):
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            c.executemany('DELETE FROM models WHERE id = ?', [(model_id,) for model_id in model_ids])
            conn.commit()
        except sqlite3.Error as e:
            st.error(f"Error deleting from database: {e}")
        finally:
            conn.close()
    st.success("Selected models deleted successfully!")


if __name__ == "__main__":
    path_database_lmk_public = "\\\\pkor33file01\\LMK\Manufacturing\\Application\\Test_Web_Application_Bulletin_Board\\DB_File\\"
    name_database_flex_model = "flex_atac_models.db"
    # create_database_table()   # For first time , to created db file.

    sidebar_for_model_registration_form()
    filter_lpr_model_name()

