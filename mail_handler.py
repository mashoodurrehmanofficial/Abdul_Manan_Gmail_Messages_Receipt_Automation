# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import os
import email
from bs4 import BeautifulSoup
try:
    from .data_extractor import EXTRACT_DATA_FROM_BODY
    from .template_generator import GENERATE_TEMPLATE_IMAGE
    from .apis import singleMessageApi
except:
    from data_extractor import EXTRACT_DATA_FROM_BODY
    from template_generator import GENERATE_TEMPLATE_IMAGE
    from apis import singleMessageApi


target_subject_key = 'New China Cuisine - Order'
orignal_creds = os.path.join(os.getcwd(), 'data', 'orignal_creds.json')


from datetime import  *
import time

 






# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def getEmails():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                orignal_creds, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # request a list of all the messages
    print("-->> Getting first 50 messages")
    
    today = datetime.now().today()
    date  = datetime(today.year, today.month, today.day, 0, 0)
    seconds  =time.mktime(date.timetuple())
        
    tomorrow = datetime.now().today().date() + timedelta(1)
    today = datetime.now().today().date()
    
        
    query = f"after: {today}"    
    result = service.users().messages().list(maxResults=50, userId='me', labelIds=['INBOX'],q=query).execute()
    messages = result.get('messages')


    print(len(messages))

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    for msg_index, msg in enumerate(messages[:0]):
        # Get the message from its id
        txt = service.users().messages().get(
            userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)
            soup = BeautifulSoup(decoded_data, "lxml")

            if target_subject_key in str(subject):
                body = BeautifulSoup(decoded_data, "lxml").select('html')[
                    0].text.strip().replace('\n\n', '\n')
                with open(f"email_body_received.txt", 'w', encoding="utf-8")as file:
                    file.write(str(body))

                # print(subject, '-->',msg['id'])
                response = singleMessageApi(msg['id'])
                # if response == 0:
                #     break

                # data = EXTRACT_DATA_FROM_BODY(file_path = f"email_body_received.txt",lang='eng')
                # GENERATE_TEMPLATE_IMAGE(data)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)
            pass


if __name__ == "__main__":
    getEmails()
