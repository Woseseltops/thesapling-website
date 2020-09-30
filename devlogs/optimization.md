Optimization: what I did to make the game 300 times faster
===========================================================

The first major update for The Sapling, the flower update, was released in September, and it looks like this:

[x]

Among other things (like, obviously, flowers), I addresses a major point of feedback to kept coming back: players wanted more space for their creations to grow and evolve. I couldn't easily make the levels larger, however, because the small levels already were a problem for the game's performance. The hard part is that there are not one, but two computationally heavy things going on at the same time: simulating an ecosystem where hundreds of organisms are all doing their own things (moving, eating, reproducing, mutating) AND visualizing these hundreds of objects. With larger levels, this would be thousands, essentially bringing the game to a halt with 1 frame per 5 seconds (FPS) instead of the regular 60 per 1 second. 

Besides my obvious desire to please the players, having larger levels was also crucial for my own ambitions with the game, because a number of the simulation mechanics didn't really work with the smaller maps; for example, why evolve an instinct to run away from a predator if you have nowhere the go? Or for plants, why evolve things like bark or high leaves if the biggest reason that your offspring is dying is because all seeds are landing on spots that are already taken? You better focus on getting as much offspring as possible, in the hopes that at least one of them by accident lands in a spot that is free.

In other words, if there was going to be one major feature in the first big update, it should be larger maps. To make this possible, I spent 3 months in the beginning of 2020 with that one focus: optimize, optimize, optimize the game's code, so I could get that FPS up and shave off more of the milliseconds it takes to render a scene. It was frustrating at times, but the main feeling I remember was actually excitement, as this really forced me to investigate the major bottlenecks (when I close my eyes, I can still see the Unity profiler), and come up with several new creative solutions for them. During this period I was reading a book about how John Carmack, the brilliant programmer behind the first Doom engine, was doing endless optimizations to make first person shooters a reality in the 90s, which was a great help in keeping me motivated.

While I implemented all kinds of larger and smaller ideas that made significant positive contributions to the performance of the game, there is one insight that had the biggest impact for the visualization part of the problem (how do you show thousands of unique organisms on screen?), which is to **fake it before you make it**. Let's go through my thought process step by step to see what I mean by that in this context. For every step, there is an interactive simulation you can run in your browser, so you can play with the idea yourself.

Step 1: the raw, unoptimized goal
----------------------------------

This is the basic idea, without any optimization: players can add their self created species somewhere in the world, and see whether it it strong enough to survive. In the interactive example below, you can add two species, 1 and 2, and then run the simulation. 

[x]

The simulation and subsequent visualization should be instant in your browser, but this is of course a 2D table with precreated images. When we have to create fully animated 3D models in a 3D world instead, it quickly becomes too much. The main problem is that **building/visualizing an organism in 3D is expensive**. While I have done major rewrites of the code that builds plants and animals, mostly focusing on not doing things twice and skipping parts of the procedure that are not 100% necessary (like building the roots of plants that are underground anyway), creating new organisms from scratch remained, and still is, expensive.

---
Building an organism in 3D is expensive
---

Step 2: object pooling
----------------------

The textbook solution when a lot of objects need to be created and removed in a game is to use object pooling. The idea is that when an object dies (in The Sapling, quite litterally), the game object is not destroyed but reincarnates as the next object that is created, instantly moving to the position of the newborn organism and resetting any animations it was showing. That is, you think you are looking at a large amount of objects being created and destroyed again, but in reality you are looking at a smaller amount of objects that are just changing locations quickly.

In the interactive example below, I have added a pool to the right. When plants die, their models are either immediately reused or are stored in the pool until they are needed again, so a lot less 3D models need to be created. Comparing this simulation to the one above, the difference becomes clear when you skip 10 days a few times; in the first simulation, the model number gets higher and higher, while here it stays low, reflecting the small number of 3D models that were created.

x 
Plant A
Organism 1334
Model 32

