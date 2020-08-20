from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from email.mime.text import MIMEText
import base64

from youtubers import batch_youtubers, game_list_to_description

def create_message(sender, to, subject, message_text):
	message = MIMEText(message_text,'html')
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

PRESS_CONTACT_FILE = 'press-overview'

TEMPLATE = '<p>Dear {name},</p><p>My name is Wessel Stoop and I am working on the indie evolution sim The Sapling. I am about to release a major update to the game, and I am looking for Youtubers that would be interested in showcasing it. I think your channel is very cool and was thinking it might be a good fit, among other things because you played the {games}. This is the trailer for the update:</p><a href="https://www.youtube.com/watch?v=_aglK-7GFCI"><img width=540 src="https://thesaplinggame.com/static/png/FlowerUpdate_thumbnail.png"></a><p>I am planning to send you a key for the update in the week of September 3, so you can already play it ahead of the crowd if you want to. In case you are not interested, it would be great if you could let me know, so I can send your key to somebody else!</p><p>Also let me know if you have any questions or want to do something special (for example talking to me while playing). Some more information about the game:</p><ul><li>My previous video, first look: <a href="https://www.youtube.com/watch?v=-tFe4_-7cFA">https://www.youtube.com/watch?v=-tFe4_-7cFA</a></li><li>Website: <a href="https://thesaplinggame.com/">https://thesaplinggame.com/</a></li><li>Twitter: <a href="https://twitter.com/thesaplinggame">@thesaplinggame</a></li><li>Press kit: <a href="https://thesaplinggame.com/press/sheet.html">https://thesaplinggame.com/press/sheet.html</a></li><li>Newsletter: <a href="https://thesaplinggame.com/newsletter">https://thesaplinggame.com/newsletter</a></li></ul><p>Best,<br>Wessel Stoop</p><img width=540 src="https://thesaplinggame.com/static/png/FlowerUpdate_cliff.png"><img width=540 src="https://thesaplinggame.com/static/png/FlowerUpdate_plant.png">'

batches = batch_youtubers()
current_batch = batches[2]
print(len(current_batch))

for youtuber in current_batch:

	message = {'message': create_message('thesaplinggame@gmail.com',youtuber.email,'Interested in Steam key for indie evolution sim The Sapling?',TEMPLATE.replace('{name}',youtuber.best_name).replace('{games}',game_list_to_description(youtuber.games)))}
	connection.users().drafts().create(userId='thesaplinggame@gmail.com', body=message).execute()