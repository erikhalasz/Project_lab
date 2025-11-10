# 🚗 Project Lab Sumo – 2025
---

## 🗂 Project Structure

```text
Project_lab/
├─ ramp/
├─ Output/
├─ Analysis/
│  ├─ analysis_results/
├─ generation/
├─ test/
├─ run_multiple_simulations.py
├─ kutatasi_terv.pdf
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
---

### To extract data from all simulations for neural network:

After creating the necessary parameter space for the simulations in the ```run_multiple_simulations.py``` file write this in the terminal

```bash
python .\run_multiple_simulations.py
```

After that, you can find the data extracted in the ```sim_summary_min.csv``` file in the ```NN``` folder.

---

## If you do NOT want to create multiple simulations:

### 2. Run SUMO

```text
Note: this will run with the current setup in the ramp folder.
``` 

```bash
sumo -c "ramp\ramp.sumocfg" --summary-output "Output\summary.xml" --tripinfo-output "Output\tripinfo.xml" --edgedata-output "Output\edgeData.xml"
```

#### SUMO in GUI

If you want to run the simulation in GUI, run the following command:

```bash
sumo-gui -c ramp/ramp.sumocfg
```

#### 📂 Output Files
After running the simulation, the Output folder will contain:

`summary.xml` – overall simulation summary

`tripinfo.xml` – trip-by-trip information

`edgeData.xml` – detailed edge/road data

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
### ⚡ Alternatively, You Can Run Everything in One Command

You can run the simulation and process all XML files into CSVs in one go:

```bash
.\run_sumo_and_analyse.bat

```


## 🧭 Git Quickstart Tutorial (For First-Time Users)
If you’ve never used Git before, follow these steps to get started.


### 🪶 1. Navigate to Your Working Directory

Open your terminal (or command prompt) and move to your desired working directory:
```bash 
cd C:\...\Documents
```

### 🌱 2. Clone the Repository

Clone the project from GitHub by running:
```bash
https://github.com/erikhalasz/Project_lab.git
```

### 🌿 3. Create Your Own Branch

After cloning, you’ll be on the main branch by default.
To create your own development branch (so your work stays separate), run:
```bash
git checkout -b [your_name]_dev
```

### ✏️ 4. Make Changes and Commit Them

Once you’ve made some changes in your branch, save them to Git with:
```bash
git add .
git commit -m "Describe your changes here"
```

### ☁️ 5. Push Your Changes to GitHub

Finally, upload your branch and commits to the remote repository:
```bash 
git push
``` 
> ### 📚 Learn More About Git  
> Want to dive deeper into **Git branching** and workflows?  
> Check out this excellent interactive tutorial:  
> 🔗 [**Learn Git Branching**](https://learngitbranching.js.org/)
