---
type: "query"
date: "2026-09-14T04:43:23.492294+00:00"
question: "Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend"
contributor: "graphify"
outcome: "useful"
source_nodes: ["ConicVisualizer", "MathEngine", "UIManager", "Camera", "GraphicsEngine"]
---

# Q: Understand the complete current architecture before migrating the frontend to JavaScript and retaining Python for the backend

## Answer

Expanded from original query via graph vocab: [application, math, engine, interface, rendering, camera, events, intersection, pygame, opengl]. The project is a single-process Pygame/OpenGL desktop app. ConicVisualizer owns the event/render loop and coordinates UIManager, Camera, GraphicsEngine, and MathEngine. MathEngine is the future Python backend boundary; UIManager, Camera, and GraphicsEngine are browser-frontend concerns. The current design has no HTTP/API boundary. Verified issues include no tests, a wrong documented hyperbola sample, degenerate apex intersections represented as duplicate origin points, a hardcoded 720 sample count that bypasses config, direct MathEngine state mutation, and unused pygame-gui dependency.

## Outcome

- Signal: useful

## Source Nodes

- ConicVisualizer
- MathEngine
- UIManager
- Camera
- GraphicsEngine