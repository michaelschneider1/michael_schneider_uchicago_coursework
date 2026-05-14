import pytest

from image import Image, Loc, Color
from graph import ImageGraph


### TASK 1 TESTS ###


@pytest.mark.parametrize(
    "filename, width, height, pixels",
    [
        (
            "assets/example.ppm",
            2,
            4,
            [
                ((0, 0), (255, 0, 0)),
                ((0, 1), (255, 0, 0)),
                ((1, 0), (255, 255, 0)),
                ((1, 1), (255, 255, 0)),
                ((2, 0), (0, 255, 0)),
                ((2, 1), (0, 255, 0)),
                ((3, 0), (0, 0, 255)),
                ((3, 1), (0, 0, 255)),
            ],
        ),
        (
            "assets/grid.ppm",
            320,
            192,
            [
                ((0, 0), (0, 0, 255)),
                ((0, 319), (0, 0, 255)),
                ((191, 0), (0, 0, 255)),
                ((191, 319), (0, 0, 255)),
                ((13, 7), (0, 0, 255)),
                ((23, 64), (255, 255, 0)),
                ((64, 128), (255, 255, 0)),
                ((135, 130), (0, 0, 255)),
            ],
        ),
        (
            "assets/shapes.ppm",
            800,
            300,
            [
                ((20, 10), (255, 255, 0)),
                ((150, 100), (255, 0, 0)),
                ((55, 60), (128, 128, 128)),
                ((230, 375), (0, 255, 0)),
                ((60, 330), (128, 128, 128)),
                ((84, 720), (0, 0, 255)),
            ],
        ),
    ],
)
def test_task1_image_load(
    filename: str, width: int, height: int, pixels: list[tuple[Loc, Color]]
) -> None:
    img = Image(filename)

    assert img.width == width, "incorrect image width"
    assert img.height == height, "incorrect image height"

    for loc, color in pixels:
        r, c = loc
        error_msg = f"incorrect image pixel at (row,col) = ({r},{c})"
        assert img.pixels[r][c] == color, error_msg


### TASK 3 TESTS ###


@pytest.mark.parametrize(
    "name, start, expected",
    [
        ("example", (0, 0), ((255, 0, 0), 2)),
        ("example", (0, 1), ((255, 255, 0), 2)),
        ("example", (0, 2), ((0, 255, 0), 2)),
        ("example", (0, 3), ((0, 0, 255), 2)),
        ("grid", (155, 98), ((255, 255, 0), 4096)),
        ("grid", (227, 28), ((255, 255, 0), 4096)),
        ("grid", (281, 160), ((0, 0, 255), 4096)),
        ("shapes", (167, 151), ((255, 0, 0), 31415)),
        ("shapes", (432, 211), ((0, 255, 0), 20000)),
        ("shapes", (686, 106), ((0, 0, 255), 40000)),
        ("shapes", (525, 219), ((255, 255, 0), 120000)),
        ("shapes", (65, 230), ((128, 128, 128), 2146)),
    ],
)
def test_task3_compute_region_color_and_num_pixels(
    name: str, start: Loc, expected: tuple[Color, int]
) -> None:
    img_graph = ImageGraph(Image(f"assets/{name}.ppm"))
    region = img_graph.compute_region(start)
    actual = (region["color"], len(region["pixels"]))
    assert actual == expected


@pytest.mark.parametrize(
    "name, start",
    [
        ("grid", (155, 98)),
        ("grid", (156, 31)),
        ("grid", (163, 162)),
        ("grid", (214, 100)),
        ("grid", (214, 151)),
        ("grid", (227, 28)),
        ("grid", (28, 106)),
        ("grid", (280, 37)),
        ("grid", (281, 160)),
        ("grid", (298, 85)),
        ("grid", (32, 160)),
        ("grid", (42, 42)),
        ("grid", (83, 24)),
        ("grid", (87, 100)),
        ("grid", (92, 159)),
        ("shapes", (167, 151)),
        ("shapes", (232, 229)),
        ("shapes", (234, 68)),
        ("shapes", (320, 160)),
        ("shapes", (432, 211)),
        ("shapes", (461, 88)),
        ("shapes", (525, 219)),
        ("shapes", (64, 69)),
        ("shapes", (65, 230)),
        ("shapes", (686, 106)),
    ],
)
def test_task3_compute_region_outline(name: str, start: Loc) -> None:
    with open(f"tests/{name}-{start[0]}-{start[1]}.txt") as f:
        lines = f.readlines()
    lines2 = [line.strip().split(",") for line in lines]
    expected = set([(int(line[0]), int(line[1])) for line in lines2])

    img = Image(f"assets/{name}.ppm")
    img_graph = ImageGraph(img)

    actual = img_graph.compute_region(start)["outline"]
    assert actual == expected, "outline is incorrect"
