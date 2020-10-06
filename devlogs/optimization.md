Optimization: what I did to make the game 300 times faster
===========================================================

| Technical | Graphics |

A major point of feedback for evolution simulator The Sapling is that the players wanted larger levels. To make this possible, I spent three months optimizing the underlying game engine. This article is an in-depth explanation of one of the main insights I had. There are several interactive simulations you can play with in your browser to get a deeper understanding of how everything works.

The first major update for The Sapling, the flower update, was released in September. It adds pollination, flowers (obviously), a new scenario, a complete overhaul of the sandbox level, bioluminescence and much more. A number of scenes from the trailer:

<video width="320" style="height:inherit; visibility: visible;" loop autoplay muted>
  <source src="optimization/flower_highlights.mp4" type="video/mp4">
</video>

Importantly, it addresses a major point of feedback that kept coming back: players wanted more space for their creations to grow and evolve. I couldn't easily make the levels larger, however, because the small levels already were a problem for the game's performance. The hard part is that there are not one, but two computationally heavy things going on at the same time: simulating an ecosystem where hundreds of organisms are all doing their own things (moving, eating, reproducing, mutating) AND visualizing these hundreds of objects. With larger levels, this would be thousands, essentially bringing the game to a halt with 1 frame per 5 seconds (FPS) instead of the regular 60 per 1 second. 

Besides my obvious desire to please the players, having larger levels was also crucial for my own ambitions with the game, because a number of the simulation mechanics didn't really work with the smaller maps; for example, why evolve an instinct to run away from a predator if you have nowhere to go? Or for plants, why evolve things like bark or high leaves if the biggest reason that your offspring is dying is because all seeds are landing on spots that are already taken? You better focus on getting as much offspring as possible, in the hopes that at least one of them by accident lands in a spot that is free.

In other words, if there was going to be one major feature in the first big update, it should be larger maps. To make this possible, I spent 3 months in the beginning of 2020 with that one focus: optimize, optimize, optimize the game's code, so I could get that FPS up and shave off more of the milliseconds it takes to render a scene. It was frustrating at times, but the main feeling I remember was actually excitement, as this really forced me to investigate the major bottlenecks (when I close my eyes, I can still see the Unity profiler), and come up with several new creative solutions for them. During this period I was reading a book about how John Carmack, the brilliant programmer behind the first Doom engine, was doing endless optimizations to make first person shooters a reality in the 90s, which was a great help in keeping me motivated.

While I implemented all kinds of larger and smaller ideas that made significant positive contributions to the performance of the game, there is one insight that had the biggest impact for the visualization part of the problem (how do you show thousands of unique organisms on screen?), which is to **fake it before you make it**. Let's go through my thought process step by step to see what I mean by that in this context. For every step, there is an interactive simulation you can run in your browser, so you can play with the idea yourself.

Step 1: the raw, unoptimized goal
----------------------------------

This is the basic idea, without any optimization: players can add their self created species somewhere in the world, and see whether it is strong enough to survive. In the interactive example below, you can add two species, 1 and 2, and then run the simulation. 

<style>
.sim
{
	height: 842px;
    width: 783px;
    padding: 35px;	
    font-family: 'Montserrat';
}

#basic
{
	background: url('optimization/simulation_background_basic.svg');	
}

#pool
{
	background: url('optimization/simulation_background_pool.svg');	
}

#library
{
	background: url('optimization/simulation_background_library.svg');	
}

#ancestors
{
	background: url('optimization/simulation_background_ancestors.svg');	
}

.devlog button
{
	background-color: transparent;
    border: none;
    padding: 0px;
    width: inherit;
    margin: 0px;    
    margin-right: 10px;
}	

button:focus
{
	outline: none;
}

button img
{
	height: 51px;
	margin-bottom: 17px;
	cursor: pointer;
}

button img:hover
{
	filter: brightness(0.9);
}

table
{
	height: 590px;
}

td
{
	color: white;
	text-align: center;
	width: 100px;
	height: 116px;
    font-size: 12px;
    font-weight: 200;
}

