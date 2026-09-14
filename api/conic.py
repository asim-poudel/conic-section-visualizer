"""Vercel endpoint for cone-plane intersection geometry."""

import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer

HEIGHT = 5.0
K = 1.0
SAMPLES = 360
EPSILON = 1e-9


def _clean(value):
    return 0.0 if abs(value) < EPSILON else round(value, 5)


def _format_equation(a, b, c, d):
    terms = []
    for value, variable in ((a, "x"), (b, "y"), (c, "z")):
        if abs(value) < EPSILON:
            continue
        magnitude = abs(value)
        coefficient = "" if abs(magnitude - 1) < EPSILON else f"{magnitude:g}"
        term = f"{coefficient}{variable}"
        terms.append(("−" if value < 0 else "+", term))
    if abs(d) >= EPSILON:
        terms.append(("−" if d < 0 else "+", f"{abs(d):g}"))
    if not terms:
        return "0 = 0"
    sign, term = terms[0]
    equation = ("−" if sign == "−" else "") + term
    equation += "".join(f" {sign} {term}" for sign, term in terms[1:])
    return f"{equation} = 0"


def _sample_nappe(a, b, c, d, sign):
    sampled = []
    for index in range(SAMPLES):
        theta = 2 * math.pi * index / SAMPLES
        denominator = K * (a * math.cos(theta) + b * math.sin(theta)) + sign * c
        if abs(denominator) < EPSILON:
            sampled.append(None)
            continue
        radius_parameter = -d / denominator
        if -EPSILON <= radius_parameter <= HEIGHT + EPSILON:
            t = max(0.0, min(HEIGHT, radius_parameter))
            sampled.append([_clean(K * t * math.cos(theta)), _clean(K * t * math.sin(theta)), _clean(sign * t)])
        else:
            sampled.append(None)

    if all(point is not None for point in sampled):
        return [sampled + [sampled[0]]]

    segments, current = [], []
    for point in sampled:
        if point is None:
            if len(current) > 1:
                segments.append(current)
            current = []
        else:
            current.append(point)
    if len(current) > 1:
        if segments and sampled[0] is not None:
            segments[0] = current + segments[0]
        else:
            segments.append(current)
    return segments


def solve(payload):
    try:
        a, b, c, d = (float(payload[key]) for key in ("a", "b", "c", "d"))
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        raise ValueError("A, B, C, and D must be finite numbers.") from exc

    if not all(math.isfinite(value) and abs(value) <= 1000 for value in (a, b, c, d)):
        raise ValueError("Use finite coefficients between −1000 and 1000.")
    normal_length = math.sqrt(a * a + b * b + c * c)
    if normal_length < EPSILON:
        raise ValueError("A, B, and C cannot all be 0.")

    plane_angle = math.degrees(math.asin(min(1.0, abs(c) / normal_length)))
    cone_angle = math.degrees(math.atan(K))
    eccentricity = math.cos(math.radians(plane_angle)) / math.cos(math.radians(cone_angle))
    tolerance = 0.15

    if abs(d) < EPSILON:
        conic_type = "Degenerate"
        description = "The plane passes through the cone’s apex, producing a point or intersecting lines instead of a regular conic."
        eccentricity = None
    elif plane_angle > 90 - tolerance:
        conic_type = "Circle"
        description = "A plane perpendicular to the cone axis creates a closed curve with constant radius."
        eccentricity = 0.0
    elif plane_angle > cone_angle + tolerance:
        conic_type = "Ellipse"
        description = "The plane cuts one nappe at a steeper angle than the cone’s side, creating a closed oval."
    elif abs(plane_angle - cone_angle) <= tolerance:
        conic_type = "Parabola"
        description = "The plane is parallel to the cone’s side, creating one open curve with eccentricity 1."
        eccentricity = 1.0
    else:
        conic_type = "Hyperbola"
        description = "The plane cuts both nappes of the cone, creating 2 mirrored open branches."

    curves = _sample_nappe(a, b, c, d, 1) + _sample_nappe(a, b, c, d, -1)
    return {
        "type": conic_type,
        "description": description,
        "eccentricity": eccentricity,
        "plane_angle": plane_angle,
        "cone_angle": cone_angle,
        "equation": _format_equation(a, b, c, d),
        "curves": curves,
        "point_count": sum(len(curve) for curve in curves),
    }


class handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        self._send(200, {"status": "ok", "service": "conic geometry"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 4096:
                raise ValueError("Request is too large.")
            payload = json.loads(self.rfile.read(length) or b"{}")
            self._send(200, solve(payload))
        except (ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)})


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), handler).serve_forever()
