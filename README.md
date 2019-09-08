# S2DE: A Simple Event-Driven 2D Engine
S2DE (**S**imple **2D** **E**ngine) is a simple game engine wrote in python 3 on
top of the pygame library.  It's structure resembles that of the Unity3D game 
engine, from which borrows many terms and concepts such as GameObject, 
Component, Behaviour and Scene.

S2DE is 'event-driven', meaning that event system is the most important component: 
everything is moved by events.

The engine follows the KISS principle: it contains only the basic components, 
it is the task of the user to extend it by adding new Components or even 
expanding the core engine and fit it to their need. That's why 'simple' is in 
the name. 

## Features
- Small, lightweight and portable;
- Powerful event system;
- Useful abstractions such as Scenes and GameObjects;
- Displaying, loading and caching Scenes from disk;
- Extensibility through the addition of the user's own Components and Behaviours

## Requirements
- Python 3
- See `requirements.txt`

## Installation
Copy the contents of `engine/src` into the desired installation folder and run
by executing either `launch` (Linux and OSX) or `launch.bat` (Windows).

