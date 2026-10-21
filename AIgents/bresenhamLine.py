"""Interactive Bresenham line and anti-aliasing demonstration."""

from collections.abc import Iterable

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import AxesImage
from matplotlib.text import Text
from matplotlib.widgets import Slider

def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> np.ndarray:
    """Return a binary canvas containing a Bresenham line."""
    if x1 <= x0:
        raise ValueError("x1 must be greater than x0")
    if y1 < y0:
        raise ValueError("y1 must not be less than y0")

    delta_x = x1 - x0
    delta_y = y1 - y0
    canvas = np.zeros((delta_x, delta_y + 1))

    y = y0
    decision = (delta_y << 1) - delta_x
    doubled_x = delta_x << 1
    doubled_y = delta_y << 1

    for x in range(x0, x1):
        canvas[x - x0, y - y0] = 1

        if decision > 0:
            y += 1
            decision -= doubled_x

        decision += doubled_y

    return canvas


def bresenham_aa_line(
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    aa: Iterable[float],
) -> np.ndarray:
    """Return a canvas containing an anti-aliased Bresenham line."""
    aa = np.asarray(tuple(aa), dtype=float)

    if aa.size == 0:
        raise ValueError("aa must contain at least one value")

    if x1 <= x0:
        raise ValueError("x1 must be greater than x0")
    if y1 < y0:
        raise ValueError("y1 must not be less than y0")

    delta_x = x1 - x0
    delta_y = y1 - y0
    canvas = np.zeros((delta_x, delta_y + 1))

    def clamp_y(y: int) -> int:
        return int(np.clip(y, y0, y1))

    decision = (delta_y << 1) - delta_x
    y = y0
    length = len(aa)
    correction = 1 - (length % 2)
    half_length = length >> 1

    for x in range(x0, x1):
        if decision > 0:
            positions = range(
                y - half_length + correction,
                y - half_length + correction + length,
            )

            for position, weight in zip(positions, aa):
                canvas[x - x0, clamp_y(position) - y0] = weight

            y += 1
            decision -= delta_x << 1
        else:
            positions = range(
                y - half_length,
                y - half_length + length,
            )

            for position, weight in zip(positions, aa[::-1]):
                canvas[x - x0, clamp_y(position) - y0] = weight

        decision += delta_y << 1

    return canvas


def triangular_filter(length: int) -> tuple[float, ...]:
    """Create a symmetric triangular anti-aliasing filter."""
    if length < 1:
        raise ValueError("The filter length must be positive")

    center = (length - 1) / 2
    weights = [
        1.0 - abs(index - center) / (center + 1)
        for index in range(length)
    ]

    maximum = max(weights)
    return tuple(weight / maximum for weight in weights)


def render(
    x1: int,
    y1: int,
    filter_length: int,
    images: tuple[AxesImage, AxesImage, AxesImage],
    title: Text,
) -> None:
    """Recalculate and display all line variants."""
    x1 = max(2, int(x1))
    y1 = min(max(0, int(y1)), x1 - 1)
    filter_length = max(1, int(filter_length))

    ordinary = bresenham_line(0, 0, x1, y1)
    anti_aliased = bresenham_aa_line(
        0,
        0,
        x1,
        y1,
        triangular_filter(filter_length),
    )
    combined = np.maximum(ordinary, anti_aliased)

    for image, data in zip(images, (ordinary, anti_aliased, combined)):
        image.set_data(data.T)
        image.set_extent((-0.5, data.shape[0] - 0.5, -0.5, data.shape[1] - 0.5))
        image.set_clim(0, 1)

    title.set_text(
        f"Bresenham line: endpoint=({x1}, {y1}), "
        f"anti-aliasing width={filter_length}"
    )

    images[0].axes.relim()
    images[0].axes.autoscale_view()
    images[1].axes.relim()
    images[1].axes.autoscale_view()
    images[2].axes.relim()
    images[2].axes.autoscale_view()

    images[0].figure.canvas.draw_idle()


def main() -> None:
    initial_x = 353
    initial_y = 112
    initial_filter_length = 3

    figure, axes = plt.subplots(
        1,
        3,
        figsize=(14, 6),
        num="Interactive Bresenham Line",
    )

    figure.subplots_adjust(bottom=0.22, top=0.86, wspace=0.25)

    ordinary = bresenham_line(0, 0, initial_x, initial_y)
    anti_aliased = bresenham_aa_line(
        0,
        0,
        initial_x,
        initial_y,
        triangular_filter(initial_filter_length),
    )
    combined = np.maximum(ordinary, anti_aliased)

    images = (
        axes[0].imshow(ordinary.T, cmap="gray", vmin=0, vmax=1, origin="lower"),
        axes[1].imshow(anti_aliased.T, cmap="gray", vmin=0, vmax=1, origin="lower"),
        axes[2].imshow(combined.T, cmap="gray", vmin=0, vmax=1, origin="lower"),
    )

    axes[0].set_title("Bresenham")
    axes[1].set_title("Anti-aliased")
    axes[2].set_title("Combined")

    for axis in axes:
        axis.set_xlabel("X")
        axis.set_ylabel("Y")
        axis.grid(False)

    title = figure.suptitle("Interactive Bresenham Line")

    x_axis = figure.add_axes((0.15, 0.12, 0.70, 0.03))
    y_axis = figure.add_axes((0.15, 0.075, 0.70, 0.03))
    filter_axis = figure.add_axes((0.15, 0.03, 0.70, 0.03))

    x_slider = Slider(
        x_axis,
        "X endpoint",
        2,
        512,
        valinit=initial_x,
        valstep=1,
    )
    y_slider = Slider(
        y_axis,
        "Y endpoint",
        0,
        512,
        valinit=initial_y,
        valstep=1,
    )
    filter_slider = Slider(
        filter_axis,
        "AA width",
        1,
         nine := 9,
        valinit=initial_filter_length,
        valstep=2,
    )

    def update(_value: float) -> None:
        render(
            x_slider.val,
            y_slider.val,
            filter_slider.val,
            images,
            title,
        )

    x_slider.on_changed(update)
    y_slider.on_changed(update)
    filter_slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    main()