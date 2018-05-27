from os import listdir, mkdir
from os.path import isdir
from shutil import copytree, rmtree

import datetime
import markdown

def parse_devlog(identifier,raw_markdown,tags):

	#First, take out the info we need
	devlog = DevLog(identifier)

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
		if '<h1>' in line:
			html[n] = ''

		elif '<p>|' in line:
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
				devlog.lead = html[n].replace('<p>','').replace('</p>','')
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

	html.append('<p id="date">Published '+devlog.get_pretty_date()+'</p>')

	devlog.html = '\n'.join(html);
	return devlog

class DevLog():

	def __init__(self,identifier):

		self.identifier = identifier

		self.title = ''
		self.html = ''
		self.tags = []
		self.date = None
		self.lead = ''

	def get_pretty_date(self):
		return self.date.strftime("%A %d %B %Y")		

def fill_template(template,vars):

	for key, replacement in vars.items():
		template = template.replace('{{'+key+'}}',replacement)

	return template

def create_page(template_location,title_area_file_location,title,content,page_type,content_variables = None):

	title_area = open(title_area_file_location).read()

	if content_variables != None:
		content = fill_template(content,content_variables)

	return fill_template(open(template_location).read(),{'title_area':title_area,'title':title,'content':content,'page_type':page_type})

def devlog_to_list_item(devlog,devlog_list_item_template_location,even):

	NR_OF_CHARS_IN_LEAD = 150;

	if even:
		evenorodd = 'even'
	else:
		evenorodd = 'odd'

	return fill_template(open(devlog_list_item_template_location).read(),{'identifier':devlog.identifier,'title':devlog.title,'date':devlog.get_pretty_date(),
																'lead':devlog.lead[:NR_OF_CHARS_IN_LEAD],'tag':devlog.tags[0],'evenorodd':evenorodd})

def generate_static_website():

	PAGES_TO_GENERATE_FOLDER = 'pages_to_generate/'
	DEVLOGS_FOLDER = 'devlogs/'

	MAIN_TEMPLATE_LOCATION = 'main_template.html'
	MAIN_TITLE_AREA_FILE_LOCATION = 'main_title_area.html'
	DEVLOG_TITLE_AREA_FILE_LOCATION = 'devlog_title_area.html'
	DEVLOG_LIST_ITEM_TEMPLATE_LOCATION = 'devlog_list_item_template.html'

	GOAL_LOCATION = 'latest_website/'
	STATIC_FOLDER = 'static/'

	DEVLOG_TAGS = ['Announcement','Behind the scenes','Technical details']

	#Empty last
	if isdir(GOAL_LOCATION):
		rmtree(GOAL_LOCATION)

	mkdir(GOAL_LOCATION)
	mkdir(GOAL_LOCATION+'devlogs/')

	#Generate devlogs
	devlogs = []

	for filename in listdir(DEVLOGS_FOLDER):
		devlog = parse_devlog(filename.split('.')[0],open(DEVLOGS_FOLDER+filename).read(),DEVLOG_TAGS)
		full_content = create_page(MAIN_TEMPLATE_LOCATION,DEVLOG_TITLE_AREA_FILE_LOCATION,devlog.title.upper(),devlog.html,'devlog')
		filename = filename.replace('.md','.html')
		open(GOAL_LOCATION+'devlogs/'+filename,'w').write(full_content)
		devlogs.append(devlog)

	devlogs.sort(key=lambda devlog: devlog.date,reverse=True)

	#Generate the devlog listview
	listview_content = '<h3 class="page_header">DEVLOGS</h3>'

	for n,devlog in enumerate(devlogs):
		listview_content += devlog_to_list_item(devlog,DEVLOG_LIST_ITEM_TEMPLATE_LOCATION,n%2==0)
	
	listview_content = create_page(MAIN_TEMPLATE_LOCATION,MAIN_TITLE_AREA_FILE_LOCATION,'The Sapling',listview_content,'devlog_list')
	open(GOAL_LOCATION+'devlogs/index.html','w').write(listview_content)

	#Generate basic pages
	for filename in listdir(PAGES_TO_GENERATE_FOLDER):
		full_content = create_page(MAIN_TEMPLATE_LOCATION,MAIN_TITLE_AREA_FILE_LOCATION,'The Sapling',open(PAGES_TO_GENERATE_FOLDER+filename).read(),'main',
									content_variables={'latest_devlog':devlog_to_list_item(devlogs[0],DEVLOG_LIST_ITEM_TEMPLATE_LOCATION,False)})
		open(GOAL_LOCATION+filename,'w').write(full_content)

	#Move over the static files
	copytree(STATIC_FOLDER,GOAL_LOCATION+STATIC_FOLDER)

if __name__ == '__main__':
	generate_static_website()