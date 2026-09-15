# Graph Report - Conic Section Visualizer  (2026-09-15)

## Corpus Check
- 12 files · ~65,837 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .css 1)

## Summary
- 112 nodes · 128 edges · 14 communities (9 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e887311a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Conic Section 3D Visualizer
- calculate
- Conic Section Visualizer — Codebase Guide
- app.js
- handler
- updateCameraLabels
- Dependency Installation
- Project Knowledge Graph
- Standalone Executable
- package.json
- conic.py
- Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend
- vercel.json
- render

## God Nodes (most connected - your core abstractions)
1. `solve()` - 9 edges
2. `calculate()` - 8 edges
3. `Conic Section Visualizer — Codebase Guide` - 7 edges
4. `scripts` - 6 edges
5. `Conic Section 3D Visualizer` - 6 edges
6. `Project Knowledge Graph` - 6 edges
7. `handler` - 5 edges
8. `Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend` - 4 edges
9. `_sample_nappe()` - 3 edges
10. `values()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `test_cone_dimensions()` --calls--> `solve()`  [EXTRACTED]
  test_conic.py → api/conic.py
- `test_invalid_dimensions()` --calls--> `solve()`  [EXTRACTED]
  test_conic.py → api/conic.py
- `test_known_sections()` --calls--> `solve()`  [EXTRACTED]
  test_conic.py → api/conic.py
- `test_slope_changes_classification()` --calls--> `solve()`  [EXTRACTED]
  test_conic.py → api/conic.py

## Import Cycles
- None detected.

## Communities (14 total, 5 thin omitted)

### Community 0 - "Conic Section 3D Visualizer"
Cohesion: 0.29
Nodes (7): Automatic Conic Classification, Conic Section 3D Visualizer, Double-Napped Cone, Interactive User Interface, Modular Software Architecture, OpenGL 3D Rendering, Real-Time Cone-Plane Intersection

### Community 1 - "calculate"
Cohesion: 0.22
Nodes (10): applyTheme(), calculate(), syncUrl(), updateCone(), updateConeLabels(), updateCurves(), updatePlane(), updateResults() (+2 more)

### Community 2 - "Conic Section Visualizer — Codebase Guide"
Cohesion: 0.25
Nodes (7): API, Conic Section Visualizer — Codebase Guide, Files, Geometry model, Local workflow, Purpose, Runtime architecture

### Community 3 - "app.js"
Cohesion: 0.07
Nodes (27): axes, axisLabels, camera, cameraFields, coneMaterial, controls, curves, fields (+19 more)

### Community 5 - "updateCameraLabels"
Cohesion: 0.67
Nodes (3): setCameraFromSliders(), syncCameraSliders(), updateCameraLabels()

### Community 7 - "Project Knowledge Graph"
Cohesion: 0.29
Nodes (7): Graph Report, graphify explain, graphify path, graphify query, Graphify Wiki, Incremental Graph Update, Project Knowledge Graph

### Community 9 - "package.json"
Cohesion: 0.12
Nodes (15): dependencies, three, devDependencies, vite, name, private, scripts, api (+7 more)

### Community 10 - "conic.py"
Cohesion: 0.24
Nodes (11): _clean(), _format_equation(), Vercel endpoint for cone-plane intersection geometry., run(), _sample_nappe(), solve(), Local entry point for the Python geometry API., test_cone_dimensions() (+3 more)

### Community 11 - "Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend, Source Nodes

## Knowledge Gaps
- **62 isolated node(s):** `form`, `submitButton`, `planeFields`, `fields`, `stage` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 70 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `three` connect `package.json` to `app.js`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **What connects `form`, `submitButton`, `planeFields` to the rest of the system?**
  _62 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `app.js` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._