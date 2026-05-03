import smtplib
from email.message import EmailMessage
from Constant import Constant as const

class EmailConfig:
    SENDER = const.SENDER_EMAIL_ID
    PASSWORD = const.GOOGLE_EMAIL_PASS
    SERVER = const.SERVER_NAME
    PORT = const.PORT

class EmailSender:
    
    def __init__(self):
        print('Email Sender initialized')
    
    def get_attachment_data(self):
        """Reads the file once to save memory/processing power."""
        try:
            with open(const.FILE_PATH, 'rb') as f:
                return f.read(), "Vikranth_Resume.pdf"
        except FileNotFoundError:
            print(f"Error: Resume file not found at {const.FILE_PATH}")
            return None, None

    def send_email(self, jsonList):
        # 1. Load the attachment once
        file_data, file_name = self.get_attachment_data()
        if not file_data:
            return

        try:
            # 2. Open connection once
            with smtplib.SMTP(EmailConfig.SERVER, EmailConfig.PORT) as server:
                server.starttls()
                print("Logging in...")
                server.login(EmailConfig.SENDER, EmailConfig.PASSWORD)

                for person in jsonList:
                    try:
                        msg = EmailMessage()
                        msg['Subject'] = person.get('email_subject', "Salesforce Application.") 
                        msg['From'] = EmailConfig.SENDER
                        msg['To'] = person.get('career_email_id', "fallback@example.com")
                        msg.set_content(person.get('email_draft', "Please find my application attached."))
                        
                        # 3. Attach the pre-loaded file
                        msg.add_attachment(
                            file_data,
                            maintype='application',
                            subtype='pdf',
                            filename=file_name
                        )
                        
                        server.send_message(msg)
                        print(f"Successfully sent to: {person.get('application_id', 'Unknown ID')}")
                    
                    except Exception as e:
                        # Individual email failure shouldn't stop the whole script
                        print(f"Failed to send to {person.get('application_id')}: {e}")

        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Check your email/app password.")
        except Exception as e:
            print(f"A connection error occurred: {e}")


'''
# REPLACE THESE TWO STRINGS
MY_EMAIL = "vikranthpuvvadi@gmail.com"  # Ensure the 'l' is there!
MY_APP_PASS = const.GOOGLE_EMAIL_PASS          # NO SPACES

try:
    print("Step 1: Connecting to Gmail...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    
    print("Step 2: Starting TLS...")
    server.starttls()
    
    print(f"Step 3: Attempting login for {MY_EMAIL}...")
    server.login(MY_EMAIL, MY_APP_PASS)
    
    print("✅ SUCCESS! Your account and password are working.")
    server.quit()

except smtplib.SMTPAuthenticationError:
    print("❌ FAILED: Username or App Password rejected by Google.")
    print("Check: 1. Is 2-Step Verification ON? 2. Is this a 16-letter App Pass?")
except Exception as e:
    print(f"❌ AN ERROR OCCURRED: {e}")
'''