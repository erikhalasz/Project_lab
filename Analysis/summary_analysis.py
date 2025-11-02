import xml.etree.ElementTree as ET
import pandas as pd

# Parse the summary XML
tree = ET.parse('./Output/summary.xml')
root = tree.getroot()

# Collect data from each step
rows = []
for step in root.findall('step'):
    rows.append({key: float(step.get(key)) for key in step.keys()})

# Convert to DataFrame
df = pd.DataFrame(rows)

# Save to CSV for analysis
df.to_csv('./Analysis/analysis_results/summary_steps.csv', index=False)

