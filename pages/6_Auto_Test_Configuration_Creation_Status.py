import streamlit as st
from PIL import Image


st.set_page_config(layout="wide")
st.title("Troubleshooting History")
st.header("Will be updated.")
st.write("Reference. Auto mailing 되고 있는 사항 표시")


image_path = './Images/Plan_Auto_Test_Configuration_Creation_Status.JPG'
image = Image.open(image_path)
st.image(image, caption='Sample Image', width=800)