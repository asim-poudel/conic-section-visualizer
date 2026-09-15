# Conic Section Visualizer — Codebase Guide

## Purpose

Conic Lab visualizes the intersection of a plane and a configurable double-napped cone. The browser renders the scene and owns the controls; Python validates inputs, calculates intersection samples, and classifies the conic.

## Runtime architecture

```text
index.html
    └─ app.js + styles.css
          ├─ Three.js scene and camera controls
          ├─ cone height and slope controls
          └─ POST /api/conic
                    └─ api/conic.py
                          ├─ validates inputs
                          ├─ samples both cone nappes
                          └─ returns JSON geometry and classification
```

There is one frontend and one backend. `main.py` is only a local launcher for the same Python handler used by deployment.

## Files

| File | Responsibility |
|---|---|
| `index.html` | Accessible controls, visualization stage, and result markup |
| `app.js` | Three.js rendering, form state, mouse/touch camera interaction, and API calls |
| `styles.css` | Responsive light/dark presentation |
| `api/conic.py` | Cone-plane math, validation, HTTP handler, and local server |
| `main.py` | Local Python API entry point |
| `test_conic.py` | Dependency-free backend regression checks |
| `vite.config.js` | Proxies local `/api` requests to Python on port 8000 |
| `vercel.json` | Deployment response headers |

## Geometry model

The double cone is:

```text
x² + y² = slope² × z²
−height ≤ z ≤ height
```

The cutting plane is:

```text
Ax + By + Cz + D = 0
```

For each sampled azimuth `θ`, the backend solves the plane equation on each nappe and retains points inside the configured height. The cone half-angle is `atan(slope)`. Comparing it with the plane angle determines whether the regular section is a circle, ellipse, parabola, or hyperbola. A plane through the apex is reported as degenerate.

## API

`POST /api/conic` accepts JSON:

```json
{
  "a": 0,
  "b": 0,
  "c": 1,
  "d": -2,
  "height": 5,
  "slope": 1
}
```

`height` defaults to `5` and `slope` defaults to `1` for older callers. The response includes the classification, explanation, angles, eccentricity, normalized equation, dimensions, point count, and curve branches.

## Local workflow

```bash
npm install
npm run api
npm run dev
```

Run `npm test` before deployment. It executes the Python regression checks and the Vite production build.
