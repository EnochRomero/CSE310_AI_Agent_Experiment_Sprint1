# 2D PIE

This was a simple 2D game. The point of putting together this project was to get more familiar with using and working with AI agents, not to get better at pygames game making. I used pygames as a testing ground because it's something I haven't used before, and I wanted to see how easy it would be to use a new toolset with AI support.


## Instructions for Build and Use


Steps to build and/or run the software:


1. Install Python 3.10 or newer.
2. From the project folder, install the game dependency with `python -m pip install -r requirements.txt`.
3. Start the game with `python game.py`.


Instructions for using the software:


1. Move left and right with **A/D** or the **arrow keys**. The camera follows you as the world generates more platforms and enemies.
2. Jump with **Space**, **W**, or **Up**. Land on an enemy from above to stomp it; touching its side ends the run.
3. On the death screen, press **R** to restart or **Esc** to quit. You can also press **Esc** to quit during gameplay.


## Development Environment


To recreate the development environment, you need the following software and/or libraries with the specified versions:


* Python 3.10 or newer (developed and tested with Python 3.11.9).
* Pygame 2.5 or newer, below version 3 (tested with Pygame 2.6.1; see `requirements.txt`).
* Python's built-in `unittest` module for tests; no separate test package is required.


## Useful Websites to Learn More


I found these websites useful in developing this software:


* [Youtube](https://www.youtube.com/watch?v=5fhcklZe-qE&t=6s)
*[Youtube](https://www.youtube.com/watch?v=A4aLYwtpyes)
*[Youtube](https://www.youtube.com/watch?v=uwA3MMYBfAQ)


## Future Work


The following items I plan to fix, improve, and/or add to this project in the future:


* [ ] because this was an AI focused project for me, the program itself is very simple, and more depth should be added to the game play.
* [ ] I would like to make the game much more visually appealing.
* [ ] I would like to add some kind of win condition.
