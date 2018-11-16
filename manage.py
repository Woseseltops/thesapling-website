from os import listdir, system
from json import load, dump
import webbrowser

from twython import Twython
from praw import Reddit
from mailchimp3 import MailChimp

#All necessary for gmail
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from devlog import parse_devlog
from template import fill_template

#======= General functionality ============

class PlatformManager():

	base_url = ''

	devlogs = []
	devlogs_published = []

	letter_identifier = None

def show_status(devlogs):

	print()

	for devlog in devlogs:
		header = devlog.title + ' ('+devlog.identifier+')'

		print(header)
		print('='*len(header))

		platforms_published = []
		platforms_not_published = []

		for platform in PLATFORM_MANAGERS:
			if platform.devlogs_published[devlog.identifier]:
				platforms_published.append(platform.letter_identifier)
			else:
				platforms_not_published.append(platform.letter_identifier)

		print('Published:',' '.join(platforms_published))
		print('Not published:',' '.join(platforms_not_published))
		print()

def add_to_clipboard(text,remove_linebreaks):

    if remove_linebreaks:
        command = 'echo | set /p nul="' + text.replace('\n','').strip() + '"| clip'
    else:
        command = 'echo | set /p nul="' + text.strip() + '"| clip'

    system(command)

#======= Individual managers ==========

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
	TEMPLATE_ID = 36269

	def __init__(self,base_url):

		PASSWORD_FILE_LOCATION = 'credentials/mailchimp.json'		
		passwords = load(open(PASSWORD_FILE_LOCATION))

		self.connection = MailChimp(mc_api=passwords['api_key'], mc_user=passwords['username'])
		self.base_url = base_url

	def publish(self,devlog):
		response = self.connection.campaigns.create(data={'type':'regular', 'recipients':{'list_id':'cee6f2fdcf'},
		 										'settings':{'subject_line': self.EMAIL_TITLE_PREFIX+devlog.title, 
		 										'from_name': 'Wessel Stoop', 
		 										'reply_to': 'thesaplinggame@gmail.com',
		 										'to_name': '*|FNAME|**|LNAME|*'}})

		#Deprecated
		#page = fill_template(open(self.EMAIL_TEMPLATE_LOCATION).read(),{'style': open(self.STYLESHEET_LOCATION).read(),'content':devlog.html,'title':devlog.title.upper()})

		self.connection.campaigns.content.update(campaign_id=response['id'],data={'template':{'id':self.TEMPLATE_ID,'sections':{'header':devlog.title.upper(),'content':devlog.html,
																																'link':'<a href="'+self.base_url+devlog.identifier+'" target="_blank">View this email in your browser</a>'}}})
		print('Campaign created, but you still need to log in and send!')

class HackerNewsManager(PlatformManager):

	letter_identifier = 'H'	

	def __init__(self,base_url):
		self.base_url = base_url

	def publish(self,devlog):
		webbrowser.open('https://news.ycombinator.com/submitlink?u='+self.base_url+devlog.identifier+'&t='+devlog.title)

class IndieDBManager(PlatformManager):

	letter_identifier = 'I'

	def __init__(self,base_url):
		self.base_url = base_url

	def publish(self,devlog):
		webbrowser.open('https://www.indiedb.com/games/olvand/articles/add/#articlesform')
		add_to_clipboard(devlog.title,False)
		input('Title on clipboard. Enter for next item.')
		add_to_clipboard(devlog.lead,False)
		input('Lead on clipboard. Enter for next item.')
		add_to_clipboard(devlog.bare_html,True)
		print('HTML on clipboard.')

class GamaSutraManager(PlatformManager):

	letter_identifier = 'S'

	def __init__(self,base_url):
		self.base_url = base_url

	def publish(self,devlog):
		webbrowser.open('http://gamasutra.com/blogs/edit/blog/item/')
		add_to_clipboard(devlog.title,False)
		input('Title on clipboard. Enter for next item.')
		add_to_clipboard(devlog.lead,False)
		input('Lead on clipboard. Enter for next item.')
		add_to_clipboard(devlog.bare_html,True)
		print('HTML on clipboard.')

class ItchManager(PlatformManager):

	letter_identifier = 'C'

	def __init__(self,base_url):
		self.base_url = base_url

	def publish(self,devlog):
		webbrowser.open('https://itch.io/dashboard/game/328633/new-devlog')
		add_to_clipboard(devlog.title,False)
		input('Title on clipboard. Enter for next item.')
		add_to_clipboard(devlog.bare_html,True)
		print('HTML on clipboard.')


# ==================================

if __name__ == '__main__':

	#Settings
	DEVLOG_FOLDER = 'devlogs/'
	DEVLOG_TAGS = ['Announcement','Behind the scenes','Technical details']

	BASE_URL = 'http://thesaplinggame.com/devlogs/'
	PLATFORM_MANAGERS = [TwitterManager, RedditManager, GmailManager, MailChimpManager, HackerNewsManager, 
							IndieDBManager, GamaSutraManager, ItchManager]
	SAVE_FILE_LOCATION = 'manage.save'

	#Get the devlogs
	devlogs = []

	for devlog_file in listdir(DEVLOG_FOLDER):

		devlog = parse_devlog(devlog_file.split('.')[0],open(DEVLOG_FOLDER+devlog_file).read(),DEVLOG_TAGS)
		devlogs.append(devlog)

	devlogs.sort(key=lambda devlog: devlog.date,reverse=True)

	#Load the save file
	try:
		saved_state = load(open(SAVE_FILE_LOCATION,'r'))
	except FileNotFoundError:
		saved_state = {}

	#Initialize the platforms
	platforms = [platform(BASE_URL) for platform in PLATFORM_MANAGERS]
	platforms_by_letter = {platform.letter_identifier: platform for platform in platforms}

	for platform_manager in PLATFORM_MANAGERS:
		platform_manager.devlogs = devlogs

		try:
			platform_manager.devlogs_published = saved_state[platform_manager.letter_identifier]
		except KeyError:
			platform_manager.devlogs_published = {devlog.identifier: False for devlog in devlogs}

	print('commands: status, publish <devlog ID> <platform IDs>')

	while True:
		command = input('> ')
		keyword = command.split()[0]

		if command == 'status':
			show_status(devlogs)

		elif keyword == 'publish':
			devlog_identifier = command.split()[1]

			for devlog in devlogs:
				if devlog.identifier == devlog_identifier:
					break

			platforms = [platforms_by_letter[platform_letter] for platform_letter in command.split()[2]]

			for platform in platforms:
				platform.publish(devlog)
				platform.devlogs_published[devlog.identifier] = True
				saved_state[platform.letter_identifier] = platform.devlogs_published
				dump(saved_state,open(SAVE_FILE_LOCATION,'w'))