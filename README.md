# 🚗 Project Lab Sumo – 2025
---

## 🗂 Project Structure

Project_lab/
├─ ramp/ # Your ramp network files (.sumocfg etc.)
├─ Output/ # Generated XML output files
├─ Analysis/ # Python scripts to convert XML to CSV
└─ README.md # This file

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
Template:


sumo -c "ramp\ramp.sumocfg" --summary-output "Output\summary.xml" --tripinfo-output "Output\tripinfo.xml" --edgedata-output "Output\edgeData.xml"
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
