import streamlit as st
from PIL import Image
import pandas as pd
import os
import re
import time


# Streamlit 페이지 설정
st.set_page_config(layout="wide")
st.title("ATAC PC Location And Expired Dates")

# 이미지 표시
image_path = './Images/ATAC_PC_Location.JPG'
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, caption='Flex ATAC PC Location', width=800)
else:
    st.error(f"Image not found at {image_path}")

# 주어진 데이터
data = {
    "PM": [
        "PM 6: CTC-KO-6003075", "PM 5: CTC-KO-2001354", "PM 4: CTC-KO-6003226",
        "PM 3: CTC-KO-6003221", "PM 2: CTC-KO-6002754", "PM 1: CTC-KO-6003223",
        "PM NPI 1: CTC-KO-7002354", "PM NPI 2: CTC-KO-7002348", "PM NPI 3: CTC-KO-5003908"
    ],
    "Top": [
        "Top 1: CTC-KO-6003224", "Top 2: CTC-KO-2001357", "", "", "", "", "", "", ""
    ],
    "RF": [
        "RF 1: CTC-KO-3004728", "", "", "", "", "", "", "", ""
    ],
    "Bias": [
        "Bias 1: CTC-KO-9008168", "Bias 2: CTC-KO-2001348", "Bias 3: CTC-KO-2001344",
        "Bias 4: CTC-KO-6003215", "Bias 5: CTC-KO-9008166", "Bias 6: CTC-KO-9008157",
        "", "", ""
    ]
}
df = pd.DataFrame(data)
df.index = df.index + 1

folder_path = r"\\fre_filer03\2300testdata\PMATACConfig\Osan\activated_atac_pc_list\hwasung"

def extract_expiration_dates(folder_path):
    results = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    content = file.read()
                    match = re.search(r"ExpirationDate\s*:\s*:\s*'([^']+)'", content)
                    if match:
                        expiration_date = match.group(1)
                        filename_without_extension = os.path.splitext(filename)[0]
                        results.append((filename_without_extension, expiration_date))
    else:
        st.error(f"Folder not found at {folder_path}")
    return results

def update_expiration_dates(df, expiration_data):
    for col in df.columns:
        for i in range(len(df[col])):
            for filename, exp_date in expiration_data:
                if filename in str(df[col].iloc[i]):
                    df.at[i + 1, col] += f" ({exp_date})"
    return df


# 액션 버튼
if st.button('Check Expiration Dates (The process takes approximately 28 seconds.)'):
    start_time = time.time()

    results = extract_expiration_dates(folder_path)
    df_updated = update_expiration_dates(df.copy(), results)

    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 경과 시간 계산

    st.table(df_updated)

    st.write(f"Running time: {elapsed_time:.2f} Second")
else:
    st.table(df)
