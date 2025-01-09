import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(layout="wide")
st.title("ATAC PC Location And Expired Dates")


image_path = 'D:/streamlit_modle_list/Images/ATAC_PC_Location.JPG'
image = Image.open(image_path)
st.image(image, caption='Flex ATAC PC Location', width=800)


data = {
    "PM": ["PM 6: CTC-KO-6003075", "PM 5: CTC-KO-2001354", "PM 4: CTC-KO-6003226", "PM 3: CTC-KO-6003221", "PM 2: CTC-KO-6002754", "PM 1: CTC-KO-6003223", "PM NPI 1: CTC-KO-7002354", "PM NPI 2: CTC-KO-7002348", "PM NPI 3: CTC-KO-5003908"],
    "Top": ["Top 1: CTC-KO-6003224", "Top 2: CTC-KO-2001357", "", "", "", "", "", "", ""],
    "RF": ["RF 1: CTC-KO-3004728", "", "", "", "", "", "", "", ""],
    "Bias": ["Bias 1: CTC-KO-9008168", "Bias 2: CTC-KO-2001348", "Bias 3: CTC-KO-2001344", "Bias 4: CTC-KO-6003215", "Bias 5: CTC-KO-9008166", "Bias 6: CTC-KO-9008157", "", "", ""]
}
df = pd.DataFrame(data)
df.index = df.index + 1
st.table(df)