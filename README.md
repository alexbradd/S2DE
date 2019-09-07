# S2DE: A Simple Event-Driven 2D Engine
S2DE (**S**imple **2D** **E**ngine) is a simple game engine wrote in python 3 on
top of the pygame library.  It's structure resembles that of the Unity3D game 
engine, from which borrows many terms and concepts such as GameObject, 
Component, Behaviour and Scene.

In S2DE the event system is the most important component because everything 
is moved by events. A diagram of the flow of said events can be found in
`docs/program-flowchart.png`.

## Features
- Small, lightweight and portable;
- Powerful event system;
- Useful abstractions such as Scenes and GameObjects;
- Displaying, loading and caching Scenes from disk;
- Extensibility through the addition of the user's own Components and Behaviours

## Repository structure
The repository contains two main folders:

- `engine`: where the engine source (`src`) and docs (`docs`) live
- `utils`: where some utilities to automate some processes live (like `compctl`)

## Requirements
- Python 3
- See `requirements.txt`

## Installation
Copy the contents of `engine/src` into the desired installation folder and run
by run the `launch` program.

