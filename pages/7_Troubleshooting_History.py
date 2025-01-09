import streamlit as st
from PIL import Image


st.set_page_config(layout="wide")
st.title("Auto Test Configuration Creation Status")
st.header("Will be updated.")
st.header("Dump data 으로 가공 범주이내")
st.write("Reference. \\pkor33file01\LMK\Manufacturing\Corus (구Ver)\MFG\2. 개인자료\FLEX Public\01 Flex Troubleshooting Sharing Folder (추진중).")

image_path = './Images/Plan_Troubleshooting_History.JPG'
image = Image.open(image_path)
st.image(image, caption='Sample Image', width=800)