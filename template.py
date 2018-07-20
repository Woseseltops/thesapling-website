def fill_template(template,vars):

	#Do it multiple times, as one iteration might create opportunities for the next one
	for i in range(0,2):
		for key, replacement in vars.items():
			template = template.replace('{{'+key+'}}',replacement)

	return template
