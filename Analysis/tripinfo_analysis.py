import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('./Output/tripinfo.xml')
root = tree.getroot()

rows = []
for trip in root.findall('tripinfo'):
    rows.append({
        'id': trip.get('id'),
        'depart': float(trip.get('depart')),
        'arrival': float(trip.get('arrival')),
        'duration': float(trip.get('duration')),
        'routeLength': float(trip.get('routeLength')),
        'waitingTime': float(trip.get('waitingTime'))
    })

df = pd.DataFrame(rows)
df.to_csv('./Analysis/important_outputs/tripinfo_summary.csv', index=False)
