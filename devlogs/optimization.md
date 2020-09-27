'Larger levels would be nice', 'The grow areas are way too small', 'I need larger maps!'... It was a piece of feedback from players that kept coming back; the idea of a simulation with self created flora and fauna was well received, but the players wanted more space for their creations to grow and evolve. I couldn't easily make them larger, however, because the small levels already were a problem for the game's performance. The hard part is that there are not one, but two computationally heavy things going on at the same time: simulating an ecosystem where hundreds of organisms are all doing their own things (moving, eating, reproducing, mutating) AND visualizing these hundreds of objects. With larger levels, this would be thousands, essentially bringing the game to a halt with 1 frame per 5 seconds (FPS) instead of the regular 60 per 1 second. 

Besides my obvious desire to please the players, having larger levels was also crucial for my ambitions with the game, because a number of the simulation mechanics didn't really work with the smaller maps; for example, why evolve an instinct to run away from a predator if you have nowhere the go? Or for plants, why evolve things like bark or high leaves if the biggest reason that your offspring is dying is because all seeds are landing on spots that are already taken? You better focus on getting as much offspring as possible, in the hopes that at least one of them by accident lands in a spot that is free.

In other words, if there was going to be one major feature in the first big update, it should be larger maps. To make this possible, I spent 3 months in the beginning of 2020 with that one focus: optimize, optimize, optimize the game's code, so I could get that FPS up and shave off more of the milliseconds it takes to render a scene. It was frustrating at times, but the main feeling I remember was actually excitement, as this really forced me to investigate the major bottlenecks, and come up with several new creative solutions for them. During this period I was reading a book about how John Carmack, the brilliant programmer behind the first Doom engine, was doing endless optimizations to make first person shooters a reality in the 90s, which was a great help in keeping me motivated.

While I implemented all kinds of larger and smaller ideas that made significant positive contributions to the performance of the game, there is one insight that had the biggest impact for the visualization part of the problem (how do you show thousands of unique organisms on screen?), which is to **fake it before you make it**. Let's go through my thought process step by step to see what I mean by that in this context. For every step, there is an interactive simulation you can run in your browser, so you can play with the idea yourself.

Step 1: the raw, unoptimized goal
----------------------------------

This is the basic idea, without any optimization: players can add their self created species somewhere in the world, and see whether it it strong enough to survive. In the interactive example below, you can add two species, 1 and 2, and then run the simulation. 

[x]

The simulation and subsequent visualization should be instant in your browser. However, if you replace the precreated images in a 2D table with unique, fully animated 3D models created on the fly in a 3D world, it quickly becomes too much. The main problem is that **building/visualizing an organism in 3D is expensive**. While I have done major rewrites of the code that builds plants and animals, mostly focusing on not doing things twice and skipping parts of the procedure that are not 100% necessary (like building the roots of plants that are underground anyway), creating new organisms from scratch remained, and still is, expensive.

Step 2: object pooling
----------------------

The textbook solution when a lot of objects need to be created and removed in a game is to use object pooling. The idea is that when an object dies (in The Sapling, quite litterally), the game object is not destroyed but reincarnates as the next object that is created, instantly moving to the position of the newborn organism and resetting any animations it was showing. That is, you think you are looking at a large amount of objects being created and destroyed again, but in reality you are looking at a smaller amount of objects that are just changing locations really quickly.

In the interactive example below, I have added a pool to the right. When plants die, their models are either immediately reused or are stored in the pool until they are needed again. If you skip ahead 10 days a few times, you'll notice that the model nr stays low, or at least much lower than was the case without object pooling... fewer plants are created!

x 
Plant A
Organism 1334
Model 32

Oject pooling greatly improves the FPS in a stable ecosystem, as you can simply reuse what you already have and there is no need to create new objects from scratch. Unfortunately, in practice ecosystems in the game are very frequently unstable, most notably in the beginning of every new scenario when there is empty land to colonize. In other words, an object pool is not going to help if that pool is empty... so we'll also need a faster way to fill it.

Step 3: prebuilt organism library
---------------------------------

So far, when a plant was not available in the pool, we built it from scratch. In the interactive example, however, there is a limited number of species: plant 1 and plant 2. Instead of building the same 3D model from scratch over and over, let's store an example somewhere and just copy it. This is more expensive that taking an object from the pool, but way cheaper than building it from scratch.

x 
Plant A
Organism 1334
Model 32

Library: plant A

Note that this requires an ecosystem with mostly identical plants and animals... which is actually the case during the scenarios! In the sandbox mode, however, there is a *random mutations mode* that has a 30% chance of introducing a random change to a newborn plant or animal; that is, for 1 out of 3 plants we won't have anything in the object pool AND the prebuilt organism library, so we're back to building from scratch.

Step 4: faking it and showing ancestors instead
-----------------------------------------------

I came with this final step when actually implementing larger levels, and playing around with them: because random mutations mode is random, the player has no idea of what something is supposed to look like. For example, if a new plant is a little taller than its ancestors, but this is not shown to the player, will the player ever know that the plant s/he was shown is not 100% identical to what the underlying simulation was using? Probably not, especially if keep in mind that the player might be looking at hundreds of plants and animals simultaneously. Will the player notice performance problems? Yes, for sure.

This means that if an organism is born that is not in the pool and not in the library, the game will look at what was shown for the parent, and show this instead of building the real thing, until the game has time to build it. The game keeps track which organisms have a 'fake' appearance, and I can vary in how hard I want to try to keep up. Right now, I have settled on a maximum of 1 organism per frame.

[x]

,...

Todo
====
No plants flashing when you click a button: don't refresh everything
Text ending
Add to library functionality