import os
import smtplib
import shutil
import time
from email.parser import BytesParser
from email.message import EmailMessage
from email import policy
from tkinter import Tk, Button, Label, Entry, filedialog
import tnefparse

def send_eml_files():
    # Function to handle sending eml files

    def send():
        smtp_server = server_entry.get()
        smtp_port = int(port_entry.get())
        sender_email = sender_entry.get()
        receiver_email = receiver_entry.get()
        delay = float(delay_entry.get()) / 1000  # 이메일 전송사이의 시간(밀리초 단워)
        max_retries = int(retries_entry.get())  # 실패한 이메일에 대한 최대 재시도 횟수
        eml_folder = eml_label["text"]

        if not os.path.exists(eml_folder):
            status_label.config(text="폴더를 선택하세요.")
            return

        success_folder = os.path.join(eml_folder, "successed")
        if not os.path.exists(success_folder):
            os.makedirs(success_folder)

        eml_files = [os.path.join(eml_folder, file) for file in os.listdir(eml_folder) if file.endswith(".eml")]
        eml_total_count = len(eml_files)
        eml_processed_count = 0

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # server.ehlo()  # Can be omitted if not using TLS
                # server.starttls()  # Uncomment if using TLS
                # server.login(sender_email, password)  # Uncomment if authentication is required

                for eml_file in eml_files:
                    for attempt in range(max_retries):
                        try:
                            with open(eml_file, 'rb') as file:
                                eml_content = file.read()

                            msg = BytesParser(policy=policy.default).parsebytes(eml_content)

                            # Check if the message contains TNEF data
                            if msg.is_multipart():

                                for part in msg.iter_parts():
                                    # >>>>>>>>>>>>>>>>>>>
                                    tnef_data = part.get_payload(decode=True)
                                    tnef_message = tnefparse.TNEF(tnef_data)
                                    print("*")
                                    print(tnef_data)
                                    print("*>")
                                    print(tnef_message)

                                    # content_disposition = part.get_content_disposition()
                                    # if content_disposition == 'attachment':
                                    #     filename = part.get_filename()
                                    #     file_data = part.get_payload(decode=True)
                                    #     print(filename)
                                    #     try:
                                    #         # 텍스트 파일의 경우 내용을 디코딩하여 출력
                                    #         print("TXT")
                                    #         print(file_data)
                                    #     except UnicodeDecodeError:
                                    #         # 바이너리 파일인 경우 내용을 그대로 출력 (16진수로 변환할 수도 있음)
                                    #         print("BIN")
                                    #         print(file_data)  # 필요에 따라 수정 가능
                                    # >>>>>>>>>>>>>>>>>>>

                                    if part.get_content_type() == 'application/ms-tnef':
                                        tnef_data = part.get_payload(decode=True)
                                        tnef_message = tnefparse.TNEF(tnef_data)

                                        # Replace TNEF part with extracted parts
                                        for attachment in tnef_message.attachments:
                                            msg.add_attachment(
                                                attachment.data,
                                                maintype=attachment.mimetype.split('/')[0],
                                                subtype=attachment.mimetype.split('/')[1],
                                                filename=attachment.name,
                                                disposition='attachment',  # Disposition can be 'attachment' or 'inline'
                                                cid=None  # Content ID, if needed for inline display in HTML emails
                                            )
                                        print(type(msg))
                                        msg.remove(part)

                            # Ensure the message is in the correct format and encoding
                            if isinstance(msg, EmailMessage):
                                msg.set_charset('utf-8')

                            server.sendmail(sender_email, receiver_email, msg.as_string())
                            print(f"Sent: {eml_file}")

                            # Move the successfully sent email to the success folder
                            shutil.move(eml_file, success_folder)
                            break  # Exit the retry loop if successful

                        except Exception as e:
                            print(f"Error sending {eml_file} (attempt {attempt + 1}): {str(e)}")
                            time.sleep(2)  # Wait before retrying

                    else:
                        status_label.config(text=f"Failed to send {eml_file} after {max_retries} attempts.")

                    eml_processed_count += 1
                    eml_count_str = str(eml_processed_count) + '/' + str(eml_total_count)
                    count_label.config(text=eml_count_str)
                    time.sleep(delay)  # Wait between sending emails

            status_label.config(text="Emails sent successfully!")

        except Exception as e:
            status_label.config(text=f"Error:{str(e)}")

    # Function to select eml folder
    def select_eml_folder():
        eml_folder = filedialog.askdirectory()
        if eml_folder:
            eml_label.config(text=eml_folder)

    def quit_app():
        root.quit()
        root.destroy()

    # Create Tkinter window
    root = Tk()
    root.geometry("300x250")
    root.title("EML 파일들 전송하기")

    # Server settings
    server_label = Label(root, text="SMTP 서버:")
    server_label.grid(row=0, column=0)
    server_entry = Entry(root)
    server_entry.grid(row=0, column=1)

    port_label = Label(root, text="SMTP 포트:")
    port_label.grid(row=1, column=0)
    port_entry = Entry(root)
    port_entry.grid(row=1, column=1)

    sender_label = Label(root, text="송신 Email:")
    sender_label.grid(row=2, column=0)
    sender_entry = Entry(root)
    sender_entry.grid(row=2, column=1)

    receiver_label = Label(root, text="수신 Email:")
    receiver_label.grid(row=3, column=0)
    receiver_entry = Entry(root)
    receiver_entry.grid(row=3, column=1)

    delay_label = Label(root, text="메일전송 지연시간:")
    delay_label.grid(row=4, column=0)
    delay_entry = Entry(root)
    delay_entry.grid(row=4, column=1)

    retries_label = Label(root, text="실패메일 재시도 수:")
    retries_label.grid(row=5, column=0)
    retries_entry = Entry(root)
    retries_entry.grid(row=5, column=1)

    # EML folder selection
    eml_button = Button(root, text="EML 파일 폴더 선택", command=select_eml_folder)
    eml_button.grid(row=6, column=0, columnspan=2)
    eml_label = Label(root, text="")
    eml_label.grid(row=7, column=0, columnspan=2)

    # Send button
    send_button = Button(root, text="보내기", command=send)
    send_button.grid(row=8, column=0, columnspan=2)

    # 끝내기 버튼
    quit_button = Button(root, text="끝내기", command=quit_app)
    quit_button.grid(row=8, column=1, columnspan=2)

    # Count label
    count_label1 = Label(root, text="처리건수/총건수 : ")
    count_label1.grid(row=9, column=0)
    count_label = Label(root, text="")
    count_label.grid(row=9, column=1, columnspan=2)

    # Status label
    status_label = Label(root, text="")
    status_label.grid(row=10, column=0, columnspan=2)

    root.mainloop()

# Run GUI
send_eml_files()
