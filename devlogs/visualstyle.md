Breakdown of the visual style of The Sapling
============================================

Writing game code and creating game graphics are two fundamentally different beasts, with very different upsides and downsides. One area where programming has the clear advantage, is when you're inspired by another game and want to see if you can replicate a particular idea. If I encounter a game mechanic that I like, I can do a quick internet search and the result is most likely a tutorial on how to build this kind of technology. If I like the graphics in a game, on the other hand, there's not much I can do other than endlessly combining tricks I already know and hope this by chance achieves the graphical style I was trying to reproduce.

In this article I'd like to show you it doesn't have to be this way; I'll set a good example and explain in detail how to achieve the visual style of The Sapling. I will do this step by step with sliders so you can compare the impact of the effect, and at the end with an interactive scene so you can turn on and off everything at your heart's desire.

Subdivision
-----------
The Catmull-Clark subdivision algorithm is what started this whole project. It's like a machine where you can put in a simple 3D object, and a smooth more detailed object comes out. Implementing it was my first experiment in Unity, and with it showed myself that I was able to do 3D game programming. I allows me to work with basic shapes for the models of plants and animals under the hood, while they appear more realistic to the player.

[x]

Depth of Field
--------------
I really like depth of field in film and photography as it guides what the viewer focuses on in a very natural way. Unfortunately it does not work really well in most gaming contexts: in most situations, the player should be able to focus wherever s/he wants. On top of this, depth of field makes objects feel relatively small; depth of field on anything larger than a human makes it look like some kind of miniature version - although some recent city building sims use this to their advantage to create a 'toy city' kind of feel. In The Sapling, the only place I thought depth of field worked well is when the player clicks a plant or animal to focus on it. Look at the background in the image below to see the effect.

[x]

Vignette
--------
Unlike depth of field, I rarely like vignettes in film and photography but I almost always do in games. I guess it's because a really simple trick that most players won't actively notice, while it does give the game a more artistic and modern look.

Water animation
---------------
A comment a lot of early playtesters gave was that the island looked empty and boring when you start. While I still haven't come up with a way to really fix this, I think that moving water makes the whole thing feel a little more alive. It's achieved by saving [x] animation in Blender as shapekeys.

Gradient skyboxes
-----------------
I came up with this idea quite late in the development of the game (before that, the sky in The Sapling was simply always blue), but the effect on the overal atmosphere was enormous. Interestingly, I've achieved in the Unity game engine by using 3 pixel textures like these ones (enlarged versions):

[x]

This is the effect for a single point in the day night cycle with a slider for comparison. In the interactive scene below, you can actually move through the whole cycle.

[x]

Colored lights
--------------
Of course, beautiful skies only work when it matches the colors of the rest of the world. This is mostly achieved by simply changing the colors of the lights of the game along with the sky. Like with the skyboxes, you can see the effect for one point in the day night cycle here, and for the whole cycle in the interactive scene below the article.

Color correction
----------------
Color correction has the same goal as the colored lights (color the world to fit with the sky), but with a different approach. Whereas colored lights have much more effect, color corrections create a more unified and pretty look. This made them great together.

[x]

[x]


---

Whereas I code with a clear goal in mind and confidence I can make it (this is often overconfidence, but only rarely does a quick internet search not provide the answer) as long as I have the time to step by step approach my goal, creating graphics is much more like endlessly throwing things at the wall and see what sticks. I only know what I wanted once I see it, and I'm unsure if I'll ever reach my goal until I reach it. Or to make the difference more concrete: 