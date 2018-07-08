from os import listdir
from json import load

from twython import Twython
from praw import Reddit
from mailchimp3 import MailChimp

#All necessary for gmail
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from devlog import parse_devlog

class PlatformManager():

	base_url = ''

	devlogs = []
	devlogs_published = []

	letter_identifier = None

class TwitterManager(PlatformManager):

	letter_identifier = 'T'
	hash_tag = '#justtesting'

	def __init__(self,base_url):

		self.base_url = base_url

		PASSWORD_FILE_LOCATION = 'credentials/twitter.json'		
		passwords = load(open(PASSWORD_FILE_LOCATION))
		self.connection = Twython(passwords['app_key'], passwords['app_secret'], passwords['oauth_token'], passwords['oauth_token_secret'])

	def update_statuses(self): #Confusing name given the term 'status' in Twitter jargon
		pass

	def publish(self,devlog):
		self.connection.update_status(status=devlog.title+' '+self.base_url+devlog.identifier+' '+self.hash_tag)

class RedditManager(PlatformManager):

	letter_identifier = 'R'

	def __init__(self,base_url):

		self.base_url = base_url

		PASSWORD_FILE_LOCATION = 'credentials/reddit.json'		
		passwords = load(open(PASSWORD_FILE_LOCATION))
		self.connection = Reddit(client_id=passwords['client_id'],
		                     client_secret=passwords['client_secret'],
		                     user_agent=passwords['user_agent'],
		                     username=passwords['username'],
		                     password=passwords['password'])		

	def publish(self,devlog):
		subreddit = self.connection.subreddit('r/testingground4bots')
		print(subreddit)

		subreddit.submit('Devlog: '+devlog.title, url=self.base_url+devlog.identifier)
		
class GmailManager(PlatformManager):

	letter_identifier = 'G'	
	SIGNATURE_TEXT_PREFIX = 'Check out the latest devlog '

	def __init__(self,base_url):

		self.base_url = base_url

		SCOPES = 'https://www.googleapis.com/auth/gmail.settings.basic'
		store = file.Storage('credentials/gmail.json')
		creds = store.get()

		if not creds or creds.invalid:
		    flow = client.flow_from_clientsecrets('credentials/gmail_client_secret.json', SCOPES)
		    creds = tools.run_flow(flow, store)

		self.connection = build('gmail', 'v1', http=creds.authorize(Http()))

	def publish(self,devlog):

		primary_alias = None
		aliases = self.connection.users().settings().sendAs().list(userId='me').execute()

		for alias in aliases.get('sendAs'):
		    if alias.get('isPrimary'):
		        primary_alias = alias
		        break

		sendAsConfiguration = {'signature': self.SIGNATURE_TEXT_PREFIX+' \''+devlog.title+'\': '+self.base_url+devlog.identifier}
		result = self.connection.users().settings().sendAs().patch(userId='me',sendAsEmail=primary_alias.get('sendAsEmail'),body=sendAsConfiguration).execute()		

class MailChimpManager(PlatformManager):

	letter_identifier = 'M'	
	EMAIL_TITLE_PREFIX = 'New devlog: '

	def __init__(self,base_url):

		PASSWORD_FILE_LOCATION = 'credentials/mailchimp.json'		
		passwords = load(open(PASSWORD_FILE_LOCATION))

		self.connection = MailChimp(mc_api=passwords['api_key'], mc_user=passwords['username'])

	def publish(self,devlog):
		response = self.connection.campaigns.create(data={'type':'regular', 'recipients':{'list_id':'cee6f2fdcf'},
		 										'settings':{'subject_line': self.EMAIL_TITLE_PREFIX+devlog.title, 'from_name': 'Wessel Stoop', 'reply_to': 'thesaplinggame@gmail.com'}})

		print(response['id'])
		#self.connection.campaigns.content.update(campaign_id='5a056544ca',data={'url':'<h1>This is a test.</h1>'})

		#print('Campaign created, but you still need to log in and send!')

def show_status(devlogs):

	for n, devlog in enumerate(devlogs):
		header = str(n) + '. '+ devlog.title

		print(header)
		print('='*len(header))

		platforms_published = []
		platforms_not_published = []

		for platform in PLATFORM_MANAGERS:
			if devlog in platform.devlogs_published:
				platforms_published.append(platform.letter_identifier)
			else:
				platforms_not_published.append(platform.letter_identifier)

		print('Published:',' '.join(platforms_published))
		print('Not published:',' '.join(platforms_not_published))
		print()


if __name__ == '__main__':
	DEVLOG_FOLDER = 'devlogs/'
	BASE_URL = 'http://thesaplinggame.com/devlogs/'
	PLATFORM_MANAGERS = [TwitterManager(BASE_URL), RedditManager(BASE_URL), GmailManager(BASE_URL), MailChimpManager(BASE_URL)]

	platforms_by_letter = {platform.letter_identifier: platform for platform in PLATFORM_MANAGERS}
	devlogs = []

	#Get the devlogs
	for devlog_file in listdir(DEVLOG_FOLDER):

		devlog = parse_devlog(devlog_file.split('.')[0],open(DEVLOG_FOLDER+devlog_file).read(),[])
		devlogs.append(devlog)

	devlogs.sort(key=lambda devlog: devlog.date,reverse=True)

	for platform_manager in PLATFORM_MANAGERS:
		platform_manager.devlogs = devlogs

	print('commands: status, publish <devlog #> <platform IDs>')

	while True:
		command = input('> ')
		keyword = command.split()[0]

		if command == 'status':
			show_status(devlogs)

		elif keyword == 'publish':
			devlog = devlogs[int(command.split()[1])]
			platforms = [platforms_by_letter[platform_letter] for platform_letter in command.split()[2]]

			for platform in platforms:
				platform.publish(devlog)