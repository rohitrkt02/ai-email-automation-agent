import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Humne jo scope Google Cloud par select kiya tha, wahi yahan define karenge
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Handles OAuth2 authentication and token generation/refresh."""
        # token.json automatic generate hogi pehli baar login karne ke baad
        token_path = os.path.join('config', 'token.json')
        creds_path = os.path.join('config', 'credentials.json')

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
        # Agar credentials valid nahi hain ya expire ho gaye hain, toh refresh/login karein
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(f"Error: '{creds_path}' nahi mili! Pehle Google Cloud se ise download karein.")
                
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
                
            # Agli baar ke liye token save kar lein
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

        # Gmail API Service client build karein
        self.service = build('gmail', 'v1', credentials=self.creds)
        print("[INFO] Gmail API successfully authenticated.")

    def get_unread_emails(self, max_results=5):
        """Fetches a list of unread emails from the inbox."""
        try:
            # Sirf UNREAD emails jo INBOX me hain unhe fetch karne ke liye query
            results = self.service.users().messages().list(
                userId='me', q='is:unread category:primary', maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []

            for msg in messages:
                # Har email ki detailed information nikalna
                txt = self.service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                payload = txt.get('payload', {})
                headers = payload.get('headers', [])

                # Headers se Subject, Sender aur Date parse karna
                subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), "No Subject")
                sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), "Unknown Sender")
                
                # Email body extract karna (Snippet utility standard output ke liye)
                snippet = txt.get('snippet', '')

                email_list.append({
                    'id': msg['id'],
                    'threadId': msg['threadId'],
                    'sender': sender,
                    'subject': subject,
                    'body': snippet
                })
            return email_list

        except HttpError as error:
            print(f"[ERROR] An error occurred while fetching emails: {error}")
            return []

    def send_reply(self, to_email, subject, body, thread_id):
        """Sends an automated email reply inside the specific thread."""
        try:
            from email.mime.text import MIMEText
            
            # Agar subject me Re: nahi hai toh standard thread flow ke liye add karein
            if not subject.lower().startswith('re:'):
                subject = f"Re: {subject}"

            message = MIMEText(body)
            message['to'] = to_email
            message['from'] = 'me'
            message['subject'] = subject
            
            # Threading maintain karne ke liye threadId pass karna zaroori hai
            raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode(), 'threadId': thread_id}
            
            send_result = self.service.users().messages().send(userId='me', body=raw_message).execute()
            print(f"[INFO] Reply sent successfully to {to_email}. Message ID: {send_result['id']}")
            return send_result
        except HttpError as error:
            print(f"[ERROR] An error occurred while sending email: {error}")
            return None