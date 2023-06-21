# **Simulation of an eco system**

### Controls
| Button | Does |
| --- | --- |
| R | Generates a new Map |
___

### Insides
The map gets generated with [Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise), if a point is unter a custom threshold the pixle gets blue, else the color is green. Relative to the threshold the points value gets converted into an lighter or darker color.
To save hardware resources the map gets saved as an image, that later gets drawn. *Also*  you can change the resolution1

The Plants spawn **random**, but **relativ** to the map-color. (Darker = More Plants)
You can add your own plants by creating a new class in **this** file! Your plant need to have a **tick** and **draw** funktion, and the values `gives_hunger` and `gives_thrist`.
`growes` means how many `plant.tick()`'s need to be done until the plant is fully grown, `grow` means what the current state of growes is.
`live_spand` means how many `plant.tick()`'s the plant lives, and `live_time`
means how long the plant allready alive. The Rest should be self explaining.
When a plant gets spawned the code **randomly selects** a class **from this file** to create an new plant.

All the rest can you figure out by your self :DD
___

### Required Modules
| Module | install |
|---|---|
| [pygame](https://pypi.org/project/pygame/) | `pip install pygame` |
| [perlin_noise](https://pypi.org/project/perlin-noise/) | `pip install perlin-noise` |

