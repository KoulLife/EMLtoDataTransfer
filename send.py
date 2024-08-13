import os
import smtplib
import shutil
import time
from email.parser import BytesParser
from email import policy

def send(server_entry, port_entry, sender_entry, receiver_entry, delay_entry, retries_entry, eml_folder, count_label,
         status_label):
    smtp_server = server_entry.get()
    smtp_port = int(port_entry.get())
    sender_email = sender_entry.get()
    receiver_email = receiver_entry.get()
    delay = float(delay_entry.get()) / 1000  # 이메일 전송 사이의 시간(밀리초 단위)
    max_retries = int(retries_entry.get())  # 실패한 이메일에 대한 최대 재시도 횟수

    if not os.path.exists(eml_folder):
        status_label.config(text="폴더를 선택하세요.")
        return

    success_folder = os.path.join(eml_folder, "successed")
    if not os.path.exists(success_folder):
        os.makedirs(success_folder)

    eml_files = [os.path.join(eml_folder, file) for file in os.listdir(eml_folder) if file.endswith(".eml")]

    # eml 파일의 총 수
    eml_total_count = len(eml_files)
    eml_processed_count = 0

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            for eml_file in eml_files:
                for attempt in range(max_retries):
                    try:
                        with open(eml_file, 'rb') as file:
                            eml_content = file.read()

                        # .eml 파일을 이메일 메시지로 파싱
                        msg = BytesParser(policy=policy.default).parsebytes(eml_content)

                        # 이메일 전송
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                        print(f"Sent: {eml_file}")

                        # 전송된 이메일을 성공 폴더로 이동
                        shutil.move(eml_file, success_folder)
                        break  # 성공하면 재시도 루프 탈출

                    except Exception as e:
                        print(f"Error sending {eml_file} (attempt {attempt + 1}): {str(e)}")
                        time.sleep(2)  # 재시도 전에 잠시 대기

                else:
                    status_label.config(text=f"Failed to send {eml_file} after {max_retries} attempts.")

                eml_processed_count += 1
                eml_count_str = f"{eml_processed_count}/{eml_total_count}"
                count_label.config(text=eml_count_str)
                time.sleep(delay)  # 이메일 전송 간 대기 시간

        status_label.config(text="Emails sent successfully!")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
