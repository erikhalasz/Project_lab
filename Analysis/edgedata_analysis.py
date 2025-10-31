import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('./Output/edgeData.xml')
root = tree.getroot()

records = []
for interval in root.findall('interval'):
    start = float(interval.get('begin'))
    end = float(interval.get('end'))
    for edge in interval.findall('edge'):
        records.append({
            'begin': start,
            'end': end,
            'edge': edge.get('id'),
            'speed': float(edge.get('speed')),
            'density': float(edge.get('density')),
            'entered': int(edge.get('entered')),
            'left': int(edge.get('left'))
        })

edges_df = pd.DataFrame(records)
edges_df.to_csv('./Analysis/important_outputs/edge_density.csv', index=False)
