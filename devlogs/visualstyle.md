Breakdown of the visual style of The Sapling
============================================

| Technical | Graphics |

How was the graphical style of The Sapling is achieved? In this interactive breakdown I'll show you, step by step. At the bottom there's an interactive scene so you can turn all individual effects on and off.

Writing game code and creating game graphics are two fundamentally different beasts, and what is fun about them is very different. Programming has the clear advantage when I'm inspired by another game and want to see if I can replicate a particular idea. For example, if I encounter a game mechanic that I like, I can do a quick internet search and the result is most likely a tutorial on how to build this kind of technology. If I like the graphics in a game, on the other hand, there's not much I can do other than endlessly combining tricks I already know and hope this by chance achieves the graphical style I was trying to reproduce.

---

I'll set a good example and explain in detail how to achieve the visual style of The Sapling

---

In this article I'd like to show you it doesn't have to be this way; I'll set a good example and explain in detail how to achieve the visual style of The Sapling. I will do this step by step with sliders so you can compare the impact of the effect, and at the end with an interactive scene so you can turn on and off everything to your heart's desire.

Subdivision
-----------
The Catmull-Clark subdivision algorithm is like a machine where you can put in a simple 3D object, and a smooth more detailed object comes out. Fun fact: the Catmull in the name is actually Edwin Catmull, former president of Pixar and Walt Disney Animation Studios. Implementing it was my first experiment in Unity, and with it I showed myself that I was able to do 3D game programming. The algorithm allows the game to work with basic shapes for the models of plants and animals under the hood, while they appear more realistic to the player.

<div class="img-comp-container">
  <div class="img-comp-img">
    <img src="visualstyle/1.PNG" width="300" height="200">
  </div>
  <div class="img-comp-img img-comp-overlay">
    <img src="visualstyle/0.PNG" width="300" height="200">
  </div>
</div>

Depth of Field
--------------
Depth of field is a fancy term for making the background blurry. I really like depth of field in film and photography as it guides what the viewer focuses on in a very natural way. Unfortunately it often does not work well in gaming contexts: in most situations, the player should be able to focus wherever s/he wants. On top of this, depth of field makes objects feel relatively small; depth of field on anything larger than a human makes it look like some kind of miniature version - although recent city building sims use this to their advantage to create a 'toy city' kind of feel. In The Sapling, depth of field is used when the player clicks a plant or animal to focus on it. Look at the background in the image below to see the effect.

<div class="img-comp-container">
  <div class="img-comp-img">
    <img src="visualstyle/2.PNG" width="300" height="200">
  </div>
  <div class="img-comp-img img-comp-overlay">
    <img src="visualstyle/1.PNG" width="300" height="200">
  </div>
</div>


Vignette
--------
A vignette can be many things, but I think its default meaning is to make the corners of an image darker. Unlike depth of field, I rarely like vignettes in film and photography but I almost always do in games. I guess it's because a really simple trick that most players won't actively notice, while it does give the game a more artistic look.

<div class="img-comp-container">
  <div class="img-comp-img">
    <img src="visualstyle/3.PNG" width="300" height="200">
  </div>
  <div class="img-comp-img img-comp-overlay">
    <img src="visualstyle/2.PNG" width="300" height="200">
  </div>
</div>

Water animation
---------------
A comment a lot of early playtesters gave was that the island looked empty and boring when you start. While I still haven't come up with a way to really fix this, I think that moving water makes the whole thing feel a little more alive. If you're into the technical terms, it's achieved by saving the effect of displacement modifier in Blender as shapekeys. You can turn the moving water on and off in the interactive scene below.

Gradient skyboxes
-----------------
I came up with this idea quite late in the development of the game (before that, the sky in The Sapling was simply always blue), but the effect on the overal atmosphere was enormous. Interestingly, this can be achieved in the Unity game engine by using 3 pixel textures like these ones (enlarged versions):

![](visualstyle/textures.png)

This is the effect for a single point in the day night cycle with a slider for comparison. In the interactive scene below, you can actually move through the whole cycle.

<div class="img-comp-container">
  <div class="img-comp-img">
    <img src="visualstyle/4.PNG" width="300" height="200">
  </div>
  <div class="img-comp-img img-comp-overlay">
    <img src="visualstyle/3.PNG" width="300" height="200">
  </div>
</div>


Colored lights
--------------
Of course, beautiful skies only work when it matches the colors of the rest of the world. This is mostly achieved by simply changing the colors of the lights of the game along with the sky. Like with the skyboxes, you can see the effect for one point in the day night cycle here, and for the whole cycle in the interactive scene below the article.

<div class="img-comp-container">
  <div class="img-comp-img">
    <img src="visualstyle/5.PNG" width="300" height="200">
  </div>
  <div class="img-comp-img img-comp-overlay">
    <img src="visualstyle/4.PNG" width="300" height="200">
  </div>
</div>

Color correction
----------------
Color correction has the same goal as the colored lights (color the world to fit with the sky), but with a different approach. Whereas colored lights have much more effect, color corrections create a more unified and pretty look. This made them great together.

<div class="img-comp-container">
  <div class="img-comp-img">
    <img src="visualstyle/6.PNG" width="300" height="200">
  </div>
  <div class="img-comp-img img-comp-overlay">
    <img src="visualstyle/5.PNG" width="300" height="200">
  </div>
