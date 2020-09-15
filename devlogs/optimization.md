A piece of feedback from playtesters that kept coming back was that the levels were too small. ... spent 3 months with 1 focus: getting more FPS (frames per second), so . I was forced to come up with one solution after the other, always trying to shave off the milliseconds it took to render a scene. The hard part is that there are not one, but two things going on, simultaneously, that are computationally intensive: simulation an ecosystem where thousands of organisms are all doing there own things, reproducing, mutating, etc AND visualizing these thousands of subjects. During this period I was reading a book about John Carmack, the brilliant programmer behind the first Doom engine, in a similar way was doing endless optimizations to make first person shooters a reality, which was a great help in keeping me motivated.

While I added all kinds of larger and smaller ideas that made significant positive contributions to the performance of the game, there is one insight that had the biggest impact for the visualization part of the problem (how do you show thousands of different organisms on screen?), so this is the one I would like to share here. The main idea is to **fake it before you make it**, but let's go through my thought process step by step to see what I mean by that in this context. For every step, there is an interactive simulation you can run in your browser, so you can play with the idea yourself.

Step 1: the raw, unoptimized goal

[x]

Step 2: object pooling

[x]

Step 3: prebuilt organism library

[x]

Step 4: faking it and showing ancestors instead

[x]