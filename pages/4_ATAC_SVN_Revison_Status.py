import streamlit as st
import os
import subprocess
import time
import threading
# import win32com.client

class FileProcessor:
    def __init__(self, directory, pm_filenames, be_filenames, tp_filenames):
        self.directory = directory
        self.pm_filenames = pm_filenames
        self.be_filenames = be_filenames
        self.tp_filenames = tp_filenames
        self.file_data = {}
        self.pm_data = []
        self.be_data = []
        self.tp_data = []
        self.pm_differences = {}
        self.be_differences = {}
        self.tp_differences = {}
        self.pm_keys = set()
        self.be_keys = set()
        self.tp_keys = set()
        self.pm_missing_keys = {}
        self.be_missing_keys = {}
        self.tp_missing_keys = {}

    def read_file(self, filepath):
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                data = [tuple(line.strip().split(', ')) for line in lines]
            return data
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return []
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return []

    def process_files(self, filenames, data_list):
        for filename in filenames:
            filepath = os.path.join(self.directory, filename)
            self.file_data[filename] = self.read_file(filepath)
            data_list.append((filename, self.file_data[filename]))

    def print_all_data(self, data_list):
        # for filename, data in data_list:
        #     print(f"{filename}:")
        #     for item in data:
        #         print(f"  {item}")
        #     print("\n")
        for print_all_data in data_list:
            print(print_all_data)

    def find_differences(self, filenames, differences):
        if filenames:
            keys = set(self.file_data[filenames[0]])
            for filename, data in self.file_data.items():
                if filename in filenames:
                    for item in data:
                        if item not in keys:
                            if filename not in differences:
                                differences[filename] = []
                            differences[filename].append(item)

    def print_differences(self, differences):
        if differences:
            print("Differences found : This folder is not latest version.")
            for filename, diff in differences.items():
                print(f"Issued ATAC PC :  {filename[0:14]}")
                for item in diff:
                    print(f"  {item}")
        else:
            print("No differences found.")

    def find_all_keys(self, data_list, keys_set):
        for filename, data in data_list:
            for item in data:
                keys_set.add(item[0])

    def find_missing_keys(self, data_list, keys_set, missing_keys):
        for filename, items in data_list:
            item_keys = set(item[0] for item in items)
            missing = keys_set - item_keys
            if missing:
                missing_keys[filename] = missing

    def print_missing_keys(self, missing_keys):
        if missing_keys:
            print("Missing found : C:\\ATAC_Download\\")
            for filename, keys in missing_keys.items():
                print(f"Issued ATAC PC :  {filename[0:14]}")
                for key in keys:
                    print(f"  {key}")
        else:
            print("No missing keys found.")

    # def send_email(self, subject, body):
    #     outlook = win32com.client.Dispatch("Outlook.Application")
    #     mail = outlook.CreateItem(0)
    #     mail.To = "Insub.So@lamresearch.com"
    #     mail.Subject = subject
    #     mail.Body = body
    #
    #     try:
    #         mail.Send()
    #         print("Email sent successfully")
    #     except Exception as e:
    #         print(f"Failed to send email: {e}")

    def notify_results(self):
        subject = "SVN Version Monitoring , automatic notification email."
        body = ""

        if self.pm_missing_keys:
            body += "\n***** PM *****\n"
            body += "Missing found : C:\\ATAC_Download\\\n"
            for filename, keys in self.pm_missing_keys.items():
                body += f"Issued ATAC PC :  {filename[0:14]}\n"
                for key in keys:
                    body += f"  {key}\n"

        if self.be_missing_keys:
            body += "\n***** BE *****\n"
            body += "Missing found : C:\\ATAC_Download\\\n"
            for filename, keys in self.be_missing_keys.items():
                body += f"Issued ATAC PC :  {filename[0:14]}\n"
                for key in keys:
                    body += f"  {key}\n"

        if self.tp_missing_keys:
            body += "\n***** TP *****\n"
            body += "Missing found : C:\\ATAC_Download\\\n"
            for filename, keys in self.tp_missing_keys.items():
                body += f"Issued ATAC PC :  {filename[0:14]}\n"
                for key in keys:
                    body += f"  {key}\n"

        if self.pm_differences:
            body += "\n***** PM *****\n"
            body += "Differences found : This Model folder is not latest version.\n"
            for filename, diff in self.pm_differences.items():
                body += f"Issued ATAC PC :  {filename[0:14]}\n"
                for item in diff:
                    body += f"  {item}\n"

            body += "\n"
            for print_all_data in self.pm_data:
                body += f"{print_all_data}\n"

        if self.be_differences:
            body += "\n***** BE *****\n"
            body += "Differences found : This Model folder is not latest version.\n"
            for filename, diff in self.be_differences.items():
                body += f"Issued ATAC PC :  {filename[0:14]}\n"
                for item in diff:
                    body += f"  {item}\n"

            body += "\n"
            for print_all_data in self.be_data:
                body += f"{print_all_data}\n"

        if self.tp_differences:
            body += "\n***** TP *****\n"
            body += "Differences found : This Model folder is not latest version.\n"
            for filename, diff in self.tp_differences.items():
                body += f"Issued ATAC PC :  {filename[0:14]}\n"
                for item in diff:
                    body += f"  {item}\n"

            body += "\n"
            for print_all_data in self.tp_data:
                body += f"{print_all_data}\n"

        result = []
        result = self.comparison_rf_get_svn_version_and_rf_read_text_file()
        # print(result)
        # if result is not None:
        if result and all(not sublist for sublist in result):
            print("RF Cart result is a tuple of empty lists.")
        else:
            print("result is not None and contains non-empty lists.")
            body += "\n***** RF *****\n"
            body += "Issued ATAC PC :  CTC-KO-3004728"
            body += "Missing found : C:\\ATAC_Download\\\n"
            body += (f"rf_missing_model: {result[0]}\n")
            print(f"rf_missing_model: {result[0]}")
            body += "Differences found : This folder is not latest version.\n"
            print(f"rf_low_svn_rev: {result[1]}")
            body += (f"rf_low_svn_rev: {result[1]}\n")

        # if body:
        #     self.send_email(subject, body)
        st.write(body)

    def rf_get_svn_version(self, svn_path):
        try:
            result = subprocess.run(["svn", "info", svn_path], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                if line.startswith("Revision:"):
                    return line.split()[1]
        except subprocess.CalledProcessError as e:
            print(f"Error fetching SVN info for {svn_path}: {e}")
            return None

    def rf_read_text_file(self, file_path):
        versions = {}
        with open(file_path, 'r') as file:
            for line in file:
                model, version = line.strip().split(', ')
                versions[model] = version
        return versions

    def comparison_rf_get_svn_version_and_rf_read_text_file(self):
        rf_svn_paths = {
            "FlexGSRFCart": "https://pkor33mfgsvn01/svn/FlexGSRFCart/",
            "FlexHXPlusRFCart": "https://pkor33mfgsvn01/svn/FlexHXPlusRFCart/",
            "2300RFCart": "https://pkor33mfgsvn01/svn/2300RFCart/",
            "FlexJXPRFCart": "https://pkor33mfgsvn01/svn/FlexJXPRFCart/"
        }

        rf_svn_text_file_path = r"\\fre_filer03\2300testdata\PMATACConfig\Osan\activated_atac_pc_list\hwasung\svn_rev\CTC-KO-3004728_svn_revision.txt"

        server_versions = {model: self.rf_get_svn_version(path) for model, path in rf_svn_paths.items()}
        text_versions = self.rf_read_text_file(rf_svn_text_file_path)

        rf_missing_model = []
        rf_low_svn_rev = []
        for model, server_version in server_versions.items():
            text_version = text_versions.get(model)
            if text_version is None:
                print(f"Model: {model} is missing in the text file.")
                rf_missing_model.append(model)
            elif server_version != text_version:
                print(f"Model: {model} - Server Version: {server_version}, Text Version: {text_version}")
                rf_low_svn_rev.append({model, text_version})

        return rf_missing_model, rf_low_svn_rev


def button_to_check_the_svn_revision():
    # Usage
    directory = r"\\fre_filer03\\2300testdata\\PMATACConfig\\Osan\\activated_atac_pc_list\\hwasung\\svn_rev"
    pm_filenames = [
        "CTC-KO-6003075_svn_revision.txt",  # PM # 6
        "CTC-KO-2001354_svn_revision.txt",  # PM # 5
        "CTC-KO-6003226_svn_revision.txt",  # PM # 4
        "CTC-KO-6003221_svn_revision.txt",  # PM # 3
        "CTC-KO-6002754_svn_revision.txt",  # PM # 2
        "CTC-KO-6003223_svn_revision.txt",  # PM # 1
        "CTC-KO-7002354_svn_revision.txt",  # NPI # 1
        "CTC-KO-7002348_svn_revision.txt",  # NPI # 2
        "CTC-KO-5003908_svn_revision.txt",  # NPI # 3
    ]

    be_filenames = [
        "CTC-KO-9008168_svn_revision.txt",  # BE # 1
        "CTC-KO-2001348_svn_revision.txt",  # BE # 2
        "CTC-KO-2001344_svn_revision.txt",  # BE # 3
        "CTC-KO-6003215_svn_revision.txt",  # BE # 4
        "CTC-KO-9008166_svn_revision.txt",  # NPI BE # 5
        "CTC-KO-9008157_svn_revision.txt",  # NPI BE # 6
    ]


    tp_filenames = [
        "CTC-KO-6003224_svn_revision.txt",  # TP # 1
        "CTC-KO-2001357_svn_revision.txt",  # TP # 2
    ]

    processor = FileProcessor(directory, pm_filenames, be_filenames, tp_filenames)

    # Process PM files
    processor.process_files(pm_filenames, processor.pm_data)
    processor.find_all_keys(processor.pm_data, processor.pm_keys)
    processor.find_missing_keys(processor.pm_data, processor.pm_keys, processor.pm_missing_keys)
    # processor.print_missing_keys(processor.pm_missing_keys)
    processor.find_differences(pm_filenames, processor.pm_differences)
    # processor.print_differences(processor.pm_differences)
    # processor.print_all_data(processor.pm_data)

    # Process BE files
    processor.process_files(be_filenames, processor.be_data)
    processor.find_all_keys(processor.be_data, processor.be_keys)
    processor.find_missing_keys(processor.be_data, processor.be_keys, processor.be_missing_keys)
    # processor.print_missing_keys(processor.be_missing_keys)
    processor.find_differences(be_filenames, processor.be_differences)
    # processor.print_differences(processor.be_differences)
    # processor.print_all_data(processor.be_data)

    # Process TP files
    processor.process_files(tp_filenames, processor.tp_data)
    processor.find_all_keys(processor.tp_data, processor.tp_keys)
    processor.find_missing_keys(processor.tp_data, processor.tp_keys, processor.tp_missing_keys)
    # processor.print_missing_keys(processor.tp_missing_keys)
    processor.find_differences(tp_filenames, processor.tp_differences)
    # processor.print_differences(processor.tp_differences)
    # processor.print_all_data(processor.tp_data)


    # Notify results for both PM,BE and TP files
    processor.notify_results()


st.set_page_config(layout="wide")
st.title("ATAC PC SVN Revision Latest Version Monitoring.")
st.header("To check the SVN Revision status of Flex PC, click the button to proceed.")

st.write("Actual back data files is updated every Wednesday.")
st.write("This process will takes about 30 seconds.")
st.write("If the SVN revision is not up to date, it will be printed.")
# 버튼 생성
if st.button('To check the SVN Revision'):
    # st.write('버튼이 클릭 되었습니다!')

    progress_bar = st.progress(0)

    # button_to_check_the_svn_revision()
    threading.Thread(target=button_to_check_the_svn_revision).start()

    # 예시로 10단계로 나누어 진행 상태를 업데이트
    for i in range(30):
        time.sleep(0.5)  # 실제 작업을 여기에 추가
        progress_bar.progress((i + 1) / 30)

    # 성공 메시지 출력
    st.success("After checking the files being monitored and list that are out of date are printed.")

