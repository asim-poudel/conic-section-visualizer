import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import "./styles.css";

const $ = (selector) => document.querySelector(selector);
const form = $("#plane-form");
const submitButton = form.querySelector('[type="submit"]');
const fields = ["a", "b", "c", "d"].map((name) => form.elements[name]);
const stage = $("#scene");
const themeToggle = $("#theme-toggle");
const themeImages = {
  light: "/assets/blurry-gradient-light.png",
  dark: "/assets/blurry-gradient-dark.png",
};
const presets = {
  circle: [0, 0, 1, -2],
  ellipse: [0, 0.45, 1, -2],
  parabola: [0, 1, 1, -2],
  hyperbola: [0, 1.7, 1, -1],
};
const sectionMeta = {
  Circle: ["○", "The plane crosses one nappe at the same height in every direction."],
  Ellipse: ["⬭", "The tilted plane crosses one nappe and closes before reaching the cone’s rim."],
  Parabola: ["⌒", "The plane runs parallel to one generator of the cone, so the section stays open."],
  Hyperbola: ["⤢", "The plane reaches both nappes, producing 2 separate open branches."],
  Degenerate: ["×", "The plane passes through the apex, collapsing the usual section into a limiting case."],
};

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
stage.append(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
camera.up.set(0, 0, 1);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.enableZoom = false;
controls.enablePan = false;
controls.target.set(0, 0, 0);
camera.position.set(11, -11, 8);

scene.add(new THREE.HemisphereLight(0xeef7ff, 0x28364e, 2.6));
const keyLight = new THREE.DirectionalLight(0xffffff, 3.2);
keyLight.position.set(5, -4, 8);
scene.add(keyLight);

const model = new THREE.Group();
scene.add(model);
const coneMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x31475a,
  transparent: true,
  opacity: 0.88,
  roughness: 0.35,
  metalness: 0.05,
  side: THREE.DoubleSide,
  depthWrite: false,
});
const planeMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x5a6b5c,
  transparent: true,
  opacity: 0.84,
  roughness: 0.42,
  side: THREE.DoubleSide,
  depthWrite: false,
});
const sectionMaterial = new THREE.MeshBasicMaterial({ color: 0xb85d3b });
const sectionGlowMaterial = new THREE.MeshBasicMaterial({ color: 0xb85d3b, transparent: true, opacity: 0.34, blending: THREE.AdditiveBlending, depthWrite: false });
const sectionFillMaterial = new THREE.MeshBasicMaterial({ color: 0xb85d3b, transparent: true, opacity: 0.44, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false });

const upperCone = new THREE.Mesh(new THREE.ConeGeometry(5, 5, 72, 1, true), coneMaterial);
upperCone.rotation.x = -Math.PI / 2;
upperCone.position.z = 2.5;
const lowerCone = new THREE.Mesh(new THREE.ConeGeometry(5, 5, 72, 1, true), coneMaterial);
lowerCone.rotation.x = Math.PI / 2;
lowerCone.position.z = -2.5;
model.add(upperCone, lowerCone);

const grid = new THREE.GridHelper(10, 10, 0x718b9a, 0x526a78);
grid.rotation.x = Math.PI / 2;
grid.material.transparent = true;
grid.material.opacity = 0.18;
model.add(grid, new THREE.AxesHelper(3.25));

function axisLabel(text, color, position) {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 48;
  const context = canvas.getContext("2d");
  context.fillStyle = color;
  context.font = "600 20px IBM Plex Sans";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(text, 24, 24);
  const label = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(canvas), transparent: true, depthTest: false }));
  label.position.set(...position);
  label.scale.set(0.28, 0.28, 1);
  model.add(label);
}

axisLabel("x", "#e56b6f", [3.55, 0, 0]);
axisLabel("y", "#79b77c", [0, 3.55, 0]);
axisLabel("z", "#73a9ee", [0, 0, 3.55]);

let planeMesh;
let curves = [];
let requestId = 0;

function values() {
  return Object.fromEntries(fields.map((field) => [field.name, Number(field.value)]));
}

function validate(params) {
  if (Object.values(params).some((value) => !Number.isFinite(value))) return "Enter a number in every coefficient field.";
  if (Math.hypot(params.a, params.b, params.c) < 1e-9) return "A, B, and C cannot all be 0. Change at least one coefficient.";
  return "";
}

function updatePlane({ a, b, c, d }) {
  if (planeMesh) model.remove(planeMesh);
  const normal = new THREE.Vector3(a, b, c).normalize();
  planeMesh = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), planeMaterial);
  planeMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), normal);
  planeMesh.position.copy(normal).multiplyScalar(-d / Math.hypot(a, b, c));
  model.add(planeMesh);
}

