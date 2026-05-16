# Walking Surface Pressure Analysis

Biomechanical data analysis comparing plantar pressure patterns across two walking surfaces — **grass** and **concrete** — using StappOne pressure insole sensor data.

Completed as a research assistant trial task for the WalkSensePlace project at the CAMD Experience Design Lab, Northeastern University.

---

## Overview

This project analyzes how walking surface type affects plantar pressure distribution. Using CSV data recorded from StappOne pressure insoles, the analysis extracts step patterns, sensor-level pressure differences, and visualizes the results across both surfaces.

---

## Repository Structure

```
walksenseplace-analysis/
├── data/
│   ├── grass.csv           # Pressure insole recordings on grass
│   └── concrete.csv        # Pressure insole recordings on concrete
├── figures/
│   ├── grass_pressure.png
│   ├── concrete_pressure.png
│   ├── grass_steps_detected.png
│   └── sensor_comparison.png
├── analysis.py             # Main analysis script
└── Walking Surface Analysis_Flora Wang.pdf  # Full written report
```

---

## Methods

- **Data source**: StappOne pressure insole CSV exports
- **Language**: Python
- **Libraries**: Pandas, Matplotlib, NumPy
- **Analysis**: Step detection, per-sensor pressure aggregation, surface comparison visualization

---

## Key Findings

See the full written report: [`Walking Surface Analysis_Flora Wang.pdf`](./Walking%20Surface%20Analysis_Flora%20Wang.pdf)

---

## Author

**Flora Wang (Silu Wang)**  
BS Computer Science & Design, Northeastern University  
[GitHub](https://github.com/florawang26) · [Portfolio](https://wangsilub738.myportfolio.com)
