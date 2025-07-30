"""mailing class that can send a mail as a dataframe or a string """

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd

class Mailing:
    def __init__(self, sender, password, receiver):
        self.sender = sender
        self.password = password
        self.receiver = receiver
    def send_mail(self, subject, mail):
        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = self.receiver
        message["Subject"] = subject
        try:
            # Convert DataFrame to HTML if mail is a DataFrame
            if isinstance(mail, pd.DataFrame):
                html_table = mail.to_html(index=False, classes="dataframe", border=0)
                html_content = f"""
                <html>
                <head>
                    <style>
                        .dataframe {{
                            font-family: Arial, sans-serif;
                            border-collapse: collapse;
                            width: 100%;
                        }}
                        .dataframe th {{
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                            background-color: #f2f2f2;
                        }}
                        .dataframe td {{
                            border: 1px solid #dddddd;
                            text-align: left;
                            padding: 8px;
                        }}
                        .dataframe tr:nth-child(even) {{
                            background-color: #f9f9f9;
                        }}
                    </style>
                </head>
                <body>
                    <p3>{subject}</p3>
                    {html_table}
                </body>
                </html>
                """
                message.attach(MIMEText(html_content, "html"))
            else:
                # For string content
                message.attach(MIMEText(mail, "plain"))
            # Connect to the server and start TLS encryption
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                # Login to email
                server.login(self.sender, self.password)
                # Send the email
                server.sendmail(self.sender, self.receiver, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
