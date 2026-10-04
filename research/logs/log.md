# Tamarack Fire data inspection

**September 26, 2026 — Question:** How do detected active-fire pixels change across the Tamarack Fire’s daily files?

**Hypothesis (written before inspecting the map):** I predict that they will stay in the same area because the factors which affect fires are probably concentrated in similar areas.

**September 27, 2026 — Inspection**

Long-term goal: Predict one fire's spread day by day. This inspection is an early data audit, not a prediction experiment.

- Channel count: 23
- Channel names: ('M11', 'I2', 'I1', 'NDVI_last', 'EVI2_last', 'total precipitation', 'wind speed', 'wind direction', 'minimum temperature', 'maximum temperature', 'energy release component', 'specific humidity', 'slope', 'aspect', 'elevation', 'pdsi', 'LC_Type1', 'total_precipitation_surface_last', 'forecast wind speed', 'forecast wind direction', 'forecast temperature', 'forecast specific humidity', 'active fire')
- Height and width: 305, 243 pixels
- [First-detection map](../../artifacts/figures/tamarack_first_detection.png)

**Observation:** The map shows the first day each pixel was detected as active fire across the daily files. Most detected pixels form a main cluster, with a small detached patch. The map does not show how long any pixel burned or the complete burned area.

**Hypothesis check:** The main cluster is broadly consistent with my expectation that detections would remain in the same general area, but the detached patch complicates it. My hypothesis is partly supported, not conclusively confirmed or disproved. I need to inspect the daily images before interpreting the detached patch.

**Interpretation caution:** First detected active fire is not the same as first burned. A day with zero detections does not mean the fire went out.

**Initial audit list:**

- Smoke or clouds could hide active-fire detections.
- Satellite observation gaps could produce days with few or no detections.
- Each pixel covers approximately 375 m by 375 m, limiting spatial detail.
- Firefighting can change the actual spread pattern, so observed outcomes are not governed by weather and terrain alone.
- Putting observations from the same fire in both training and test sets could make evaluation misleading.
