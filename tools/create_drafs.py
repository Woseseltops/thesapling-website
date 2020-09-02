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

TEMPLATE = '<p>Dear {name},</p><p>My name is Wessel Stoop and I am working on the indie evolution sim The Sapling. I am about to release a major update to the game, and I am looking for Youtubers that would be interested in showcasing it. If I\'m not mistaken I\'ve offered you a key before, but when looking for entertaining Youtubers that might be a good fit I keep ending up at your channel, so I\'m giving it another try.</p><p>This is the trailer for the update:</p><a href="https://www.youtube.com/watch?v=_aglK-7GFCI"><img width=540 src="https://thesaplinggame.com/static/png/FlowerUpdate_thumbnail.png"></a><p>I\'ve written a small key dispenser web application so I don\'t have to copypaste the keys manually: you can get your key here <a href="http://dispenser.thesaplinggame.com">http://dispenser.thesaplinggame.com</a> ; your password is the email address I\'m sending this to. The key will be shown only once, so make sure to store it somewhere save (or even better: enter it in Steam directly :) ). If you don\'t want to use my dispenser for some reason, or if something went wrong, let me know and I\'ll send you your key manually.</p><p>The flower update will be released exactly one week from now, so if you want to get the curious fanbase as your viewers, now is the time :). Let me know if you have any questions, or if something does not work. Also let me know if you have any questions or want to do something special (for example talking to me while playing). Some more information about the game:</p><ul><li>My previous video, first look: <a href="https://www.youtube.com/watch?v=-tFe4_-7cFA">https://www.youtube.com/watch?v=-tFe4_-7cFA</a></li><li>Website: <a href="https://thesaplinggame.com/">https://thesaplinggame.com/</a></li><li>Twitter: <a href="https://twitter.com/thesaplinggame">@thesaplinggame</a></li><li>Press kit: <a href="https://thesaplinggame.com/press/sheet.html">https://thesaplinggame.com/press/sheet.html</a></li><li>Newsletter: <a href="https://thesaplinggame.com/newsletter">https://thesaplinggame.com/newsletter</a></li></ul><p>Best,<br>Wessel Stoop</p><img width=540 src="https://thesaplinggame.com/static/png/FlowerUpdate_cliff.png"><img width=540 src="https://thesaplinggame.com/static/png/FlowerUpdate_plant.png">'

for line in open('input',encoding='utf-8'):

	youtuber, name, email = line.strip().split('\t')

	if name in ['',None]:
		best_name = 'creator of the YouTube channel '+youtuber
	else:
		best_name = name

	message = {'message': create_message('thesaplinggame@gmail.com',email,'Interested in Steam key for indie evolution sim The Sapling?',TEMPLATE.replace('{name}',best_name))}
	connection.users().drafts().create(userId='thesaplinggame@gmail.com', body=message).execute()