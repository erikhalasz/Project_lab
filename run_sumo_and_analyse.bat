@echo off
echo =====================================
echo Running SUMO Simulation...
echo =====================================

sumo -c "ramp\ramp.sumocfg" ^
  --summary-output "Output\summary.xml" ^
  --tripinfo-output "Output\tripinfo.xml" ^
  --edgedata-output "Output\edgeData.xml"

echo Simulation complete!
echo Running analysis scripts...

python .\Analysis\edgedata_analysis.py
python .\Analysis\summary_analysis.py
python .\Analysis\tripinfo_analysis.py
python .\Analysis\extract_info.py

echo =====================================
echo All done! Check Analysis\analysis_results for CSV outputs.
echo =====================================
