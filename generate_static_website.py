from os import listdir
from shutil import copyfile

def generate_static_website():

	PAGES_TO_GENERATE_FOLDER = 'pages_to_generate/'
	MAIN_TEMPLATE_LOCATION = 'main_template.html'
	GOAL_LOCATION = 'latest_website/'
	STYLESHEET_NAME = 'style.css'

	for filename in listdir(PAGES_TO_GENERATE_FOLDER):
		full_content = open(MAIN_TEMPLATE_LOCATION).read().replace('{{content}}',open(PAGES_TO_GENERATE_FOLDER+filename).read())
		open(GOAL_LOCATION+filename,'w').write(full_content)

	copyfile(STYLESHEET_NAME,GOAL_LOCATION+STYLESHEET_NAME)

if __name__ == '__main__':
	generate_static_website()