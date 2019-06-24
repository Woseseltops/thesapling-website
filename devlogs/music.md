Under the hood of the procedural music in The Sapling
=====================================================

| Technical | Music |

This article is an in-depth interactive explanation of how the procedural music in The Sapling works. Furthermore, we see how I had to give up my preference for clear hummable melodies, but got my way in the end.

<div>Music player</div>

This is a short excerpt of what the music in The Sapling sounds like. I hesitated a long time before I settled on this musical style. Normally, I prefer memorable, hummable melodies over soundscapes, but for The Sapling I couldn't figure how this would work. This was mainly for two reasons: firstly, every melody I came up with didn't really seem to match with the rest of game's style. Many other simulation games feature either jazzy or bright and jumpy orchestral soundtracks, but both styles somehow seemed to clash with a more serious game about nature. Secondly, I was afraid that I simply would not be able to come up with enough material, meaning that the same melodies would be repeating over and over.

---

I was afraid that I simply would not be able to come up with enough material, meaning that the same melodies would be repeating over and over

---

The solution came from an unexpected direction: during experimentation with ambient background music to get into a more productive mood (which by the way didn't work for me), I noticed that they often used a slideshow of pretty nature photos as 'background visuals'. Would it also work the other way around? If nature makes a good background visual for ambient music, is ambient music good background music for nature visuals? Accepting this, and thus giving up hummable melodies in favor of long slow notes to evoke a relaxed feeling in the listener, was a slow process, but ultimately lead to a second discovery: a lot of ambient music rarely changes chords. Instead, all notes throughout the whole ambient piece are from the same musical scale. This is convenient, because a general (and oversimplified) rule of thumb is that two pieces of music that use notes from the same scale will always sound good together. Creating an ambient sounding procedural soundtrack could simply be a matter of creating a large pool of musical fragments that only use notes from the same scale, and mixing them at random. How well this works is exemplified by the project (http://inbflat.net)['In B Flat'] (which, as the name suggests, uses B Flat as this one scale).

---

Creating an ambient sounding procedural soundtrack could simply be a matter of creating a large pool of musical fragments that only use notes from the same scale

---

This idea solved my two problems in one go: (1) the genre of ambient music fit the game's feel and (2) I could endlessly combine small musical fragments, giving you a fresh sounding soundtrack every time. The result is available for you to play with below. Feel free to click some play buttons at random, and decide for yourself if you think they sound good together.

<div class="player_group">
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/BG1.mp3'><div class="player_label">Background</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/BG2.mp3'><div class="player_label">Background</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/BG3.mp3'><div class="player_label">Background</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/BS1.mp3'><div class="player_label">Bass</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/BS2.mp3'><div class="player_label">Bass</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/BS3.mp3'><div class="player_label">Bass</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/CL1.mp3'><div class="player_label">Color</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/CL2.mp3'><div class="player_label">Color</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/FG1.mp3'><div class="player_label">Foreground</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/FG2.mp3'><div class="player_label">Foreground</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/FG3.mp3'><div class="player_label">Foreground</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
<div class="player_container">
	<img class="layerplayer" src="music/quiet.svg" playing='false' audio='music/FG4.mp3'><div class="player_label">Foreground</div>
	<img class="layerplayer_extra_layer" src="music/extra_layer_quiet.svg" playing="false">
</div>
</div>

My own conclusion, after playing with this for some time, was that although everything indeed sounded good together, some combinations were better for videogame background music than others. In the end, I identified five categories of fragments:

* The background, with long, sleepy tones. These are what gives the music its ambient feel. Strings are the most typical example.

* The foreground, played by a single instrument with short notes, grabbing the listener's attention. I most often use the piano or the celesta for this.

* The color, which is somewhere in between: they are played by a single instrument, but use long notes. These give a bit of flavour to a background that would otherwise always sound similar. This can for example be a clarinet or a trombone.

* The bass, often played by double bases or base clarinets.

* Victory sounds, that temporarily grab the player's attention and give them a satisfactory feeling. 

Furthermore, I discovered that using strings in *unisono with octave intervals* (playing the low and high versions of the same note at the same time) worked quite well to give the mix a more epic feel - I trick I knew from trying to write epic sounding film music. In the end, I used this together with the bass as the player is looking at his/her creations from a distance: as the player zooms out, the bass and *unisono* fade in. 

The button below categorizes the musical fragments above, and for the fragments in the background category adds an option to 'switch on' the epic version. If you make sure that for every category only one fragment is playing, you get something that could also be played in game.

<button id="labels_and_epic_button">Add labels and epic buttons</button>

One final question you might have is whether these musical fragments are completely random sequences of notes chosen by chance from a static scale. The answer is 'of course not': to satisfy my own desire for hummable melodies I actually did write a main theme for the game, and to give the game some musical coherence I echo parts of this theme in various fragments. This button below plays the main theme as you hear it in the main menu. Can you identify which of the musical fragments contain hints of this theme?

<div>Music player</div>

And that's all there is to it! By the way, if you want to do more with these pieces of music, you can! Both [the individual fragments] and [the layers of the main theme] are availale to be used in your own projects, as is the [sheet music] for the main theme. See [this devlog] for more info on that.

<script>

	class LayerPlayer
	{
		constructor(new_layers, playing_by_default)
		{
			this.playing = false;
			this.layers = []

			for (var layer_index in new_layers)
			{
				this.layers.push(new Audio(new_layers[layer_index]));
			}

			this.layers_playing = playing_by_default;
		}

		TogglePlaying()
		{
			if (this.playing)
			{
				for (var layer_index in this.layers)
				{
					this.layers[layer_index].pause();
				}

				this.playing = false;
			}
			else
			{
				for (var layer_index in this.layers)
				{
					this.layers[layer_index].play();

					if (!this.layers_playing[layer_index])
					{
						this.layers[layer_index].volume = 0;
					}
				}

				this.playing = true;
			}

			return this.playing;
		}

		ToggleLayer(index)
		{
			if (this.layers_playing[index])
			{
				this.layers[index].volume = 0;
				this.layers_playing[index] = false;
			}
			else
			{
				this.layers[index].volume = 1;
				this.layers_playing[index] = true;
			}
		}
	}

	var player_buttons = document.getElementsByClassName('layerplayer');
	var players = {};

	for (player_index in player_buttons)
	{
		if (player_buttons[player_index] == player_buttons.length) // why can this occur?
		{
			break
		}

		var audioFile = player_buttons[player_index].getAttribute('audio');
		players[audioFile] = new LayerPlayer([audioFile],[true]);

		player_buttons[player_index].addEventListener('click',function() 
		{
			var audioFile = this.getAttribute('audio');
			players[audioFile].TogglePlaying();

			if (this.getAttribute('playing') == 'true')
			{
				this.src = 'music/hovered.svg';
				this.setAttribute('playing','false');
			}
			else
			{
				this.src = 'music/playing.svg';
				this.setAttribute('playing','true');
			}
		});

		player_buttons[player_index].addEventListener('mouseover',function()
		{
			if (this.getAttribute('playing') == 'false')
			{
				this.src = 'music/hovered.svg'
			}
		});

		player_buttons[player_index].addEventListener('mouseout',function()
		{
			if (this.getAttribute('playing') == 'false')
			{
				this.src = 'music/quiet.svg'
			}
		});
	}

	var player_buttons = document.getElementsByClassName('layerplayer_extra_layer');

	for (player_index in player_buttons)
	{
		if (player_buttons[player_index] == player_buttons.length) // why can this occur?
		{
			break
		}

		player_buttons[player_index].addEventListener('click',function() 
		{
			if (this.getAttribute('playing') == 'true')
			{
				this.src = 'music/extra_layer_hovered.svg';
				this.setAttribute('playing','false');
			}
			else
			{
				this.src = 'music/extra_layer_playing.svg';
				this.setAttribute('playing','true');
			}
		});

		player_buttons[player_index].addEventListener('mouseover',function()
		{
			if (this.getAttribute('playing') == 'false')
			{
				this.src = 'music/extra_layer_hovered.svg'
			}
		});

		player_buttons[player_index].addEventListener('mouseout',function()
		{
			if (this.getAttribute('playing') == 'false')
			{
				this.src = 'music/extra_layer_quiet.svg'
			}
		});
	}

	var player_labels = document.getElementsByClassName('player_label');
	var layerplayer_extra_layers = document.getElementsByClassName('layerplayer_extra_layer');
	console.log(layerplayer_extra_layers);

	for (player_label_index in player_labels)
	{
		if (player_label_index == 'length')
		{
			break;
		}

		player_labels[player_label_index].style.display = 'none';
		layerplayer_extra_layers[player_label_index].style.display = 'none';
	}

	document.getElementById('labels_and_epic_button').addEventListener('click',function() 
	{
		var player_labels = document.getElementsByClassName('player_label');
		var layerplayer_extra_layers = document.getElementsByClassName('layerplayer_extra_layer');

		for (player_label_index in player_labels)
		{
			if (player_label_index == 'length')
			{
				break;
			}

			player_labels[player_label_index].style.display = 'block';
			layerplayer_extra_layers[player_label_index].style.display = 'block';
		}
	}
	);	

</script>

29-04-20