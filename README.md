# LU2IN013 - Artificial Life

Course materials and simple templates for the LU2IN013 practicals (agent-based models, cellular automata, and small simulations).

## Contents
- `TME01` — traffic jam and forest fire templates
- `TME02` — predator–prey template
- `plotCSV` — small utilities to plot any CSV data

## Requirements
- **Python ≤ 3.11** — this project is intended for Python 3.11 and earlier (tested with Python 3.11)
- Install Python packages listed in `requirements.txt` (see below)

## Setup (quick)
- Install dependencies:

   ```bash
   py -3.11 -m pip install -r requirements.txt
   ```

## Quick start - How to execute files
- Run any simulation:

  ```bash
  py -3.11 folder/example.py
  ```

- Run the forest fire template:

  ```bash
  py -3.11 TME01/forestfire_template.py
  ```

- Run the plots:

  ```bash
  py -3.11 plotCSV/plot.py folder/example.csv 0 1 -title "Title" -xLabel "XLabel" -yLabel "YLabel"
  ```

- Visualize the trees plot:

  ```bash
  py -3.11 plotCSV/plot.py TME01/trees.csv 0 1 -title "Title" -xLabel "Iterations" -yLabel "Trees Fractions"
  ```