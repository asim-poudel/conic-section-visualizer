import math

from api.conic import solve


def test_known_sections():
    cases = {
        "Circle": (0, 0, 1, -2),
        "Ellipse": (0, 0.45, 1, -2),
        "Parabola": (0, 1, 1, -2),
        "Hyperbola": (0, 1.7, 1, -1),
    }
    for expected, values in cases.items():
        result = solve(dict(zip("abcd", values)))
        assert result["type"] == expected, (expected, result["type"])
        assert result["point_count"] > 0


def test_cone_dimensions():
    result = solve({"a": 0, "b": 0, "c": 1, "d": -6, "height": 7, "slope": 0.5})
    assert result["height"] == 7
    assert result["slope"] == 0.5
    assert math.isclose(result["cone_angle"], math.degrees(math.atan(0.5)))
    assert result["point_count"] > 0
    assert max(abs(point[2]) for curve in result["curves"] for point in curve) <= 7
    assert solve({"a": 0, "b": 0, "c": 1, "d": -6, "height": 5})["point_count"] == 0


def test_slope_changes_classification():
    plane = {"a": 0, "b": 1, "c": 1, "d": -2}
    assert solve({**plane, "slope": 0.5})["type"] == "Ellipse"
    assert solve({**plane, "slope": 1})["type"] == "Parabola"
    assert solve({**plane, "slope": 2})["type"] == "Hyperbola"


def test_invalid_dimensions():
    for key, value in (("height", 0), ("height", 21), ("slope", 0), ("slope", 4)):
        try:
            solve({"a": 0, "b": 0, "c": 1, "d": -2, key: value})
        except ValueError:
            continue
        raise AssertionError(f"{key}={value} should be rejected")


if __name__ == "__main__":
    test_known_sections()
    test_cone_dimensions()
    test_slope_changes_classification()
    test_invalid_dimensions()
    print("Conic API tests passed")
