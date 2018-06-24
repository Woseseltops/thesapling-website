from os import listdir
from json import load

from twython import Twython

from devlog import parse_devlog

class PlatformManager():

	devlogs = []
	devlogs_published = []

	letter_identifier = None

class TwitterManager():

	letter_identifier = 'T'

	def __init__(self):

		PASSWORD_FILE_LOCATION = 'twitter_passwords.json'		
		passwords = load(open(PASSWORD_FILE_LOCATION))
		self.connection = Twython(passwords['app_key'], passwords['app_secret'], passwords['oauth_token'], passwords['oauth_token_secret'])

	def update_statuses(self): #Confusing name given the term 'status' in Twitter jargon
		pass

	def publish(self,devlog):
		self.connection.update_status(status=devlog.title)

if __name__ == '__main__':
	DEVLOG_FOLDER = 'devlogs/'
	PLATFORM_MANAGERS = [TwitterManager()]

	devlogs = []

	for devlog_file in listdir(DEVLOG_FOLDER):

		devlog = parse_devlog(devlog_file.split('.')[0],open(DEVLOG_FOLDER+devlog_file).read(),[])
		devlogs.append(devlog)

	for platform_manager in PLATFORM_MANAGERS:
		platform_manager.devlogs = devlogs

	platform_manager.publish(devlogs[0])