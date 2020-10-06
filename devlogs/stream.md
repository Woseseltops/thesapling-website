Running The Sapling for 7 days straight: this is what happened
==============================================================

| Announcement |

To celebrate the release of the flower update of The Sapling, there was a 1 week live stream of the game on Twitch in the beginning of September. I have now created a video that summarizes and explains the most important things that happened.

It seemed a rather innocent idea: a week before the release of the flower update, rent a cheap gaming setup in the cloud, let it stream The Sapling with random mutations on, and watch what happens. When testing this idea, however, it turned out that there is a lot of time for things to go wrong when streaming 24/7... so everything that can possibly go wrong will eventually: think of memory leaks that only show up after hours of play, or connection hiccups that make the streaming software stop (switched to StreamLabs last moment, which solved everything). It all resulted in many sleepless hours, but also in many fixed bugs.

To make sure that a crash of the game didn't result in multiple days of progress being reset, I implemented a mechanism that made regular backups of the save file. It wasn't needed in the end, but had the unintended side effect that I can now go back to various stages in the 1 week simulation and relive what happened. To share this experience with all of you, I made a video of it:

<iframe id="ytvideo" src="https://www.youtube.com/embed/flmm-Y5KePo" frameborder="0" allowfullscreen=""></iframe>

The next devlog will be an interactive dive into the details of the optimizations I have to make the flower update work; it will be published around a month from now. Follow [The Sapling on Twitter](https://twitter.com/thesaplinggame) or subscribe to the newsletter below if you are interested!

06-10-20