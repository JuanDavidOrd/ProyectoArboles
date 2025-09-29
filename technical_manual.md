Technical Documentation – AVL Car Game

1. Executive Summary
The AVL Car Game is a 2D pixel-art style game built with Python and Pygame. 
Its purpose is educational and recreational: it demonstrates the use of AVL trees to manage obstacles and providing an entertaining gameplay experience.

2. System Architecture
File/Folder Structure:
- models/ → Core data structures (Carrito, Obstaculo, AVLTree).
- controllers/ → Game logic (GameController, JSONLoader).
- views/ → Graphical interface (MenuView, GameView, EndView, AVLVisualizer).
- data/ → JSON configuration and obstacle storage.
- assets/ → Sprites for cars, obstacles, and road.
- main.py → Project entry point.

3. Explanation of Components
Models:
- Carrito: position, energy, speed, jumping logic.
- Obstaculo: x, y, type, damage, width, height.
- AVLTree: balanced insertion, rotations, in-order traversal.

Controllers:
- GameController: manages movement, collisions, win/lose condition.
- JSONLoader: loads and saves configuration.

Views:
- MenuView: main menu, add obstacle, view tree.
- GameView: renders road, car, HUD, obstacles.
- EndView: displays results and options.
- AVLVisualizer: obstacle structure visualization.

Main:
- Controls the flow: Menu → Game → End.

4. Data Flow
1. Player runs main.py.
2. JSONLoader loads obstacles from config.json into AVL tree.
3. MenuView opens (options: Play, Add Obstacle, View Tree, Exit).
4. If Play → creates Carrito and GameController.
5. GameView runs: controller updates logic, view updates visuals.
6. EndView shows win/lose results.

5. Algorithms
- AVL Balancing: rotations (LL, RR, LR, RL).
- Collision Detection: bounding box overlap on X and Y.
- Jump Timing: parabolic approximation using phase function.
- Obstacle Uniqueness: no duplicates at same (x,y).

6. Installation & Deployment
Requirements:
- Python 3.10+

Run game:
python main.py

