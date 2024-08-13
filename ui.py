from tkinter import Tk, Button, Label, Entry, filedialog
import tnefparse

from quit import quit
from select_folder import select_folder
from send import send
from send_gateway import send_gateway


def ui():
    root = Tk()
    root.geometry("300x250")
    root.title("EML 파일들 전송하기")
    eml_location = ""

    def select_and_store_folder():
        nonlocal eml_location  # 외부 변수 eml_location을 사용할 수 있도록 지정
        eml_location = select_folder(eml_label)
        print(f"Selected folder: {eml_location}")  # 선택한 폴더 경로 출력 (디버그용)

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

    eml_button = Button(root, text="EML 파일 폴더 선택", command=select_and_store_folder)
    eml_button.grid(row=6, column=0, columnspan=2)

    eml_label = Label(root, text="")
    eml_label.grid(row=7, column=0, columnspan=2)

    send_button = Button(root, text="보내기", command=lambda: send_gateway(server_entry,
                                                                        port_entry,
                                                                        sender_entry,
                                                                        receiver_entry,
                                                                        delay_entry,
                                                                        retries_entry,
                                                                        eml_location,
                                                                        count_label,
                                                                        status_label))
    send_button.grid(row=8, column=0, columnspan=2)

    quit_button = Button(root, text="끝내기", command=lambda: quit(root))
    quit_button.grid(row=8, column=1, columnspan=2)

    count_label1 = Label(root, text="처리건수/총건수 : ")
    count_label1.grid(row=9, column=0)

    count_label = Label(root, text="")
    count_label.grid(row=9, column=1, columnspan=2)

    status_label = Label(root, text="")
    status_label.grid(row=10, column=0, columnspan=2)

    root.mainloop()
