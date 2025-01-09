import streamlit as st
from PIL import Image
import subprocess


st.set_page_config(layout="wide")
st.title("UPL ACA Option Manager")
st.header("하기 버튼을 누르면 10초 이후에 Application 실행이 됩니다.")
st.write("Reference. Test Config Sheet 자동 생성 중 UPL 의 ACA Files 생성의 옵션을 적용 하기 위한 임시 app 입니다.")

if st.button('Launch the application'):
    program_path = r"\\pkor33file01\LMK\Manufacturing\Application\Test_Config_Sheet_Automatic_Generator\SQL_lite3_DB_CFG_Option\UPL_ACA_Option_Manager.exe"
    subprocess.run(program_path)
    st.success('Program has been executed!')

image_path = './Images/UPL_ACA_Option_Manager.JPG'
image = Image.open(image_path)
st.image(image, caption='Application Sample Image', width=800)




