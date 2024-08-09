import os
from email import policy
from email.parser import BytesParser
from email.message import EmailMessage
from email.generator import BytesGenerator


def extract_and_remove_dat_from_eml(eml_file_path, output_folder):
    # .eml 파일 읽기
    with open(eml_file_path, 'rb') as file:
        msg = BytesParser(policy=policy.default).parse(file)

    # .dat 파일을 추출하고 제거하기 위한 새 이메일 메시지 객체 생성
    new_msg = EmailMessage()

    if msg.is_multipart():
        # 멀티파트 메시지 처리
        for part in msg.iter_parts():
            if part.get_content_type() == 'application/octet-stream' and part.get_filename().endswith('.dat'):
                # .dat 파일 추출
                filename = part.get_filename()
                dat_file_path = os.path.join(output_folder, filename)
                with open(dat_file_path, 'wb') as dat_file:
                    dat_file.write(part.get_payload(decode=True))
            else:
                # .dat 파일을 제외한 나머지 부분을 새 이메일 메시지에 추가
                new_msg.attach(part)
    else:
        # 단일 파트 메시지 처리
        if msg.get_content_type() == 'application/octet-stream' and msg.get_filename().endswith('.dat'):
            # .dat 파일 추출
            filename = msg.get_filename()
            dat_file_path = os.path.join(output_folder, filename)
            with open(dat_file_path, 'wb') as dat_file:
                dat_file.write(msg.get_payload(decode=True))
        else:
            new_msg.set_content(msg.get_body(preferencelist=('plain', 'html')).get_content())

    # .dat 파일을 제거한 새 .eml 파일 저장
    new_eml_file_path = eml_file_path.replace('.eml', '_modified.eml')
    with open(new_eml_file_path, 'wb') as file:
        gen = BytesGenerator(file, policy=policy.default)
        gen.flatten(new_msg)

    return dat_file_path if 'dat_file_path' in locals() else None, new_eml_file_path


# 예제 사용법
eml_file_path = '/Users/dongik/Desktop/KIKI/hi.eml'
output_folder = '/Users/dongik/Desktop/KIKI/successed'

dat_file_path, new_eml_file_path = extract_and_remove_dat_from_eml(eml_file_path, output_folder)

if dat_file_path:
    print(f"Extracted .dat file saved as: {dat_file_path}")
print(f"Modified .eml file saved as: {new_eml_file_path}")
