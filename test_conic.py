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
    assert solve({"a": 0, "b": 1.7, "c": 1, "d": -1})["eccentricity"] > 1


if __name__ == "__main__":
    test_known_sections()
    print("4 known sections passed")
