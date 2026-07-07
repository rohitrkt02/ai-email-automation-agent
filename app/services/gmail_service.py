import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scope to allow reading, updating, and sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Handles OAuth2 authentication and token generation/refresh."""
        token_path = os.path.join('config', 'token.json')
        creds_path = os.path.join('config', 'credentials.json')

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception:
                    self.creds = None

            if not self.creds:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(
                        f"CRITICAL: Credentials file not found at '{creds_path}'."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
                
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)
        print("[INFO] Gmail API successfully authenticated.")

    # FIX HERE: Make sure timeframe="1d" parameter is explicitly present
    def get_unread_emails(self, max_results=5, timeframe="1d"):
        """
        Fetches unread emails from the primary inbox within a specific timeframe.
        """
        try:
            # Query utilizing timeframe filter
            query = f"is:unread category:primary newer_than:{timeframe}"
            
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []

            for msg in messages:
                txt = self.service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                payload = txt.get('payload', {})
                headers = payload.get('headers', [])

                subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), "No Subject")
                sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), "Unknown Sender")
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
            
            if not subject.lower().startswith('re:'):
                subject = f"Re: {subject}"

            message = MIMEText(body)
            message['to'] = to_email
            message['from'] = 'me'
            message['subject'] = subject
            
            raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode(), 'threadId': thread_id}
            
            send_result = self.service.users().messages().send(userId='me', body=raw_message).execute()
            print(f"[INFO] Reply sent successfully to {to_email}. Message ID: {send_result['id']}")
            return send_result
        except HttpError as error:
            print(f"[ERROR] An error occurred while sending email: {error}")
            return None