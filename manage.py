from os import listdir
from json import load

from twython import Twython

from devlog import parse_devlog

class PlatformManager():

	devlogs = []
	devlogs_published = []

	letter_identifier = None

class TwitterManager(PlatformManager):

	letter_identifier = 'T'

	def __init__(self):

		PASSWORD_FILE_LOCATION = 'twitter_passwords.json'		
		passwords = load(open(PASSWORD_FILE_LOCATION))
		self.connection = Twython(passwords['app_key'], passwords['app_secret'], passwords['oauth_token'], passwords['oauth_token_secret'])

	def update_statuses(self): #Confusing name given the term 'status' in Twitter jargon
		pass

	def publish(self,devlog):
		self.connection.update_status(status=devlog.title)

def show_status(devlogs):

	for devlog in devlogs:
		print(devlog.title)
		print('===========')

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
	PLATFORM_MANAGERS = [TwitterManager()]

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
			print(devlog,platforms)

	#platform_manager.publish(devlogs[0])