.stress_nr
{
	font-weight: 800;
}

.speciesIdentifier
{
	font-size: 50px;
	margin-top: -57px;
	font-weight: 500;
}

.library, .pool
{
	width: 62px;
    height: 582px;	
    color: white;
    text-align: center;
    font-size: 10px;
}

.pool
{
	margin-top: -552px;
    margin-left: 566px;
}

.pool img, .library img
{
	width: 40px;
}

.pool .speciesIdentifier, .library .speciesIdentifier
{
	font-size: 30px;
	margin-top: -36px;
}

.library
{
    margin-top: -582px;
    margin-left: 658px;    
}

.not_shown_plants
{
    font-weight: 800;
    margin-top: 7px;
    color: hsl(36deg 35% 28%);	
}

.showing_fake
{
    color: hsl(47deg 100% 50%);	
}		
</style>
<script src="optimization/simulation.js"></script>

<div class="sim" id="basic">
</div>

<script>
	var sim = new Simulation();
		
	elem = document.getElementById('basic');
	visualize_simulation(sim,elem,'basic','optimization/');	
</script>

The simulation and subsequent visualization should be instant in your browser, but this is of course a 2D table with precreated images. When we have to create fully animated 3D models in a 3D world instead, it quickly becomes too much. 

---

The main problem is that building an organism in 3D is expensive.

---

The main problem is that **building/visualizing an organism in 3D is expensive**. While I have done major rewrites of the code that builds plants and animals, mostly focusing on not doing things twice and skipping parts of the procedure that are not 100% necessary (like building the roots of plants that are underground anyway), creating new organisms from scratch remained, and still is, expensive.

Step 2: object pooling
----------------------

The textbook solution when a lot of objects need to be created and removed in a game is to use object pooling. The idea is that when an object dies (in The Sapling, quite literally), the game object is not destroyed but reincarnates as the next object that is created, instantly moving to the position of the newborn organism and resetting any animations it was showing. That is, you think you are looking at a large amount of objects being created and destroyed again, but in reality you are looking at a smaller amount of objects that are just changing locations quickly.

In the interactive example below, I have added a pool to the right. When plants die, their models are either immediately reused or are stored in the pool until they are needed again, so a lot less 3D models need to be created. Comparing this simulation to the one above, the difference becomes clear when you skip 10 days a few times; in the first simulation, the model number gets higher and higher, while here it stays low, reflecting the small number of 3D models that were created.

<div class="sim" id="pool">
</div>

<script>
	var sim = new Simulation();
	sim.usePool = true;
		
	elem = document.getElementById('pool');
	visualize_simulation(sim,elem,'pool','optimization/');	
</script>

Object pooling greatly improves the FPS in a stable ecosystem, as you can simply reuse what you already have and there is no need to create new objects on the fly. Unfortunately, in practice ecosystems in the game are very frequently unstable, most notably in the beginning of every new scenario when there is empty land to colonize. In other words, an object pool is not going to help if that pool is empty... so we'll also need a faster way to fill it.

Step 3: prebuilt organism library
---------------------------------

So far, when a plant was not available in the pool, we built it from scratch. If we are building a 3D model that we have built before, however, this is not necessary: why not store an example somewhere and just copy it? This is more expensive than taking an object from the pool, but way cheaper than building it from scratch. In the current example, there is a limited number of species (plant 1 and plant 2), so that would mean we only have to build a 3D model two times, and then be done with it.

<div class="sim" id="library">
</div>

<script>
	var sim = new Simulation();
	sim.usePool = true;
	sim.useLibrary = true;
		
	elem = document.getElementById('library');
	visualize_simulation(sim,elem,'library','optimization/');	
</script>

Note that this requires an ecosystem with mostly identical plants and animals... which is actually the case during the scenarios! In the sandbox mode, however, there is a *random mutations mode* that has a 30% chance of introducing a random change to a newborn plant or animal; that is, for 1 out of 3 newborn plants we won't have anything in the object pool AND the prebuilt organism library, so we're back to building from scratch.

