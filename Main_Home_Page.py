import streamlit as st
import base64

# from streamlit_lottie import st_lottie  # pip install streamlit-lottie
# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/


st.set_page_config(
    page_title='Bulletin Board'
)

st.title("Main Page")
st.sidebar.success("Select a page above")

# # URL을 통한 GIF 표시
# st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")

# # 절대 경로를 통한 GIF 표시
file_ = open("./Images/waving-287_256.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="gif">',
    unsafe_allow_html=True,
)
