class YouTuber:

    def __init__(self,name):

        self.name = name
        self.email = None
        self.real_name = None
        self.views_per_game = {}

    @property
    def games(self):
        return list(self.views_per_game.keys())

    @property
    def highest(self):
        if len(self.views_per_game.values()) > 0:
            return max(self.views_per_game.values())
        else:
            return 0

    @property
    def best_name(self):
    
        if self.real_name != None:
            return self.real_name
        else:
            return 'creator of the YouTube channel ' + self.name

    def __str__(self):
        return f'{self.name} ({self.highest})'

def game_list_to_description(game_list):

    if len(game_list) == 1:
        return f'game {game_list[0]}'
    else:
        comma_separated_games = ', '.join(game_list[:-1])
        return f'games {comma_separated_games} and {game_list[-1]}'

def batch_youtubers():
	FILENAME = 'Marketing planning.txt'
	youtubers = []

	for n, line in enumerate(open(FILENAME)):

		if n == 0:
			continue

		name, species, riples, instincts, equilinox, empires, universim, nectar, beetle, design, spore, eco, birthdays, evolution, flowscape, creatura, highest, email, real_name, note, nr_of_games = line.split('\t')
		y = YouTuber(name)

		for game, view_count in [('Species: ALRE',species), ('Among ripples',riples), ('Natural Instincts',instincts),
								 ('Equilinox',equilinox), ('Empires of the Undergrowth',empires), ('The Universim',universim),
								 ('Drunk on nectar',nectar), ('Beetle Uprising',beetle), ('Intelligent Design',design), ('Spore',spore),
								 ('Eco',eco), ('Birthdays the Beginning',birthdays), ('Evolution: the videogame',evolution), ('Flowscape',flowscape),('Creatura',creatura)]:

			if len(view_count) > 0 and float(view_count) > 0:
				y.views_per_game[game] = float(view_count)

		if '@' in email:
			y.email = email

		if len(real_name) > 0:
			y.real_name = real_name

		youtubers.append(y)

	batch_a = []
	batch_b = []
	batch_c = []
	batch_d = []
	batch_e = []

	no_email = []

	for y in youtubers:
	
		if y.email == None:
			no_email.append(y)
			continue

		if len(y.views_per_game) > 2:
			batch_a.append(y)
		elif len(y.views_per_game) > 1:
			batch_b.append(y)
		elif y.games[0] != 'The Universim' or y.highest > 50:
			batch_c.append(y)
		elif y.games[0] != 'The Universim':
			batch_d.append(y)
		else:
			batch_e.append(y)

	batch_a = sorted(batch_a,key=lambda youtuber: (len(youtuber.games),youtuber.highest),reverse=True)
	batch_b = sorted(batch_b,key=lambda youtuber: (len(youtuber.games),youtuber.highest),reverse=True)
	batch_c = sorted(batch_c,key=lambda youtuber: (len(youtuber.games),youtuber.highest),reverse=True)
	batch_d = sorted(batch_d,key=lambda youtuber: (len(youtuber.games),youtuber.highest),reverse=True)
	batch_e = sorted(batch_e,key=lambda youtuber: (len(youtuber.games),youtuber.highest),reverse=True)

	no_email = sorted(no_email,key=lambda youtuber: (len(youtuber.games),youtuber.highest),reverse=True)
	
	return batch_a,batch_b,batch_c,batch_d,batch_e,no_email

if __name__ == '__main__':
	batch = batch_youtubers()[2]
	print(batch)
	selection = []

	for tuber in batch:
		average = sum(tuber.views_per_game.values()) / len(tuber.views_per_game)

		if (average < 100 and average > 1):
			print(tuber)
			selection.append(tuber)

	print(len(selection))