Step 4: faking it and showing ancestors instead
-----------------------------------------------

I came with this final step when actually playing around with the (then still sluggish) random mutations mode in larger levels. The main insight is that in random mutations mode the player has no idea of what something is supposed to look like. For example, if a new plant is a little taller than its ancestors, but this is not shown to the player, will the player ever know? Almost certainly not, in particular if you take into account that the player is often looking at hundreds of plants and animals simultaneously. On the other hand, will the player notice performance problems? Yes, for sure... so a 100% smooth experience should get a higher priority than a 100% accurate visualization.

---

The player has no idea of what something is supposed to look like

---

In practice, this means that if random mutation leads to a completely new organism, the game will not automatically build it from scratch, even though it is not in the pool or the library. Instead, it will look at what was shown for the parent and show this instead. Later, when the game has time to breathe, the missing model might be added to the library. The game keeps track which organisms have a 'fake' appearance, and I can vary in how fast gaps in the library should be closed. Right now, I have settled on building a maximum of 1 organism per second. 

In the simulation below, random mutations are turned on for the first time. This means that after some time you will not only see plants like the ones you added yourself (plant 1 and plant 2); instead, the number will go up each time a newborn plants changes a little bit from its parent, so after some time you will see plant 3, plant 4, plant 5, etc. The accompanying model, however, will NOT change, meaning that the real plant and its 3D model go out of sync; the name will turn orange if this is the case. So you might see the model of a plant 1, while the text in orange tells you it is actually a plant 3. To catch up, you have to click the 'Add 1 model to library' button.

<div class="sim" id="ancestors">
</div>

<script>
	var sim = new Simulation();
	sim.usePool = true;
	sim.useLibrary = true;
	sim.fakeWithAncestors = true;
	sim.randomMutations = true;
		
	elem = document.getElementById('ancestors');
	visualize_simulation(sim,elem,'ancestors','optimization/');	
</script>

And this way, we have scaled back from building hundreds of 3D models per second to just one! Of course, there are a number of details, quirks and edge cases that I have left out of the explanation above to keep things simple. Two of them I want to mention to give you a more complete idea of the problem:

* In the simulation above, whenever you create a new 3D model, it's just the next one in line. In the real game, I'm trying to do this smarter by looking at which organisms are visually the most different from the 3D model they are using. That is, an animal that evolved an extra pair of feet is way more likely to get its model updated than a plant that evolved deeper underground roots.
* When you leave the simulation running for a longer period of time, hundreds of plant species emerge and go extinct again. This means the pool and library will endlessly grow... until you run out of RAM! To fix this, there is a mechanism that keeps track of which models are no longer used, and destroys them after some time to free up memory.

So, now the game is running at >60 FPS all the time, right? Well... it depends. The performance of the game depends on a large amount of factors: of course, the hardware plays a huge role, as do the quality settings, and any other things the computer might be doing at the same time. On top of that, it really matters what you are doing in the game: how large is the level, is the simulation sped up or not, how fast do the organisms reproduce, is the game camera close to the ground or not (close means more detail needs to be shown), and do you have random mutations turned on? While on the one hand there are numerous use cases where the game went from 0.5 FPS to 60 FPS, on the other it will definitely still drop below 30 if you are playing the sandbox mode (the largest level) with random mutations on, at the highest time speed, with the camera close to the action, shown on max quality settings, on a laptop.

Overall, though, the goal was that most players will have a smooth experience with larger levels, and with the optimizations described above I believe this was well achieved. This is why, after three months, I moved on to creating mechanics that were made possible because of these larger levels, which in turn led to the flower update. The things added in the flower update, in turn, open up a whole world of new possibilities, and I can't wait to share them with you.

The next devlog will announce a series of short videos; it will be published around a month from now. Follow [The Sapling on Twitter](https://twitter.com/thesaplinggame) or subscribe to the newsletter below if you are interested!

03-11-20