import rasterio
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

PATH = Path("/Users/maheswardileep/firehorizonREAL/data/WildfireSpreadTS/2021/fire_25294746")
files = sorted(PATH.glob("*.tif"))
print("Number of files: ", len(files))
if not files:
    raise FileNotFoundError(f"No GeoTIFF files found in {PATH}")
print("First: ", files[0].name)
print("Last: ", files[-1].name)


with rasterio.open(files[0]) as image:
    print("Channels:", image.count)
    print("Height and width:", image.height, image.width)
    print("Channel names:", image.descriptions)
    band = image.read(23)
    finite = np.isfinite(band)
    print("Finite Pixels: ", finite.sum())

    if finite.any():
        values = band[finite]
        print("minimum: ", values.min())
        print("Maximum: ", values.max())

    reference_grid = (image.height, image.width, image.crs, image.transform)

# -1 means this pixel was never detected as active fire in these daily files.
# Day 0 is the first file's date; day 1 is the next date, and so on.
first_detection = np.full((reference_grid[0], reference_grid[1]), -1, dtype=int)
daily_counts = []

for day_index, file in enumerate(files):
    with rasterio.open(file) as image:
        grid = (image.height, image.width, image.crs, image.transform)
        if grid != reference_grid:
            raise ValueError(f"Grid mismatch in {file.name}")

        fire_band = image.read(23)
        detected = np.isfinite(fire_band) & (fire_band > 0)
        daily_count = int(detected.sum())
        daily_counts.append(daily_count)
        print(file.name, daily_count)

        newly_detected = detected & (first_detection == -1)
        first_detection[newly_detected] = day_index

assert int((first_detection == 0).sum()) == daily_counts[0]
assert first_detection.min() >= -1
assert first_detection.max() < len(files)
print("Pixels detected at least once:", int((first_detection >= 0).sum()))
print("Never-detected pixels:", int((first_detection == -1).sum()))
print("First-detection day indices:", np.unique(first_detection))

plot_map = np.ma.masked_equal(first_detection, -1)
plt.imshow(plot_map, cmap='viridis', vmax=len(files)-1, vmin=0)
colorbar = plt.colorbar()
colorbar.set_label("Days since july 8, 2021")
plt.title("Tamarack Fire: first detected active fire")
plt.show()
plt.savefig(
    "artifacts/figures/tamarack_first_detection.png",
    dpi=200,
    bbox_inches="tight"
)
