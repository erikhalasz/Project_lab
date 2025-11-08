import argparse
import csv
import os
import xml.etree.ElementTree as ET
from statistics import mean


def extract_speeds_from_edg(edg_path):
    """Return mean highway speed and mean ramp speed from an .edg file."""
    if not os.path.exists(edg_path):
        return None, None
    tree = ET.parse(edg_path)
    root = tree.getroot()

    highway_speeds, ramp_speeds = [], []
    for edge in root.findall('.//edge'):
        sid = edge.get('id', '')
        speed = edge.get('speed')
        priority = edge.get('priority')
        try:
            sp = float(speed) if speed is not None else None
        except ValueError:
            sp = None

        if (('main' in sid) or (priority and int(priority) >= 3)) and sp is not None:
            highway_speeds.append(sp)
        elif (('ramp' in sid) or (priority and int(priority) <= 1)) and sp is not None:
            ramp_speeds.append(sp)

    h = mean(highway_speeds) if highway_speeds else None
    r = mean(ramp_speeds) if ramp_speeds else None
    return h, r


def extract_vehsperhour_from_rou(rou_path):
    """Return vehsPerHour per flow type (main, ramp, total)."""
    if not os.path.exists(rou_path):
        return {}
    tree = ET.parse(rou_path)
    root = tree.getroot()

    results = {'main': 0.0, 'ramp': 0.0, 'total': 0.0}
    for flow in root.findall('.//flow'):
        fid = flow.get('id', '')
        vph = flow.get('vehsPerHour') or flow.get('vehsperhour')
        try:
            vphf = float(vph) if vph is not None else 0.0
        except ValueError:
            vphf = 0.0

        if 'main' in fid.lower():
            results['main'] += vphf
        if 'ramp' in fid.lower():
            results['ramp'] += vphf
        results['total'] += vphf
    return results


def extract_mean_speed_from_summary(summary_path):
    """Compute the average meanSpeed from SUMO summary.xml."""
    if not os.path.exists(summary_path):
        return None
    tree = ET.parse(summary_path)
    root = tree.getroot()

    speeds = []
    for step in root.findall('.//step'):
        ms = step.get('meanSpeed')
        if ms is None:
            continue
        try:
            speeds.append(float(ms))
        except ValueError:
            continue

    return mean(speeds) if speeds else None


def write_row(out_path, row):
    """Write or append a row to a CSV, updating headers if needed."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    file_exists = os.path.exists(out_path)

    if not file_exists:
        header = list(row.keys())
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerow(row)
        return

    with open(out_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_fieldnames = reader.fieldnames or []
        existing_rows = list(reader)

    new_fields = [k for k in row.keys() if k not in existing_fieldnames]
    merged_fields = existing_fieldnames + new_fields

    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=merged_fields)
        writer.writeheader()
        for r in existing_rows:
            writer.writerow({k: r.get(k, '') for k in merged_fields})
        writer.writerow({k: row.get(k, '') for k in merged_fields})


def main():
    parser = argparse.ArgumentParser(description='Extract configuration + mean speed summary per simulation.')
    parser.add_argument('--edg', default='../ramp/ramp.edg.xml', help='Path to .edg file')
    parser.add_argument('--rou', default='../ramp/ramp.rou.xml', help='Path to .rou file')
    parser.add_argument('--summary', default='../Output/summary.xml', help='Path to summary.xml file')
    parser.add_argument('--out', default='../sim_summary_min.csv', help='Output CSV')
    parser.add_argument('--sim-id', default=None, help='Simulation identifier')
    args = parser.parse_args()

    sim_id = args.sim_id or os.path.splitext(os.path.basename(args.edg))[0]
    base_dir = os.path.dirname(__file__)

    edg_path = os.path.normpath(os.path.join(base_dir, args.edg))
    rou_path = os.path.normpath(os.path.join(base_dir, args.rou))
    summary_path = os.path.normpath(os.path.join(base_dir, args.summary))
    out_path = os.path.normpath(os.path.join(base_dir, args.out))

    highway_speed, ramp_speed = extract_speeds_from_edg(edg_path)
    vph = extract_vehsperhour_from_rou(rou_path)
    mean_speed = extract_mean_speed_from_summary(summary_path)

    row = {
        'sim_id': sim_id,
        'highway_speed': highway_speed,
        'ramp_speed': ramp_speed,
        'vehsPerHour_main': vph.get('main', 0.0),
        'vehsPerHour_ramp': vph.get('ramp', 0.0),
        'vehsPerHour_total': vph.get('total', 0.0),
        'meanSpeed_avg': mean_speed,
    }

    write_row(out_path, row)
    print(f'✅ Wrote simulation summary for {sim_id} to {out_path}')


if __name__ == '__main__':
    main()
