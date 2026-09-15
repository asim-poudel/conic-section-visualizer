# Conic Lab

An interactive 3D view of the curves created when a plane cuts a double-napped cone.

- JavaScript and Three.js render the browser interface.
- Python computes, validates, and classifies cone-plane intersections.
- Cone height and slope are adjustable; the half-angle is derived from the slope.
- Mouse, touch, and wheel control the camera.

## Run locally

Requires Python 3.9+ and a current Node.js release.

```bash
npm install
```

Start the backend and frontend in separate terminals:

```bash
npm run api
npm run dev
```

Open `http://localhost:5173`. `main.py` starts only the Python API on port 8000; Vite serves the JavaScript frontend and proxies `/api` to it.

## Controls

- Set cone height and slope with the sliders. The displayed half-angle is `atan(slope)`.
- Enter `A`, `B`, `C`, and `D` for the plane `Ax + By + Cz + D = 0`.
- Drag the model to orbit and use the mouse wheel to zoom.
- Choose a preset to load a circle, ellipse, parabola, or hyperbola.

## Test and build

Run the backend regression checks and production frontend build together:

```bash
npm test
```

The tests cover the four regular conic sections, variable height, slope-dependent classification, clipping at the cone height, and invalid dimensions. Python uses only the standard library.

## Architecture

```text
Browser (index.html + app.js + styles.css)
        | POST /api/conic
        v
Python (api/conic.py)
        | JSON geometry + classification
        v
Three.js scene
```

- `main.py` — local Python API launcher
- `api/conic.py` — shared math, validation, local HTTP handler, and Vercel function
- `index.html`, `app.js`, `styles.css` — accessible browser controls and 3D renderer
- `test_conic.py` — dependency-free Python regression checks
- `vite.config.js` — local `/api` proxy
- `vercel.json` — deployment headers

## Deploy to Vercel

Import the repository in Vercel or run `npx vercel`. Vercel builds the Vite frontend and serves `api/conic.py` as a Python Function. Run `npm test` before deploying.

This project was created for COMP342 (Computer Graphics), KU DOCSE-III/II.
