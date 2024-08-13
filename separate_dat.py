import os
import email
from email import policy
from email.parser import BytesParser
from email.message import EmailMessage
import base64
from tkinter import Tk, Button, Label, Entry, filedialog

from export_dat import unzip_dat
from collect_eml import create_eml


# .dat파일 추출
def export_dat(eml_file_path):
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

    # 이메일의 각 파트를 순회
    for part in msg.walk():
        # 파일이 첨부파일이고, 확장자가 .dat인 경우
        if part.get_content_disposition() == 'attachment' and part.get_filename().endswith('.dat'):
            dat_filename = part.get_filename()
            dat_data = part.get_payload(decode=True)  # Base64 디코딩

    return dat_data


# .dat파일 삭제 후 eml
def export_eml(eml_file_path):
    # .eml 파일 열기 및 파싱
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

    # 새로운 메시지 생성
    new_msg = EmailMessage()

    # 기존 메시지의 헤더 복사
    for header, value in msg.items():
        new_msg[header] = value

    # 첨부파일 제거하면서 메시지의 각 파트를 순회
    for part in msg.iter_parts():
        # winmail.dat이 아닌 모든 파트를 새로운 메시지에 추가
        if not (part.get_filename() and part.get_filename().endswith('.dat')):
            new_msg.attach(part)

    return new_msg.as_bytes()


def check_eml_in_folder(eml_folder):
    # 선택된 폴더 내의 모든 .eml 파일을 처리
    for eml_file in os.listdir(eml_folder):
        if eml_file.endswith(".eml"):
            eml_file_path = os.path.join(eml_folder, eml_file)

            file_paths = unzip_dat(export_dat(eml_file_path))
            msg = export_eml(eml_file_path)

            return create_eml(file_paths, msg)
