# Challenge Name: Un cercle est un carré

---

## Statement

Alice and Bob live on a unique planet: it is neither flat nor spherical—it is a cube! They want to optimize their wired connection on the surface to minimize the latency of their communications.

The cube has dimensions of 32×32×32, and the format of the points where Alice and Bob live is like [0,2,14] or [32,28,11]. We can see that these points are located on the surface of their planet.

To minimize wired communication, Alice and Bob need to find the shortest surface distance between a series of point pairs. To simplify calculations and keep only integer values, the goal is to compute the square of the shortest path distance (on the surface) between each pair of points.

Using the previous example, the expected minimum surface path distance between [0,2,14] and [32,28,11] would be 3789. This path passes through the point [13,0,0].

Note: The provided file, un-cercle-est-un-carre.py, contains the server-side code that handles the service. We do not provide the file minimum_distance.py. This file is referenced because it is used to check your answers: your objective is to write the function minimumDistanceOnCube.

---

## Solution

To solve the challenge, I researched how to compute the shortest path **on the surface of a cube**.

The key steps:
- Understand that paths are not traveling through the interior but **on the faces** of the cube.
- Realize that the shortest path can involve **flattening the cube** ("unfolding" the faces) and measuring straight-line distances in 2D across connected faces.
- Try several unfoldings to find the minimum surface distance.

### References Used
- 📄 [Research paper: *Shortest Paths on Cubes* (Richard Goldstone, Rachel Roca, Robert Suzzi Valli)](https://arxiv.org/abs/2003.06096)
- 💻 [GitHub repository: *cuboid_shortest_paths*](https://github.com/Hermann-SW/cuboid_shortest_paths/tree/main)

These references explain mathematical models and algorithms for solving shortest paths on a cube's surface.

---

## Result

After implementing the solution based on those principles:

**Flag obtained:**

```
FCSC{a98d6d397bd7b91e8364bd98d52fdafa6a49e9ed2f5ba50186ae373eb1505d5f}
```
