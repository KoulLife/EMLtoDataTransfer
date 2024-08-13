import os
import smtplib
import shutil
import time
from email.parser import BytesParser
from email.message import EmailMessage
from email import policy
from tkinter import Tk, Button, Label, Entry, filedialog
import tnefparse

def quit(root):
    root.quit()
    root.destroy()