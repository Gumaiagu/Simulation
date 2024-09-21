# Simulation

This is a simple project that shows a simple evolution of a randomized moving sprite.

## Version

The python version that this code was made is the 3.12.

## Libraries

You'll only install one library, the pygame.

```commandline
pip install pygame
```

## What does

It creates a window with 50 red points with eyes and 50 green points, the green points are the food, and the red points are the predators, that need to eat the foods to keep alive.

Everytime one predator eats one food, one copy of it is created in the wall of the window, it will have a different speed and field of view that can help or harm it.

If a predator don't eat in 10 seconds, it will die.

If there isn't any food in the screen, is created more food.

Is very easy to all the predators die, so, the simulation is restated every time that all the predators die.