function updateCurves(branches) {
  curves.forEach((curve) => {
    model.remove(curve);
    curve.geometry.dispose();
  });
  curves = branches.filter((points) => points.length > 1).flatMap((points) => {
    const vectors = points.map(([x, y, z]) => new THREE.Vector3(x, y, z));
    const closed = vectors.length > 3 && vectors[0].distanceTo(vectors.at(-1)) < 0.08;
    const path = new THREE.CatmullRomCurve3(vectors, closed, "centripetal");
    const segments = Math.max(24, vectors.length);
    const border = new THREE.Mesh(new THREE.TubeGeometry(path, segments, 0.075, 8, closed), sectionMaterial);
    const glow = new THREE.Mesh(new THREE.TubeGeometry(path, segments, 0.16, 8, closed), sectionGlowMaterial);
    const objects = [glow, border];

    if (closed) {
      const ring = vectors.slice(0, -1);
      const center = ring.reduce((sum, point) => sum.add(point), new THREE.Vector3()).divideScalar(ring.length);
      const positions = [];
      ring.forEach((point, index) => {
        const next = ring[(index + 1) % ring.length];
        positions.push(center.x, center.y, center.z, point.x, point.y, point.z, next.x, next.y, next.z);
      });
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
      geometry.computeVertexNormals();
      objects.unshift(new THREE.Mesh(geometry, sectionFillMaterial));
    }

    model.add(...objects);
    return objects;
  });
}

function applyTheme(theme) {
  const dark = theme === "dark";
  const colors = dark
    ? { cone: 0x5ba8f5, plane: 0x7eb893, section: 0xe6a19c }
    : { cone: 0x31475a, plane: 0x5a6b5c, section: 0xb85d3b };
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("conic-theme", theme);
  document.querySelector('meta[name="theme-color"]').content = dark ? "#0f171d" : "#dfe6e8";
  themeToggle.querySelector(".theme-name").textContent = dark ? "Light" : "Dark";
  themeToggle.setAttribute("aria-label", `Switch to ${dark ? "light" : "dark"} theme`);
  document.documentElement.style.setProperty("--stage-image", `url(\"${themeImages[theme]}\")`);
  coneMaterial.color.setHex(colors.cone);
  planeMaterial.color.setHex(colors.plane);
  [sectionMaterial, sectionGlowMaterial, sectionFillMaterial].forEach((material) => material.color.setHex(colors.section));
  syncUrl();
}

function updateResults(result) {
  const [symbol] = sectionMeta[result.type] || ["—"];
  $("#results-title").textContent = result.type;
  $("#result-symbol").textContent = symbol;
  $("#result-description").textContent = result.description;
  $("#eccentricity").textContent = Number.isFinite(result.eccentricity) ? result.eccentricity.toFixed(3) : "—";
  $("#plane-angle").textContent = `${result.plane_angle.toFixed(2)}°`;
  $("#point-count").textContent = new Intl.NumberFormat().format(result.point_count);
  $("#plane-equation").textContent = result.equation;
  $("#render-status").textContent = result.point_count ? "Live geometry" : "Outside visible cone";
}

function syncUrl(params = values()) {
  const query = new URLSearchParams({ ...params, theme: document.documentElement.dataset.theme });
  history.replaceState(null, "", `${location.pathname}?${query}`);
}

async function calculate(event) {
  event?.preventDefault();
  const params = values();
  const error = validate(params);
  $("#form-error").textContent = error;
  if (error) {
    (fields.find((field) => !Number.isFinite(Number(field.value))) || fields[0]).focus();
    return;
  }

  const currentRequest = ++requestId;
  $("#render-status").textContent = "Calculating…";
  submitButton.disabled = true;
  submitButton.textContent = "Calculating…";
  try {
    const response = await fetch("/api/conic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "The section could not be calculated.");
    if (currentRequest !== requestId) return;
    updatePlane(params);
    updateCurves(result.curves);
    updateResults(result);
    syncUrl(params);
  } catch (error) {
    $("#form-error").textContent = `${error.message} Check the Python API and try again.`;
    $("#render-status").textContent = "Calculation unavailable";
  } finally {
    if (currentRequest === requestId) {
      submitButton.disabled = false;
      submitButton.textContent = "Update Section";
    }
  }
}

function loadUrlState() {
  const query = new URLSearchParams(location.search);
  fields.forEach((field) => {
    if (query.has(field.name) && Number.isFinite(Number(query.get(field.name)))) field.value = query.get(field.name);
  });
}

form.addEventListener("submit", calculate);
document.querySelectorAll("[data-preset]").forEach((button) => {
  button.addEventListener("click", () => {
    fields.forEach((field, index) => { field.value = presets[button.dataset.preset][index]; });
    calculate();
  });
});
themeToggle.addEventListener("click", () => applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark"));
document.querySelectorAll("[data-panel-toggle]").forEach((button) => {
  button.addEventListener("click", () => {
    const panel = button.dataset.panelToggle;
    document.body.dataset.panel = document.body.dataset.panel === panel ? "" : panel;
    document.querySelectorAll("[data-panel-toggle]").forEach((item) => item.setAttribute("aria-expanded", String(document.body.dataset.panel === item.dataset.panelToggle)));
  });
});

new ResizeObserver(([entry]) => {
  const { width, height } = entry.contentRect;
  renderer.setSize(width, height, false);
  camera.aspect = width / Math.max(height, 1);
  camera.fov = camera.aspect < 0.8 ? 58 : 38;
  camera.updateProjectionMatrix();
}).observe(stage);

function render() {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(render);
}

loadUrlState();
applyTheme(document.documentElement.dataset.theme);
calculate();
render();
