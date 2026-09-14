# Graph Report - COMP342_CONIC3D  (2026-09-14)

## Corpus Check
- Corpus is ~6,399 words - fits in a single context window. You may not need a graph.

## Summary
- 119 nodes · 179 edges · 9 communities (6 shown, 3 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Domain Documentation
- Pygame UI Layer
- Camera Controls
- Application and Math Core
- Python Module Structure
- OpenGL Rendering
- Python Dependencies
- Graphify Tooling
- Desktop Packaging

## God Nodes (most connected - your core abstractions)
1. `UIManager` - 25 edges
2. `Camera` - 14 edges
3. `GraphicsEngine` - 13 edges
4. `ConicVisualizer` - 10 edges
5. `MathEngine` - 10 edges
6. `Conic Section 3D Visualizer` - 8 edges
7. `Conic Visualizer Technical Documentation` - 8 edges
8. `Dependency Installation` - 7 edges
9. `Project Knowledge Graph` - 6 edges
10. `System Dependencies` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Conic Section 3D Visualizer` --semantically_similar_to--> `Conic Section 3D Visualizer`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → README.md
- `Camera Controls` --semantically_similar_to--> `Camera System`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → documentation.txt
- `Angle-Based Conic Classification` --semantically_similar_to--> `Automatic Conic Classification`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → README.md
- `Conic Eccentricity` --semantically_similar_to--> `Eccentricity Formulas`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → documentation.txt
- `Conic Section 3D Visualizer` --semantically_similar_to--> `Conic Visualizer Technical Documentation`  [INFERRED] [semantically similar]
  README.md → documentation.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Conic Mathematics Workflow** — control_guide_plane_equation, readme_real_time_intersection, documentation_parametric_intersection_algorithm, documentation_angle_based_classification, documentation_eccentricity_formulas [INFERRED 0.85]
- **Interactive Visualization System** — control_guide_camera_controls, readme_interactive_ui, documentation_camera_system, documentation_user_interface, documentation_real_time_updates [INFERRED 0.85]
- **Application Dependency Stack** — requirements_pygame, requirements_pyopengl, requirements_pyopengl_accelerate, requirements_numpy, requirements_pygame_gui [EXTRACTED 1.00]

## Communities (9 total, 3 thin omitted)

### Community 0 - "Domain Documentation"
Cohesion: 0.12
Nodes (24): Camera Controls, Cone Parameters, Angle-Based Conic Classification, Conic Section 3D Visualizer, Conic Eccentricity, Plane Equation, Angle-Based Classification Algorithm, Camera System (+16 more)

### Community 2 - "Camera Controls"
Cohesion: 0.11
Nodes (10): Camera, Manages camera position and orientation, Handle mouse button press, Handle mouse button release, Handle mouse movement for rotation, Handle mouse scroll for zoom, Set rotation around X axis, Set rotation around Y axis (+2 more)

### Community 3 - "Application and Math Core"
Cohesion: 0.18
Nodes (4): ConicVisualizer, Perform intersection and classification, MathEngine, PARAMETRIC EQUATIONS with inside-cone check For hyperbola: only show points…

### Community 4 - "Python Module Structure"
Cohesion: 0.23
Nodes (6): Camera Controller for 3D View Navigation Handles rotation, zoom, and pan…, Configuration and Constants for Conic Section Visualizer, Graphics Engine for 3D Rendering with Anti-Aliasing and Smooth Shading, Conic Section 3D Visualizer - Main Application, Mathematical Engine for Conic Section Calculations PARAMETRIC EQUATIONS with…, UI Manager - Dark Grey Theme

### Community 6 - "Python Dependencies"
Cohesion: 0.57
Nodes (8): System Dependencies, Dependency Installation, Python Dependency Manifest, NumPy, pygame, pygame-gui, PyOpenGL, PyOpenGL_accelerate

### Community 7 - "Graphify Tooling"
Cohesion: 0.29
Nodes (7): Graph Report, graphify explain, graphify path, graphify query, Graphify Wiki, Incremental Graph Update, Project Knowledge Graph

## Knowledge Gaps
- **11 isolated node(s):** `graphify query`, `graphify path`, `graphify explain`, `Graphify Wiki`, `Graph Report` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 47 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UIManager` connect `Pygame UI Layer` to `Application and Math Core`, `Python Module Structure`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera Controls` to `Application and Math Core`, `Python Module Structure`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `GraphicsEngine` connect `OpenGL Rendering` to `Application and Math Core`, `Python Module Structure`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `ConicVisualizer` (e.g. with `Camera` and `GraphicsEngine`) actually correct?**
  _`ConicVisualizer` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify query`, `graphify path`, `graphify explain` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Domain Documentation` be split into smaller, more focused modules?**
  _Cohesion score 0.11594202898550725 - nodes in this community are weakly interconnected._
- **Should `Camera Controls` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._