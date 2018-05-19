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
	alinea_index = 0
	pull_quote_mode = False

	for n,line in enumerate(html):
		if '<p>|' in line:
			html[n] = '<div id="label_bar">' 

			for tag in tags:

				if tag in devlog.tags:
					class_info = 'selected_tag'
				else:
					class_info = 'nonselected_tag'

				html[n] += '<div class="'+class_info+'">'+tag+'</div>'

			html[n] += '</div>'

		elif '<p>' in line:
			if alinea_index == 0:
				html[n] = html[n].replace('<p>','<p id="first_p">')
				alinea_index += 1
			elif alinea_index == 1:
				html[n] = '<p><span id="first_character">'+line[3]+'</span>'+line[4:]
				alinea_index += 1			
			elif pull_quote_mode:
				html[n] = html[n].replace('<p>','<p class="pull_quote">')

		elif '<hr />' in line:
			if pull_quote_mode:
				pull_quote_mode = False
			else:
				pull_quote_mode = True

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

def create_page(template_location,content,page_type):

	return open(template_location).read().replace('{{content}}',content).replace('{{page_type}}',page_type)

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
		full_content = create_page(MAIN_TEMPLATE_LOCATION,open(PAGES_TO_GENERATE_FOLDER+filename).read(),'main')
		open(GOAL_LOCATION+filename,'w').write(full_content)

	#Generate devlogs
	for filename in listdir(DEVLOGS_FOLDER):
		html = parse_devlog(open(DEVLOGS_FOLDER+filename).read(),DEVLOG_TAGS).html
		full_content = create_page(MAIN_TEMPLATE_LOCATION,html,'devlog')
		filename = filename.replace('.md','.html')
		open(GOAL_LOCATION+'devlogs/'+filename,'w').write(full_content)

	copytree(STATIC_FOLDER,GOAL_LOCATION+STATIC_FOLDER)

if __name__ == '__main__':
	generate_static_website()