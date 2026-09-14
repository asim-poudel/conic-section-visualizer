import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import "./styles.css";

const $ = (selector) => document.querySelector(selector);
const form = $("#plane-form");
const fields = ["a", "b", "c", "d"].map((name) => form.elements[name]);
const stage = $("#scene");
const horizontal = $("#horizontal-angle");
const vertical = $("#vertical-angle");
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
controls.minDistance = 7;
controls.maxDistance = 22;
controls.target.set(0, 0, 0);

scene.add(new THREE.HemisphereLight(0xeef7ff, 0x28364e, 2.6));
const keyLight = new THREE.DirectionalLight(0xffffff, 3.2);
keyLight.position.set(5, -4, 8);
scene.add(keyLight);

const model = new THREE.Group();
scene.add(model);
const coneMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xb8d9dc,
  transparent: true,
  opacity: 0.38,
  roughness: 0.35,
  metalness: 0.05,
  side: THREE.DoubleSide,
  depthWrite: false,
});
const planeMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xf2b85b,
  transparent: true,
  opacity: 0.5,
  roughness: 0.42,
  side: THREE.DoubleSide,
  depthWrite: false,
});
const sectionMaterial = new THREE.MeshStandardMaterial({ color: 0xff6c58, emissive: 0x9d1e20, emissiveIntensity: 0.75 });

const upperCone = new THREE.Mesh(new THREE.ConeGeometry(5, 5, 72, 1, true), coneMaterial);
upperCone.rotation.x = -Math.PI / 2;
upperCone.position.z = 2.5;
const lowerCone = new THREE.Mesh(new THREE.ConeGeometry(5, 5, 72, 1, true), coneMaterial);
lowerCone.rotation.x = Math.PI / 2;
lowerCone.position.z = -2.5;
model.add(upperCone, lowerCone);

const grid = new THREE.GridHelper(12, 12, 0x718b9a, 0x526a78);
grid.rotation.x = Math.PI / 2;
grid.material.transparent = true;
grid.material.opacity = 0.18;
model.add(grid, new THREE.AxesHelper(3.25));

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
  planeMesh = new THREE.Mesh(new THREE.PlaneGeometry(12, 12), planeMaterial);
  planeMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), normal);
  planeMesh.position.copy(normal).multiplyScalar(-d / Math.hypot(a, b, c));
  model.add(planeMesh);
}

function updateCurves(branches) {
  curves.forEach((curve) => {
    model.remove(curve);
    curve.geometry.dispose();
  });
  curves = branches.filter((points) => points.length > 1).map((points) => {
    const vectors = points.map(([x, y, z]) => new THREE.Vector3(x, y, z));
    const closed = vectors.length > 3 && vectors[0].distanceTo(vectors.at(-1)) < 0.08;
    const path = new THREE.CatmullRomCurve3(vectors, closed, "centripetal");
    const mesh = new THREE.Mesh(new THREE.TubeGeometry(path, Math.max(24, vectors.length), 0.045, 6, closed), sectionMaterial);
    model.add(mesh);
    return mesh;
  });
}

function updateResults(result) {
  const [symbol, reading] = sectionMeta[result.type] || ["—", result.description];
  $("#results-title").textContent = result.type;
  $("#result-symbol").textContent = symbol;
  $("#result-description").textContent = result.description;
  $("#result-reading").textContent = reading;
  $("#eccentricity").textContent = Number.isFinite(result.eccentricity) ? result.eccentricity.toFixed(3) : "—";
  $("#plane-angle").textContent = `${result.plane_angle.toFixed(2)}°`;
  $("#point-count").textContent = new Intl.NumberFormat().format(result.point_count);
  $("#plane-equation").textContent = result.equation;
  $("#render-status").textContent = result.point_count ? "Live geometry" : "Outside visible cone";
}

function syncUrl(params = values()) {
  const query = new URLSearchParams({ ...params, h: horizontal.value, v: vertical.value });
  history.replaceState(null, "", `${location.pathname}?${query}`);
}

async function calculate(event) {
  event?.preventDefault();
  const params = values();
  const error = validate(params);
  $("#form-error").textContent = error;
  if (error) return;

  const currentRequest = ++requestId;
  $("#render-status").textContent = "Calculating…";
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
  }
}

function setCameraFromSliders() {
  const azimuth = THREE.MathUtils.degToRad(Number(horizontal.value));
  const elevation = THREE.MathUtils.degToRad(Number(vertical.value));
  const radius = camera.position.length() || 12;
  camera.position.set(
    radius * Math.cos(elevation) * Math.cos(azimuth),
    radius * Math.cos(elevation) * Math.sin(azimuth),
    radius * Math.sin(elevation),
  );
  camera.lookAt(controls.target);
  $("#horizontal-value").textContent = `${horizontal.value}°`.replace("-", "−");
  $("#vertical-value").textContent = `${vertical.value}°`;
  syncUrl();
}

function loadUrlState() {
  const query = new URLSearchParams(location.search);
  fields.forEach((field) => {
    if (query.has(field.name) && Number.isFinite(Number(query.get(field.name)))) field.value = query.get(field.name);
  });
  if (query.has("h")) horizontal.value = query.get("h");
  if (query.has("v")) vertical.value = query.get("v");
}

form.addEventListener("submit", calculate);
document.querySelectorAll("[data-preset]").forEach((button) => {
  button.addEventListener("click", () => {
    fields.forEach((field, index) => { field.value = presets[button.dataset.preset][index]; });
    calculate();
  });
});
[horizontal, vertical].forEach((input) => input.addEventListener("input", setCameraFromSliders));

new ResizeObserver(([entry]) => {
  const { width, height } = entry.contentRect;
  renderer.setSize(width, height, false);
  camera.aspect = width / Math.max(height, 1);
  camera.updateProjectionMatrix();
}).observe(stage);

function render() {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(render);
}

loadUrlState();
setCameraFromSliders();
calculate();
render();
