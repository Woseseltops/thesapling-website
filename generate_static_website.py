from os import listdir, mkdir, system, chdir, getcwd, rename, remove
from os.path import isdir
from shutil import copyfile, copytree, rmtree
from email.utils import format_datetime
from subprocess import Popen

from devlog import parse_devlog
from template import fill_template

def create_page(template_location,title_area_file_location,title,content,page_type,content_variables = None,portrait_area = None):

	title_area = open(title_area_file_location).read()

	if content_variables != None:
		content = fill_template(content,content_variables)

	all_variables = {'title_area':title_area,'title':title,'content':content,'page_type':page_type,'portrait_area':''}

	if portrait_area != None:
		all_variables['portrait_area'] = open(portrait_area).read()

	return fill_template(open(template_location).read(),all_variables)

def devlog_to_list_item(devlog,devlog_list_item_template_location,even,simplified):

	if even:
		evenorodd = 'even'
	else:
		evenorodd = 'odd'

	if simplified:
		display = 'none'
		salient = 'salient_title'
		nr_of_chars = 350

	else:
		display = 'block'
		salient = ''
		nr_of_chars = 150

	return fill_template(open(devlog_list_item_template_location).read(),{'identifier':devlog.identifier,'title':devlog.title,'date':devlog.get_pretty_date(),
																'lead':devlog.lead[:nr_of_chars],'tag':devlog.tags[0],'evenorodd':evenorodd,'display':display,'salient_title':salient})

def get_svg_images(images,static_folder):

	result = {}

	for image in images:
		result[image] = open(static_folder+'svg/'+image+'.svg').read().replace('<svg','<svg class="icon"')

	return result		

def create_navigation_buttons(items,n,svg_images):

	result = ''

	try:
		result += '<div class="iconlabel"><a href="'+items[n+1].identifier+'.html">'+svg_images['arrow_left']+'<br>Older</a></div>'
	except IndexError:
		pass

	result += '<div class="iconlabel"><a href="/devlogs">'+svg_images['arrow_up']+'<br>Overview</a></div>'

	if n > 0:
		try:
			result += '<div class="iconlabel"><a href="'+items[n-1].identifier+'.html">'+svg_images['arrow_right']+'<br>Newer</a></div>'
		except IndexError:
			pass

	return result

def devlogs_to_rss(devlogs,template_location,item_template_location):

	rss_items = []

	for devlog in devlogs:
		rss_items.append(fill_template(open(item_template_location).read(),{'title':devlog.title,'lead':devlog.lead,'identifier':devlog.identifier,
																			'date':format_datetime(devlog.date)}))

	return fill_template(open(template_location,'r').read(),{'items':''.join(rss_items),'date':format_datetime(devlog.date)})

def generate_press_section(php_location,press_folder,goal_location):

	#mkdir(goal_location)
	copyfile(press_folder+'style.css',goal_location+'style.css')

	current_dir = getcwd() + '/'
	chdir(php_location) #Needed to be able to run php

	for page_name, arguments in [('index',''),('sheet','The Sapling')]:

		print(' '.join(['php.exe',current_dir+press_folder+page_name+'.php',arguments]))
		p = Popen(['php.exe',current_dir+press_folder+page_name+'.php',arguments],stdout=open(current_dir+goal_location+page_name+'.html','w'))	
		p.wait()

	chdir(current_dir)

