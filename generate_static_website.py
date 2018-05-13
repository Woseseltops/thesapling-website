from os import listdir, mkdir
from os.path import isdir
from shutil import copytree, rmtree

import datetime
import markdown

def parse_devlog(raw_markdown,tags):

	#First, take out the info we need
	devlog = DevLog()

	markdown_lines = raw_markdown.split('\n')

	for n,line in enumerate(markdown_lines):

		if n == 0:
			devlog.title = line.strip()
		elif len(line) > 0:
			if line[0] == '|':
				devlog.tags = [tag.strip() for tag in line.split('|')[1:-1]]
			elif len(line) > 5 and line[2] == '-' and line[5] == '-':
				devlog.date = datetime.datetime.strptime( line.strip(), "%d-%m-%y" )

	#Then generate the html
	html = markdown.markdown('\n'.join(markdown_lines[:-1])).split('\n')

	#And replace some html lines by what we now from the parsing of the markdown
	for n,line in enumerate(html):
		if '<p>|' in line:
			html[n] = '<div>' 

			for tag in tags:

				if tag in devlog.tags:
					class_info = 'selected_tag'
				else:
					class_info = 'nonselected_tag'

				html[n] += '<div class="'+class_info+'">'+tag+'</div>'

			html[n] += '</div>'

	html.append('<p id="date">Published '+devlog.date.strftime("%A %d %B %Y")+'</p>')

	devlog.html = '\n'.join(html);
	return devlog

class DevLog():

	def __init__(self):

		self.title = ''
		self.html = ''
		self.timestamp = 0
		self.tags = []
		self.date = None

def generate_static_website():

	PAGES_TO_GENERATE_FOLDER = 'pages_to_generate/'
	DEVLOGS_FOLDER = 'devlogs/'

	MAIN_TEMPLATE_LOCATION = 'main_template.html'
	GOAL_LOCATION = 'latest_website/'
	STATIC_FOLDER = 'static/'

	DEVLOG_TAGS = ['Announcement','Behind the scenes','Technical details']

	#Empty last
	if isdir(GOAL_LOCATION):
		rmtree(GOAL_LOCATION)

	mkdir(GOAL_LOCATION)
	mkdir(GOAL_LOCATION+'devlogs/')

	#Generate basic pages
	for filename in listdir(PAGES_TO_GENERATE_FOLDER):
		full_content = open(MAIN_TEMPLATE_LOCATION).read().replace('{{content}}',open(PAGES_TO_GENERATE_FOLDER+filename).read())
		open(GOAL_LOCATION+filename,'w').write(full_content)

	#Generate devlogs
	for filename in listdir(DEVLOGS_FOLDER):
		html = parse_devlog(open(DEVLOGS_FOLDER+filename).read(),DEVLOG_TAGS).html
		full_content = open(MAIN_TEMPLATE_LOCATION).read().replace('{{content}}',html)
		filename = filename.replace('.md','.html')
		open(GOAL_LOCATION+'devlogs/'+filename,'w').write(full_content)

	copytree(STATIC_FOLDER,GOAL_LOCATION+STATIC_FOLDER)

if __name__ == '__main__':
	generate_static_website()