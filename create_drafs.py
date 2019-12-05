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

PRESS_CONTACT_FILE = 'press-overview'

SUBJECT, TEMPLATE = {},{}
SUBJECT['en'] = 'The Sapling available: "This is what Spore should have been" (Steam key included)'
TEMPLATE['en'] = '<html><body><p>PLEASE ONLY PUBLISH DECEMBER 12 OR LATER</p><h1>The Sapling available in Early Access today: "This is what Spore should have been"</h1><h4>Wessel Stoop wanted to play with evolution in the SIMULATION genre, so the only option was to build it himself.</h4><p>Nijmegen, The Netherlands - December 12, 2019 - Today evolution sim The Sapling, a short indie game by Wessel Stoop, is officially available on Steam in Early Access (and also on itch.io, Kartridge and Gamejolt). The Sapling is a simulation game where you design your own plants and animals, and put them in a world together. Or you turn on random mutations, and see what evolution does to your ecosystem!</p><p>Wessel Stoop has wanted to play a simulation game where you can build your own plants and animals, put them in a world, and see what happens since 2002. You can imagine his excitement when Will Wright, the father of simulation games, demoed his latest game Spore to an enthusiastic crowd. "Checking several Spore related news sites was the first I did when I opened up a web browser these days", says Stoop. When Spore turned out to be all game genres except simulation, he decided he wanted to try to make the game by himself. The Sapling is the result of that attempt.</p><p>Players can start simulating evolution here: <a href="https://store.steampowered.com/app/997380/The_Sapling">https://store.steampowered.com/app/997380/The_Sapling</a></p><img width=500 src="https://thesaplinggame.com/press/The%20Sapling/images/AnimalEditor.png"><br><img width=500 src="https://thesaplinggame.com/press/The%20Sapling/images/SoilLevel.png"><p><strong>Features</strong></p><ul><li>Fast-forward time to and watch the ecosystem work like a charm or slowly fall apart (probably the latter :) ).</li><li>A sandbox mode where you can skip time and turn on random mutation, allowing true evolution.</li><li>An instinct system where you can specify what an animal should do when it hears or sees something.</li><li>A procedural animation system so any animal can perform any animation.</li><li>Procedural music mixed on the fly.</li><li>Everything set up to be easily extended by players.</li></ul><p><strong>Quotes from playtesters</strong></p><ul><li>"This is what Spore should have been."</li><li>To the other playtesters waiting in line: "Have you seen this? Have you seen this? Look at this! Have you seen this?"</li><li>"I like how I can give this plant a little penis"</li></ul><p><strong>Your Steam key</strong></p><p>xxx</p><p><strong>Links that might be useful</p></strong><ul><li>Press kit: <a href="https://thesaplinggame.com/press/sheet.html">https://thesaplinggame.com/press/sheet.html</a></li><li>Subscribe to the newsletter: <a href="https://mailchi.mp/b85a701ccf0e/thesapling">https://mailchi.mp/b85a701ccf0e/thesapling</a></li><li>Website: <a href="https://thesaplinggame.com/">https://thesaplinggame.com/</a></li><li>First look video: <a href="https://www.youtube.com/watch?v=-tFe4_-7cFA">https://www.youtube.com/watch?v=-tFe4_-7cFA</a></li><li>More (interactive!) details on the simulation: <a href="https://thesaplinggame.com/devlogs/modelsrelease.html">https://thesaplinggame.com/devlogs/modelsrelease.html</a></li></ul><p><strong>About me</strong></p><p>Wessel Stoop<br>Nijmegen, The Netherlands<br><a>http://wesselstoop.ruhosting.nl/</a></p><p>Email: thesaplinggame@gmail.com<br>Twitter: <a href="https://twitter.com/thesaplinggame">@thesaplinggame</a></p><p>I am very open to interviews, either via Skype or e-mail.</p></body></html>'
SUBJECT['nl'] = 'The Sapling beschikbaar: "Dit is wat Spore had moeten zijn" (incl Steam key)'
TEMPLATE['nl'] = '<html><body><p>GRAAG PAS 12 DECEMBER OF LATER PUBLICEREN</p><h1>The Sapling vandaag beschikbaar in Early Access: "Dit is wat Spore had moeten zijn"</h1><h4>Wessel Stoop wilde een SIMULATIEspel over evolutie, dus de enige optie was om het zelf te bouwen.</h4><p>Nijmegen - 12 december 2019 - Vandaag is evolutiesim The Sapling, een korte indiegame door Wessel Stoop, officieel beschikbaar op Steam as Early Access-titel (en ook op itch.io, Kartridge en GameJolt). The Sapling is een simulatiegame waar je je eigen planten en dieren kan ontwerpen, en ze dan samen in een wereld zet. Of zet <em>random mutations</em> aan, en kijk toe wat evolutie doet met je ecosysteem!</p><p>Al sinds 2002 wilde Wessel Stoop een spel spelen waar je je eigen planten en dieren kunt maken, om ze vervolgens samen in een wereld te zetten. Zijn enthousiasme toen Will Wright, nota bene de vader van de simulatiegames, Spore aankondigde, was dan ook ongekend: "meerdere Spore-nieuwswebsites checken was het eerste wat ik deed zodra ik een browser opende in die tijd", zegt Stoop. Toen duidelijk dat Spore zo\'n beetje alle genres was behalve simulatie, besloot hij om het spel zelf maar proberen te maken. The Sapling is het resultaat van die poging.</p><p>Hier kun je beginnen met het simuleren van evolutie: <a href="https://store.steampowered.com/app/997380/The_Sapling">https://store.steampowered.com/app/997380/The_Sapling</a><p><strong>Features</strong></p><ul><li>Versnel de tijd en kijk hoe je ecosysteem draait als een geoliede machine of langzaam uit elkaar valt (waarschijnlijk dat laatste :) )</li><li>Een sandboxmodus waar je grote sprongen in de tijd kunt maken en <em>random mutations</em> aan kunt zetten, zodat je echte evolutie aan het werk ziet.</li><li>Een instinct-systeem waarmee je instellen hoe een dier reageert als iets ziet ziet of hoort.</li><li>Procedurele animatie zodat elk dier elke animatie kan uitvoeren.</li><li>Procedurele muziek die tijdens de game gemixt wordt.</li><li>De hele game is zo opgezet dat creatieve spelers het makkelijk kunnen uitbreiden.</li></ul><p><strong>Quotes van playtesters</strong></p><ul><li>"Dit is wat Spore had moeten zijn."</li><li>Tegen de andere mensen die in de rij stonden te wachten: "Heb je dit gezien? Heb je dit gezien? Moet je kijken! Heb je dit gezien?"</li><li>"Deze plant geef ik een klein piemeltje." (Adriaan de Jongh)</li></ul><p><strong>De Steam key</strong></p>xxx<p><strong>Links die nuttig kunnen zijn</strong></p><ul><li>Perskit: <a href="https://thesaplinggame.com/press/sheet.html">https://thesaplinggame.com/press/sheet.html</a></li><li>Schrijf je in voor de nieuwsbrief: <a href="https://mailchi.mp/b85a701ccf0e/thesapling">https://mailchi.mp/b85a701ccf0e/thesapling</a></li><li>Website: <a href="https://thesaplinggame.com/">https://thesaplinggame.com/</a></li><li>First look video: <a href="https://www.youtube.com/watch?v=-tFe4_-7cFA">https://www.youtube.com/watch?v=-tFe4_-7cFA</a></li><li>Meer interactieve details over de simulatie: <a href="https://thesaplinggame.com/devlogs/modelsrelease.html">https://thesaplinggame.com/devlogs/modelsrelease.html</a></li></ul><p><strong>Over mij</strong></p><p>Wessel Stoop<br>Nijmegen, The Netherlands<br>http://wesselstoop.ruhosting.nl/<p><p>Email: thesaplinggame@gmail.com<br>Twitter: <a href="https://twitter.com/thesaplinggame">@thesaplinggame</a></p><p>Ik sta zeer open voor interviews, via Skype of email</p></body></html>'

DRAFT_ID = 'r-6416627266572108012'
draft = connection.users().drafts().get(id=DRAFT_ID,userId='me').execute()

for line in open(PRESS_CONTACT_FILE):

	print(line)
	if '#STOP' in line:
		break

	name, language, emailaddress, key = line.strip().split('\t')

	body = TEMPLATE[language].replace('{{NAME}}',name).replace('xxx',key)
	message = {'message': create_message('thesaplinggame@gmail.com',emailaddress,SUBJECT[language],body)}
	connection.users().drafts().create(userId='thesaplinggame@gmail.com', body=message).execute()