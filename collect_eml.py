import shutil
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders, policy
import mimetypes
import os
from email.parser import BytesParser


def add_attachment(msg, file_path):
    # 파일의 MIME 타입과 서브타입을 추정
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    # MIME 타입에서 메인 타입과 서브 타입을 분리
    main_type, sub_type = mime_type.split("/", 1)

    # 파일 내용을 읽어서 MIME 객체 생성
    with open(file_path, "rb") as f:
        if main_type == "text" and sub_type != "html":
            try:
                part = MIMEText(f.read().decode('utf-8'), _subtype=sub_type)
            except UnicodeDecodeError:
                part = MIMEText(f.read().decode('latin-1'), _subtype=sub_type)
        else:
            # HTML 파일이거나 다른 타입의 파일인 경우
            part = MIMEBase(main_type, sub_type)
            part.set_payload(f.read())
            encoders.encode_base64(part)

    # 첨부파일로 파일 추가
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(file_path)}",
    )
    msg.attach(part)

def delete_eml_folder(eml_folder_path):
    if os.path.exists(eml_folder_path) and os.path.isdir(eml_folder_path):
        shutil.rmtree(eml_folder_path)
        print(f"Folder '{eml_folder_path}' has been deleted.")
    else:
        print(f"Folder '{eml_folder_path}' does not exist or is not a directory.")


def create_eml(file_paths, msg, output_file):
    print("****output : " + output_file)
    # 이메일 메시지 객체 생성
    msg = BytesParser(policy=policy.default).parsebytes(msg)

    # 파일을 하나씩 추가
    for file_path in file_paths:
        add_attachment(msg, file_path)

    # 'export_eml' 폴더 생성
    output_directory = "./unzip//export_eml"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 'export_eml' 폴더 내에 output.eml 파일 저장
    output_path = os.path.join(output_directory, output_file)
    with open(output_path, "w") as f:
        f.write(msg.as_string())

    print(f"EML 파일이 생성되었습니다: {output_path}")
    delete_eml_folder("./unzip//extracted_dat_files")

    return output_path
