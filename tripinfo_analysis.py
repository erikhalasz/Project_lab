import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('output/tripinfo.xml')
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
print(df.describe())
df.to_csv('tripinfo_summary.csv', index=False)
