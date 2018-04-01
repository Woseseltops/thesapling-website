from os import listdir, mkdir
from os.path import isdir
from shutil import copytree, rmtree

import markdown

def generate_static_website():

	PAGES_TO_GENERATE_FOLDER = 'pages_to_generate/'
	DEVLOGS_FOLDER = 'devlogs/'

	MAIN_TEMPLATE_LOCATION = 'main_template.html'
	GOAL_LOCATION = 'latest_website/'
	STATIC_FOLDER = 'static/'

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
		html = markdown.markdown(open(DEVLOGS_FOLDER+filename).read())
		full_content = open(MAIN_TEMPLATE_LOCATION).read().replace('{{content}}',html)
		filename = filename.replace('.md','.html')
		open(GOAL_LOCATION+'devlogs/'+filename,'w').write(full_content)

	copytree(STATIC_FOLDER,GOAL_LOCATION+STATIC_FOLDER)

if __name__ == '__main__':
	generate_static_website()