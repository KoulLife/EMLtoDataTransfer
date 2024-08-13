import os
import smtplib
import shutil
import time
from email.parser import BytesParser
from email.message import EmailMessage
from email import policy
from tkinter import Tk, Button, Label, Entry, filedialog
import tnefparse

from separate_dat import check_eml_in_folder

def select_folder(eml_label):
    eml_folder = filedialog.askdirectory()
    if eml_folder:
        eml_label.config(text=eml_folder)

        return eml_folder
