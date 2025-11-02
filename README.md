# 🚗 Project Lab Sumo – 2025
---

## 🗂 Project Structure

```text
Project_lab/
├─ ramp/
├─ Output/
├─ Analysis/
│  ├─ analysis_results/
│  ├─ edgedata_analysis.py
│  ├─ summary_analysis.py
│  └─ tripinfo_analysis.py
├─ run_sumo_and_analyse.bat
└─ README.md

```
---

## 🚀 How to Run the Simulation

### 1. Navigate to the Project Directory
Open your terminal and go to the project folder:

```bash
cd C:\...\Project_lab
```
### 2. Run SUMO

```bash

sumo -c "ramp\ramp.sumocfg" --summary-output "Output\summary.xml" --tripinfo-output "Output\tripinfo.xml" --edgedata-output "Output\edgeData.xml"
```

📂 Output Files
After running the simulation, the Output folder will contain:

summary.xml – overall simulation summary

tripinfo.xml – trip-by-trip information

edgeData.xml – detailed edge/road data

📊 Analyze the Results
Inside the Analysis folder, you’ll find three Python scripts that:

Extract data from XML files

Convert the data into CSV format

Allow for easier processing and visualization

You can run these scripts, using the following command:
```bash
python .\Analysis\edgedata_analysis.py
python .\Analysis\summary_analysis.py
python .\Analysis\tripinfo_analysis.py
```

You can find the generated CSV files in `Analysis/analysis_results`: `edge_density.csv`, `summary_steps.csv`, and `tripinfo_summary.csv`.


---
### 3.⚡ Alternatively, You Can Run Everything in One Command

You can run the simulation and process all XML files into CSVs in one go:

```bash
.\run_sumo_and_analyse.bat

```

