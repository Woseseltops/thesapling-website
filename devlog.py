import datetime
import markdown

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