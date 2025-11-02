# 🚗 Project Lab Sumo – 2025
---

## 🗂 Project Structure

```text
Project_lab/
├─ ramp/       Your ramp network files (.sumocfg, .net.xml, etc.)
├─ Output/     Generated XML output files from SUMO
├─ Analysis/   Python scripts to convert XML output to CSV
  └─important_outputs/  Tthe CSV files extracted via the python scripts
└─ README.md   This documentation file
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

---
