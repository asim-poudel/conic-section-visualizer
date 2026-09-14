# Conic Lab

An interactive browser visualization of the curves created when a plane cuts a double-napped cone. The frontend is JavaScript and WebGL (Three.js); a small Python endpoint computes and classifies each intersection.

## Run Locally

Install once:

```bash
npm install
```

Run these in 2 terminals:

```bash
npm run api
npm run dev
```

Open `http://localhost:5173`.

## Test & Build

```bash
python test_conic.py
npm run build
```

## Deploy to Vercel

Import this repository in Vercel or run `npx vercel`. Vercel builds the Vite frontend and serves `api/conic.py` as a Python Function.

Put the 2 supplied backgrounds in `assets/` with `light` and `dark` in their filenames. The build selects them automatically; `public/gradient-background.png` remains the fallback. Background imagery is scoped to the 3D stage.

## Structure

- `index.html`, `app.js`, `styles.css` — accessible workspace and WebGL scene
- `api/conic.py` — validated cone-plane math and Vercel request handler
- `test_conic.py` — regression check for all 4 regular conic sections
- `main.py` and the other root Python modules — original desktop reference; not included in the web runtime

## Production

- This project was done as the project part of the coursework COMP342(Computer Graphics) KU DOCSE-III/II
