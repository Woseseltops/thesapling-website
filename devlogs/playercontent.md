How player content works in The Sapling
=======================================

| Technical details |

The Sapling was built from the ground up with community interaction in mind. This interaction goes both ways: players can take stuff generated by or for the game, and use it in their own creations, or they can add their own creations to the game. 

This article functions as an in-depth guide on how to do this, to be used as reference. It's a living document that will be updated continuously. If you find any mistakes, or have more ideas you want to share with other creators, drop me a line at thesaplinggame@gmail.com .


1 Repurpose material from the game for your own creations
---------------------------------------------------------
Reusing material from the Sapling for non-commercial creative purposes is highly encouraged. These three things should help with that:

### 1.1 Music

The music in the Sapling is generated on the fly by combining smaller parts. If you are a musician, you are encouraged to reuse them; for example in remixes and mashups. The sheet music could be the basis for covers. I'd love to see your project; let me know at thesaplinggame@gmail.com .

* [Smaller musical pieces used by the procedural music engine](/static/procedural_music_pieces.zip).

* [Separate layers used in the main theme](/static/separate_layers_main_theme.zip).

* [Sheet music for the main theme](/static/main_theme_sheet_music.pdf).

### 1.2 Exporting animals and animations generated by the game

Pressing the `e` button in the plant or animal editor will create a `.obj` file in the game's *persistent storage* location. On Windows, this is most likely `C:\Users\YourUserName\AppData\LocalLow\Wessel Stoop\The Sapling` , on Mac and Linux it is probably `~/Library/Application Support/Wessel Stoop/The Sapling` . The `.obj` file contains the 3D model of your animal, and can be imported by most (all?) 3D modeling software. In game, these models are softened with one layer of [Catmull-Clark subdivision](https://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface), so you might also want to do that in your modeling software.

In the animal editor, a number of `.json` files are also created besides the `.obj` file:

* `ExportedBones.json`, containing information on the armature the game has generated.

* `ExportedBoneWeights.json`, containing information on how this armature interacts with the 3D model.

* `ExportedAnimation_<ANIMATION_NAME>.json`, for each of the animations the game uses, containing information on how each bone moves at each point in time during this animation.

The JSON format can easily be interpreted by any programming language, so it should be easy to write a script to import it to your 3D animation software of choice. I use animation software Blender with Python as a scripting language; a setup for importing animals and their animations can be found in the game's folders, in `the_sapling_Data/Resources/ImportJSON.blend`.

### 1.3 Using gameplay statistics

To get a better understanding of the way people play the game, various gameplay statistics are collected anonymously. They are saved in the form of _events_, logged in a separate file per IP address. Examples of events are:

* Open an editor

* Toggle the species list view

* Toggle random mutations

* Reach a milestone

* Fail a scenario

I hope to have set up this system in such way that I can turn these raw data into useful statistics as soon as I have a quantitative question in the future. However, this dataset is much too interesting to keep for myself. For that reason [[to be continued]]. If you're interested, you can use this data to create things like beautiful infographics, realtime dashboards, interactive visualizations, you name it.

2 Extending the game
--------------------

All scenarios and bodyparts are dynamically read from the `the_sapling_Data/Resources/` folder when the games starts; adding scenarios and bodyparts simply means adding more of the required files, and the game will handle the rest.

### 2.1 Adding your own scenarios

In the game's files, the various scenarios are identified with a number: the first four main scenarios are called 0, 1, 2 and 3. This numbering is also used to order the scenarios. To prevent clashes with future main scenarios or other custom scenarios, it's probably best to give your custom scenario a 2-digit identifier.

To add your scenario to the game, you need to add the following files in the appropriate subfolders of the `the_sapling_Data/Resources/Scenarios/` folder:

* A `.fbx` file with the 3D model of the terrain, as well as various other positions like where the camera positions and the clouds are. Most (all?) 3D modeling software will be able to export to FBX. The names of the various objects in the scene are important; probably the most efficient way to understand what needs to go where is to simply look at the examples included with the game, but here's a list for convenience:
    
    * All objects with the name 'Sea' or 'River' are given the water material.
    
    * All objects with names starting with 'SurfaceRock' or 'SideRock' are given the grey stone material.
    
    * All objects with names starting with 'Mainland' are given the brown stone material.
    
    * The position and size of objects (probably best: flat planes) with names starting with 'GrowArea' are used as indicators where plants can grow and animals can walk.
    
    * The positions of the objects with names 'CameraMainPosition', 'CameraOverviewPosition', or names starting with 'CameraPreset' are used for these respective camera positions.
    
    * The height of the object with the name 'CloudsPosition' determines where clouds will spawn.
    
    * All objects that start with 'Event<INTEGER>' will only become visible as soon as the corresponding event (defined in the json file, see next bullet) occurs.

* A `.json` file where you specify various things, like the level descpription, the objective, the various soil layers and what milestones are available. You should follow the exact format of the existing `.json` files, or the game will crash.

* A 80x80px `.png` icon to be used in the main menu.

* If you specified camera presets in your `.fbx` file, they need to have accompanying buttons to be used in the interface. Each icon has a separate image for (1) a normal state, (2) a hovered state and (3) a selected state. If you follow the naming convention rigorously, the game will figure out where to put everything automatically: `2_preset_1_hovered.png` means level 2, camera preset 1, hovered state. You can specify the location of the buttons on screen in the json file.

### 2.2 Adding your own bodyparts

To get your bodypart working, you need to add the following files to the correct subfolder of the `the_sapling_Data/Resources/Bodyparts` folder:

* A `.json` file where you specify various things, like its statistics in the simulation, its place in the evolution tree, and the index of the face of the model that will be attached to the main mesh. I personally don't know of a smart way to figure out this face index; I do it by trial and error.

* A `.obj` file, containing the mesh of the bodypart. Most (all?) 3D modeling software will be able to export to .obj . Keep in mind that the game will dynamically apply an extra iteration of Catmull-Clark subdivision, so your meshes should be simple.

* If your bodypart is a limb or a mouth, a `.armature` file containing information on the locations of the bones and the weights for each of the vertices. These weights define how much influence the position of a particular bone has on the vertex. This file, which also uses the JSON format, contains a list of bones, with for each bone the (1) bone name, which is used by the procedural animation system, (2) 3D position of the bone, relative to the bodypart, and (3) a list of weights for each vertex in the `.obj` file. For each vertex, the weights of all bones should add up to one. Besides the main bones, it also possible to define bones for children, which are submeshes of the bodypart, like teeth.

The subfolder you choose defines as what kind of bodypart (is this a leaf or an eyeball?) your creation will be interpreted.

15-09-18