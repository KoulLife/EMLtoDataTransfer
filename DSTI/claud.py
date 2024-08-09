def send_emails(self):
    smtp_server = self.smtp_server.get()
    smtp_port = int(self.smtp_port.get())
    sender_email = self.sender_email.get()
    receiver_email = self.receiver_email.get()
    folder_path = self.folder_path.get()

    try:
        # Try SSL connection first
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                self.process_emails(server, sender_email, receiver_email, folder_path)
        except smtplib.SMTPException:
            # If SSL fails, try TLS
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                try:
                    server.starttls()
                except smtplib.SMTPException:
                    # If TLS fails, try without encryption
                    pass
                self.process_emails(server, sender_email, receiver_email, folder_path)

        messagebox.showinfo("Success", "Emails sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def process_emails(self, server, sender_email, receiver_email, folder_path):
    # Note: You might need to add login credentials here
    # server.login(username, password)

    for filename in os.listdir(folder_path):
        if filename.endswith('.eml'):
            with open(os.path.join(folder_path, filename), 'r') as eml_file:
                eml_content = eml_file.read()

            msg = message_from_file(eml_file)
            new_msg = MIMEMultipart()
            new_msg['From'] = sender_email
            new_msg['To'] = receiver_email
            new_msg['Subject'] = msg['Subject']

            # Add .eml content to the email body
            new_msg.attach(MIMEText(eml_content, 'plain'))

            # Attach .dat files
            for part in msg.walk():
                if part.get_content_maintype() == 'application' and part.get_filename().endswith('.dat'):
                    attachment = MIMEApplication(part.get_payload(decode=True), Name=part.get_filename())
                    attachment['Content-Disposition'] = f'attachment; filename="{part.get_filename()}"'
                    new_msg.attach(attachment)

            server.send_message(new_msg)