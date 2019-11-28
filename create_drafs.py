from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from email.mime.text import MIMEText
import base64

def create_message(sender, to, subject, message_text):
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject

	raw = base64.urlsafe_b64encode(message.as_string().encode())
	raw = raw.decode()
	return {'raw': raw}

SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
store = file.Storage('credentials/gmail.json')
creds = store.get()

#Rerun this if permission problems
#flow = client.flow_from_clientsecrets('credentials/gmail_client_secret.json', SCOPES)
#creds = tools.run_flow(flow, store)

connection = build('gmail', 'v1', http=creds.authorize(Http()))

TEMPLATE = 'HI {{NAME}}\nHow are you doing.'

for name, emailaddress in [('Wessel','wessel@wessel.nl'),('Belle','belle@belle.nl')]:

	body = TEMPLATE.replace('{{NAME}}',name)
	message = {'message': create_message('thesaplinggame@gmail.com',emailaddress,'Test',body)}
	draft = connection.users().drafts().create(userId='thesaplinggame@gmail.com', body=message).execute()