Oject pooling greatly improves the FPS in a stable ecosystem, as you can simply reuse what you already have and there is no need to create new objects on the fly. Unfortunately, in practice ecosystems in the game are very frequently unstable, most notably in the beginning of every new scenario when there is empty land to colonize. In other words, an object pool is not going to help if that pool is empty... so we'll also need a faster way to fill it.

Step 3: prebuilt organism library
---------------------------------

So far, when a plant was not available in the pool, we built it from scratch. If we are building a 3D model that we have built before, however, this is not necessary: why not store an example somewhere and just copy it? This is more expensive that taking an object from the pool, but way cheaper than building it from scratch. In the current example, there is a limited number of species (plant 1 and plant 2), so that would mean we only have to build a 3D model two times, and then be done with it.

x 
Plant A
Organism 1334
Model 32

Library: plant A

Note that this requires an ecosystem with mostly identical plants and animals... which is actually the case during the scenarios! In the sandbox mode, however, there is a *random mutations mode* that has a 30% chance of introducing a random change to a newborn plant or animal; that is, for 1 out of 3 newborn plants we won't have anything in the object pool AND the prebuilt organism library, so we're back to building from scratch.

Step 4: faking it and showing ancestors instead
-----------------------------------------------

I came with this final step when actually playing around with the (then still sluggish) random mutations mode in larger levels. The main insight is that in random mutations mode the player has no idea of what something is supposed to look like. For example, if a new plant is a little taller than its ancestors, but this is not shown to the player, will the player ever know that the plant shown is not 100% identical to what was in the underlying simulation? Almost certainly not, in particular if you take into account that the player is often looking at hundreds of plants and animals simultaneously. On the other hand, will the player notice performance problems? Yes, for sure... so a 100% smooth experience should get a higher priority than a 100% accurate visualization.

---
The player has no idea of what something is supposed to look like
---

In practice, this means that if an organism is born that is not in the pool AND not in the library, the game will not build it from scratch. Instead, it will look at what was shown for the parent and show this instead. Later, when the game has time to breathe, the missing model might be added to the library. The game keeps track which organisms have a 'fake' appearance, and I can vary in how hard I want to try to keep up. Right now, I have settled on building a maximum of 1 organism per second. In the simulation below, you have to do this 'keeping up' by hand: except for the first one, no new 3D models are created until you click the 'Add 1 model to library' button.

[x]

And this way, we have scaled back from building hundreds of 3D models per second to just one! Of course, there are a number of details, quirks and edge cases that I have left out of the explanation above to keep things simple. Two of them I want to mention to give you a more complete idea of the problem:

* In the simulation above, whenever you create a new 3D model, it's just the next one in line. In the real game, I'm trying to do this smarter by looking at which organism are visually the most different from the 3D model they are using. That is, an animal that evolved an extra pair of feet is way more likely to get its model updated than a plants that evolved deeper underground roots.
* When you leave the simulation running for a longer time, hundreds of plant species emerge and go extinct again. This means the pool and library will endlessly grow... until you run of RAM! To fix this, there is a mechanism that keeps track of which models are no longer used, and destroys them after some to free up memory.

So, now the game is running at >60 FPS all the time, right? Well... it depends. The performance of the game depends on a large amount of factors: of course, the hardware plays a huge role, as do the quality settings, and any other things the computer might be doing at the same time. On top of that, it really matters what you are doing in the game: how large is the level, is the simulation paused, running at normal or fast speed (faster means more has to be done in the same time, so less FPS), do you have random mutations turned on? The FPS will definitely still drop below 30 if you are playing the sandbox mode (the largest level) with random mutations on, at the highest time speed, with the max quality settings on a laptop. On the other hand, I believe that for most people, the experience will be smooth for most activities in the game; keep in mind the use case I started with, which when from 0.2 to 60 frames per second. This is why I moved on to creating mechanics that were made possible because of these larger levels, which in turn led to the flower update. These additions, in turn, open up a whole world of new possibilities, and I can't wait to share them with you.

Todo
====
No plants flashing when you click a button: don't refresh everything