</div>

Interactive scene
-----------------

<button onclick="ToggleVignette()">Toggle vignette</button><button onclick="ToggleDepthOfField()">Toggle depth of field</button><button onclick="ToggleSubdivision()">Toggle subdivision</button><button onclick="ToggleAnimatedWater()">Toggle animated water</button><button onclick="ToggleColoredLights()">Toggle colored lights</button><button onclick="ToggleGradientSkyBox()">Toggle gradient skybox</button><button onclick="ToggleColorGrading()">Toggle color grading</button>

<p>Slide to change where we are in the day-night cycle</p>

<input type="range" min="1" max="100" value="50" id="dayNightCycleSlider">

<script src="visualstyle/UnityProgress.js"></script>  
<script src="visualstyle/UnityLoader.js"></script>
<script>
  var gameInstance = UnityLoader.instantiate("gameContainer", "visualstyle/Builds.json", {onProgress: UnityProgress});
</script>

<div class="webgl-content">
  <div id="gameContainer" style="width: 750px; height: 600px"></div>
  <div class="footer">
  </div>
</div>

Want more like this? I write articles like this roughly once per month; you can subscribe for email reminders below! If you want more fine-grained info on my game development work, there also is a [Twitter account](https://twitter.com/thesaplinggame).

<script>
function initComparisons() 
{
  var x, i;
  /* Find all elements with an "overlay" class: */
  x = document.getElementsByClassName("img-comp-overlay");
  
  for (i = 0; i < x.length; i++) 
  {
    /* Once for each "overlay" element:
    pass the "overlay" element as a parameter when executing the compareImages function: */
    compareImages(x[i]);
  }
  
  function compareImages(img) 
  {
    var slider, img, clicked = 0, w, h;
    /* Get the width and height of the img element */
    w = img.offsetWidth;
    h = img.offsetHeight;
    /* Set the width of the img element to 50%: */
    img.style.width = (w / 2) + "px";
    /* Create slider: */
    slider = document.createElement("DIV");
    slider.setAttribute("class", "img-comp-slider");
    /* Insert slider */
    img.parentElement.insertBefore(slider, img);
    /* Position the slider in the middle: */
    slider.style.top = (h / 2) - (slider.offsetHeight / 2) + "px";
    slider.style.left = (w / 2) - (slider.offsetWidth / 2) + "px";
    /* Execute a function when the mouse button is pressed: */
    slider.addEventListener("mousedown", slideReady);
    /* And another function when the mouse button is released: */
    window.addEventListener("mouseup", slideFinish);
    /* Or touched (for touch screens: */
    slider.addEventListener("touchstart", slideReady);
     /* And released (for touch screens: */
    window.addEventListener("touchstop", slideFinish);
	
    function slideReady(e) 
	{
      /* Prevent any other actions that may occur when moving over the image: */
      e.preventDefault();
      /* The slider is now clicked and ready to move: */
      clicked = 1;
      /* Execute a function when the slider is moved: */
      window.addEventListener("mousemove", slideMove);
      window.addEventListener("touchmove", slideMove);
    }
	
    function slideFinish() 
	{
      /* The slider is no longer clicked: */
      clicked = 0;
    }
	
    function slideMove(e) 
	{
      var pos;
      /* If the slider is no longer clicked, exit this function: */
      if (clicked == 0) return false;
      /* Get the cursor's x position: */
      pos = getCursorPos(e)
      /* Prevent the slider from being positioned outside the image: */
      if (pos < 0) pos = 0;
      if (pos > w) pos = w;
      /* Execute a function that will resize the overlay image according to the cursor: */
      slide(pos);
    }
	
    function getCursorPos(e) 
	{
      var a, x = 0;
      e = e || window.event;
      /* Get the x positions of the image: */
      a = img.getBoundingClientRect();
      /* Calculate the cursor's x coordinate, relative to the image: */
      x = e.pageX - a.left;
      /* Consider any page scrolling: */
      x = x - window.pageXOffset;
      return x;
    }
	
    function slide(x) 
	{
      /* Resize the image: */
      img.style.width = x + "px";
      /* Position the slider: */
      slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + "px";
    }
  }
}

initComparisons();
</script>

<script>
    var slider = document.getElementById("dayNightCycleSlider");    
    slider.oninput = function()
    {
     gameInstance.SendMessage('Controller','SetPositionInDayNightCycle',this.value/100);    
    } 


    function ToggleVignette()
    {
       gameInstance.SendMessage('Controller', 'ToggleVignette');
    }

    function ToggleDepthOfField()
    {
       gameInstance.SendMessage('Controller', 'ToggleDepthOfField');
    }

    function ToggleSubdivision()
    {
       gameInstance.SendMessage('Controller', 'ToggleSubdivisionIterations');
    }
    
    function ToggleAnimatedWater()
    {
       gameInstance.SendMessage('Controller', 'ToggleAnimatedWater');
    }

    function ToggleColoredLights()
    {
       gameInstance.SendMessage('Controller', 'ToggleColoredLights');
    }

    function ToggleGradientSkyBox()
    {
       gameInstance.SendMessage('Controller', 'ToggleGradientSkyBox');
      }     

    function ToggleColorGrading()
    {
       gameInstance.SendMessage('Controller', 'ToggleColorGrading');
      }     
</script>

13-02-20