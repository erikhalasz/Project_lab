# Project_lab
2025 Project lab sumo

To Run this you need to navigate to the C:\...\Project_lab directory and run in the terminal something like this:

Replace the % in the command below with the full path to your ramp directory (for example: C:\Users\Somebody\Documents\Project\ramp).

Example command:
sumo -c "C:\Users\Somebody\Documents\Project\ramp\ramp.sumocfg" --summary-output "Output\summary.xml" --tripinfo-output "Output\tripinfo.xml" --edgedata-output "Output\edgeData.xml"

sumo -c "%\ramp.sumocfg" --summary-output "Output\summary.xml" --tripinfo-output "Output\tripinfo.xml" --edgedata-output "Output\edgeData.xml"

You can find in the Analysis folder three python files that generate the different csv files that contain the data extracted from the simulation.