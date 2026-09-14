# Graph Report - Conic Section Visualizer  (2026-09-14)

## Corpus Check
- 16 files · ~69,895 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .spec 1, .css 1)

## Summary
- 194 nodes · 266 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `21bdd989`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Conic Visualizer Technical Documentation
- UIManager
- Camera
- app.js
- GraphicsEngine
- ConicVisualizer
- Dependency Installation
- Project Knowledge Graph
- Standalone Executable
- package.json
- conic.py
- Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend
- vercel.json

## God Nodes (most connected - your core abstractions)
1. `UIManager` - 25 edges
2. `Camera` - 14 edges
3. `GraphicsEngine` - 13 edges
4. `ConicVisualizer` - 10 edges
5. `MathEngine` - 10 edges
6. `Conic Visualizer Technical Documentation` - 8 edges
7. `Conic Section 3D Visualizer` - 8 edges
8. `calculate()` - 7 edges
9. `Dependency Installation` - 7 edges
10. `solve()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Camera Controls` --semantically_similar_to--> `Camera System`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → documentation.txt
- `Angle-Based Conic Classification` --semantically_similar_to--> `Automatic Conic Classification`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → README.md
- `Conic Eccentricity` --semantically_similar_to--> `Eccentricity Formulas`  [INFERRED] [semantically similar]
  CONTROL_GUIDE.txt → documentation.txt
- `Automatic Conic Classification` --semantically_similar_to--> `Angle-Based Classification Algorithm`  [INFERRED] [semantically similar]
  README.md → documentation.txt
- `OpenGL 3D Rendering` --semantically_similar_to--> `Fixed-Function OpenGL Pipeline`  [INFERRED] [semantically similar]
  README.md → documentation.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Application Dependency Stack** — requirements_pygame, requirements_pyopengl, requirements_pyopengl_accelerate, requirements_numpy, requirements_pygame_gui [EXTRACTED 1.00]
- **Conic Mathematics Workflow** — control_guide_plane_equation, readme_real_time_intersection, documentation_parametric_intersection_algorithm, documentation_angle_based_classification, documentation_eccentricity_formulas [INFERRED 0.85]
- **Interactive Visualization System** — control_guide_camera_controls, readme_interactive_ui, documentation_camera_system, documentation_user_interface, documentation_real_time_updates [INFERRED 0.85]

## Communities (13 total, 2 thin omitted)

### Community 0 - "Conic Visualizer Technical Documentation"
Cohesion: 0.12
Nodes (24): Camera Controls, Cone Parameters, Angle-Based Conic Classification, Conic Section 3D Visualizer, Conic Eccentricity, Plane Equation, Angle-Based Classification Algorithm, Camera System (+16 more)

### Community 2 - "Camera"
Cohesion: 0.11
Nodes (10): Camera, Manages camera position and orientation, Handle mouse button press, Handle mouse button release, Handle mouse movement for rotation, Handle mouse scroll for zoom, Set rotation around X axis, Set rotation around Y axis (+2 more)

### Community 3 - "app.js"
Cohesion: 0.07
Nodes (32): applyTheme(), calculate(), camera, coneMaterial, controls, curves, fields, form (+24 more)

### Community 4 - "GraphicsEngine"
Cohesion: 0.11
Nodes (8): Camera Controller for 3D View Navigation Handles rotation, zoom, and pan…, Configuration and Constants for Conic Section Visualizer, GraphicsEngine, Graphics Engine for 3D Rendering with Anti-Aliasing and Smooth Shading, 3D SOLID conic section from analytical parametric curve, Conic Section 3D Visualizer - Main Application, Mathematical Engine for Conic Section Calculations PARAMETRIC EQUATIONS with…, UI Manager - Dark Grey Theme

### Community 5 - "ConicVisualizer"
Cohesion: 0.18
Nodes (4): ConicVisualizer, Perform intersection and classification, MathEngine, PARAMETRIC EQUATIONS with inside-cone check For hyperbola: only show points…

### Community 6 - "Dependency Installation"
Cohesion: 0.57
Nodes (8): System Dependencies, Dependency Installation, Python Dependency Manifest, NumPy, pygame, pygame-gui, PyOpenGL, PyOpenGL_accelerate

### Community 7 - "Project Knowledge Graph"
Cohesion: 0.29
Nodes (7): Graph Report, graphify explain, graphify path, graphify query, Graphify Wiki, Incremental Graph Update, Project Knowledge Graph

### Community 9 - "package.json"
Cohesion: 0.12
Nodes (14): dependencies, three, devDependencies, vite, name, private, scripts, api (+6 more)

### Community 10 - "conic.py"
Cohesion: 0.26
Nodes (8): _clean(), _format_equation(), handler, Vercel endpoint for cone-plane intersection geometry., _sample_nappe(), solve(), BaseHTTPRequestHandler, test_known_sections()

### Community 11 - "Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend, Source Nodes

### Community 12 - "vercel.json"
Cohesion: 0.33
Nodes (5): buildCommand, framework, headers, outputDirectory, $schema

## Knowledge Gaps
- **51 isolated node(s):** `form`, `submitButton`, `fields`, `stage`, `themeToggle` (+46 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 93 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UIManager` connect `UIManager` to `GraphicsEngine`, `ConicVisualizer`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `GraphicsEngine`, `ConicVisualizer`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `GraphicsEngine` connect `GraphicsEngine` to `ConicVisualizer`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `ConicVisualizer` (e.g. with `Camera` and `GraphicsEngine`) actually correct?**
  _`ConicVisualizer` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `form`, `submitButton`, `fields` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Conic Visualizer Technical Documentation` be split into smaller, more focused modules?**
  _Cohesion score 0.11594202898550725 - nodes in this community are weakly interconnected._
- **Should `Camera` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._