from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from email.mime.text import MIMEText
import base64

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

SUBJECT = 'The Sapling available: "This is what Spore should have been" (Steam key included)'
TEMPLATE = '<html><body><p>PLEASE ONLY PUBLISH DECEMBER 12 OR LATER</p><h1>The Sapling available today: "This is what Spore should have been"</h1><h4>Wessel Stoop wanted to play with evolution in the SIMULATION genre, so the only option was to build it himself.</h4><p>Nijmegen, The Netherlands - December 12, 2019 - Today evolution sim The Sapling, a short indie game by Wessel Stoop, is officially available on Steam in Early Access (and also on itch.io, Kartridge and Gamejolt). The Sapling is a simulation game where you design your own plants and animals, and put them in a world together. Or you turn on random mutations, and see what evolution does to your ecosystem!</p><p>Wessel Stoop has wanted to play a simulation game where you can build your own plants and animals, put them in a world, and see what happens since 2002. You can imagine his excitement when Will Wright, the father of simulation games, demoed his latest game Spore to an enthusiastic crowd. "Checking several Spore related news sites was the first I did when I opened up a web browser these days", says Stoop. When Spore turned out to be all game genres except simulation, he decided he wanted to try to make the game by himself. The Sapling is the result of that attempt.</p><p>Players can start simulating evolution here: https://store.steampowered.com/app/997380/The_Sapling</p><img width=500 src="https://thesaplinggame.com/press/The%20Sapling/images/AnimalEditor.png"><br><img width=500 src="https://thesaplinggame.com/press/The%20Sapling/images/SoilLevel.png"><p><strong>Features</strong></p><ul><li>Fast-forward time to and watch the ecosystem work like a charm or slowly fall apart (probably the latter :) ).</li><li>A sandbox mode where you can skip time and turn on random mutation, allowing true evolution.</li><li>An instinct system where you can specify what an animal should do when it hears or sees something.</li><li>A procedural animation system so any animal can perform any animation.</li><li>Procedural music mixed on the fly.</li><li>Everything set up to be easily extended by players.</li></ul><p><strong>Quotes from playtesters</strong></p><ul><li>"This is what Spore should have been."</li><li>To the other playtesters waiting in line: "Have you seen this? Have you seen this? Look at this! Have you seen this?"</li><li>I like how I can give this plant a little penis</li></ul><p><strong>Your Steam key</strong></p><p>xxx</p><p><strong>Links that might be useful</p></strong><ul><li>Press kit: <a href="https://thesaplinggame.com/press/sheet.html">https://thesaplinggame.com/press/sheet.html</a></li><li>Subscribe to the newsletter: <a href="https://mailchi.mp/b85a701ccf0e/thesapling">https://mailchi.mp/b85a701ccf0e/thesapling</a></li><li>Website: <a href="https://thesaplinggame.com/">https://thesaplinggame.com/</a></li><li>First look video: <a href="https://www.youtube.com/watch?v=-tFe4_-7cFA">https://www.youtube.com/watch?v=-tFe4_-7cFA</a></li><li>More (interactive!) details on the simulation: <a href="https://thesaplinggame.com/devlogs/modelsrelease.html">https://thesaplinggame.com/devlogs/modelsrelease.html</a></li></ul><p><strong>About me</strong></p><p>Wessel Stoop<br>Nijmegen, The Netherlands<br><a>http://wesselstoop.ruhosting.nl/</a></p><p>Email: thesaplinggame@gmail.com<br>Twitter: <a href="https://twitter.com/thesaplinggame">@thesaplinggame</a></p><p>I am very open to interviews, either via Skype or e-mail.</p></body></html>'

DRAFT_ID = 'r-6416627266572108012'
draft = connection.users().drafts().get(id=DRAFT_ID,userId='me').execute()


for name, emailaddress in [('Wessel','wessel@wessel.nl'),('Belle','belle@belle.nl')]:

    body = TEMPLATE.replace('{{NAME}}',name)
    message = {'message': create_message('thesaplinggame@gmail.com',emailaddress,SUBJECT,body)}
    connection.users().drafts().create(userId='thesaplinggame@gmail.com', body=message).execute()