def generate_static_website():

	#Settings
	PAGES_TO_GENERATE_FOLDER = 'pages_to_generate/'
	DEVLOGS_FOLDER = 'devlogs/'
	TEMPLATE_FOLDER = 'templates/'

	MAIN_TEMPLATE_LOCATION = TEMPLATE_FOLDER+'main_template.html'
	MAIN_TITLE_AREA_FILE_LOCATION = TEMPLATE_FOLDER+'main_title_area.html'
	DEVLOG_TITLE_AREA_FILE_LOCATION = TEMPLATE_FOLDER+'devlog_title_area.html'
	DEVLOG_LIST_TITLE_AREA_FILE_LOCATION = TEMPLATE_FOLDER+'devlog_list_title_area.html'
	DEVLOG_LIST_ITEM_TEMPLATE_LOCATION = TEMPLATE_FOLDER+'devlog_list_item_template.html'
	PORTRAIT_TEMPLATE_LOCATION = TEMPLATE_FOLDER+'portrait_template.html'

	RSS_TEMPLATE_LOCATION = TEMPLATE_FOLDER+'rss_template.xml'
	RSS_ITEM_TEMPLATE_LOCATION = TEMPLATE_FOLDER+'rss_item_template.xml'

	PHP_LOCATION = 'C:/Program Files/php-7.0.9-Win32-VC14-x64/' #'C:/Users/wstoop/Downloads/php/php.exe'
	CIVETWEB_LOCATION = 'C:/Users/Wessel/Downloads/CivetWeb_Win32+64_V1.9.1/' #'C:\\Users\\wstoop\\Downloads\\CivetWeb64.exe'

	GOAL_LOCATION = 'docs/'
	DOMAIN_NAME = 'thesaplinggame.com'
	STATIC_FOLDER = 'static/'
	PRESS_FOLDER = 'press/'
	PRECOMPILED_PRESS_FOLDER = 'press_precompiled/'

	FRONT_PAGE = 'landing1.html'
	DEVLOG_TAGS = ['Announcement','Technical','Graphics','Music']

	#Stop the webserver
	system("taskkill /im Civetweb64.exe")

	#Empty last
	if isdir(GOAL_LOCATION):
		rmtree(GOAL_LOCATION)

	#Create the goal folder
	mkdir(GOAL_LOCATION)
	mkdir(GOAL_LOCATION+'devlogs/')
	open(GOAL_LOCATION+'CNAME','w').write(DOMAIN_NAME)

	#Get images
	svg_images = get_svg_images(['rss_icon','devlog_icon','twitter_icon','steam_icon','itch_icon','kartridge_icon','gamejolt_icon','arrow_left','arrow_up','arrow_right'],STATIC_FOLDER)	

	#Generate devlogs
	devlogs = []

	for filename in listdir(DEVLOGS_FOLDER):

		if isdir(DEVLOGS_FOLDER+filename):
			copytree(DEVLOGS_FOLDER+filename,GOAL_LOCATION+DEVLOGS_FOLDER+filename)
		else:
			devlog = parse_devlog(filename.split('.')[0],open(DEVLOGS_FOLDER+filename).read(),DEVLOG_TAGS)
			devlogs.append(devlog)

	devlogs.sort(key=lambda devlog: devlog.date,reverse=True)

	for n,devlog in enumerate(devlogs):
		navigation_buttons = create_navigation_buttons([devlog for devlog in devlogs if devlog.published],n,svg_images)		
		full_content = create_page(MAIN_TEMPLATE_LOCATION,DEVLOG_TITLE_AREA_FILE_LOCATION,devlog.title.upper(),
									devlog.html+navigation_buttons,'devlog',portrait_area=PORTRAIT_TEMPLATE_LOCATION)
		open(GOAL_LOCATION+'devlogs/'+devlog.identifier+'.html','w').write(full_content)

	#Generate the devlog listview
	listview_content = '<h3 class="page_header">DEVLOGS</h3>'

	for n,devlog in enumerate(devlogs):

		if devlog.published:
			listview_content += devlog_to_list_item(devlog,DEVLOG_LIST_ITEM_TEMPLATE_LOCATION,n%2==0,False)
	
	listview_content = create_page(MAIN_TEMPLATE_LOCATION,DEVLOG_LIST_TITLE_AREA_FILE_LOCATION,'The Sapling',listview_content,'devlog_list')
	open(GOAL_LOCATION+'devlogs/index.html','w').write(listview_content)

	#Generate the devlog rss
	rss = devlogs_to_rss(devlogs,RSS_TEMPLATE_LOCATION,RSS_ITEM_TEMPLATE_LOCATION)
	open(GOAL_LOCATION+'devlogs.rss','w').write(rss)

	#Generate basic pages
	content_variables = svg_images
	content_variables['latest_devlog'] = devlog_to_list_item(devlogs[0],DEVLOG_LIST_ITEM_TEMPLATE_LOCATION,False,True)

	for filename in listdir(PAGES_TO_GENERATE_FOLDER):
		full_content = create_page(MAIN_TEMPLATE_LOCATION,MAIN_TITLE_AREA_FILE_LOCATION,'The Sapling',open(PAGES_TO_GENERATE_FOLDER+filename).read(),'main',
									content_variables=content_variables)
		open(GOAL_LOCATION+filename,'w').write(full_content)

	#Move over the static files
	copytree(STATIC_FOLDER,GOAL_LOCATION+STATIC_FOLDER)

	#Make static version of press pages
	#copytree(PRESS_FOLDER+'images',GOAL_LOCATION+PRESS_FOLDER+'images')
	#copytree(PRESS_FOLDER+'The Sapling/images',GOAL_LOCATION+PRESS_FOLDER+'The Sapling/images')
	#generate_press_section(PHP_LOCATION,PRESS_FOLDER,GOAL_LOCATION+PRESS_FOLDER)

	#Or copy in a precompiled press section
	copytree(PRECOMPILED_PRESS_FOLDER,GOAL_LOCATION+PRESS_FOLDER)

	#Landing page
	if FRONT_PAGE != 'index.html':
		remove(GOAL_LOCATION+'index.html')	
		rename(GOAL_LOCATION+FRONT_PAGE,GOAL_LOCATION+'index.html')

	#Start the webserver
	chdir(CIVETWEB_LOCATION)
	Popen('CivetWeb64.exe')

if __name__ == '__main__':
	generate_static_website()