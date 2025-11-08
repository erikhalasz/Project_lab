import os
import subprocess
import shutil
from datetime import datetime
from generation.generate_xml import RouteXMLGenerator, EdgeXMLGenerator


def run_command(command):
    """Run a shell command. Return True on success, False on failure.

    Captures stderr for easier debugging on failures.
    """
    proc = subprocess.run(command, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Warning: Command '{command}' failed with error:\n{proc.stderr}")
        return False
    return True


def generate_new_routes(mainline_flow, rampline_flow, routes_file="ramp/ramp.rou.xml"):
    """Generate routes using RouteXMLGenerator with explicit flow rates."""
    generator = RouteXMLGenerator(
        mainline_vehs_per_hour=int(mainline_flow),
        rampline_vehs_per_hour=int(rampline_flow),
        output_file=routes_file,
    )
    generator.generate_xml()
    return routes_file


def generate_new_edges(highway_speed, ramp_speed, edges_file="ramp/ramp.edg.xml"):
    """Generate edges using EdgeXMLGenerator with explicit speeds."""
    edge_generator = EdgeXMLGenerator(
        highway_speed=float(highway_speed),
        ramp_speed=float(ramp_speed),
        output_file=edges_file,
    )
    edge_generator.generate_xml()
    return edges_file


def parse_list_or_range(s: str):
    """Parse a comma-separated list or a start:stop:step range into floats."""
    s = str(s)
    if ':' in s:
        parts = s.split(':')
        if len(parts) != 3:
            raise ValueError('Range form must be start:stop:step')
        start, stop, step = map(float, parts)
        values = []
        v = start
        if step == 0:
            raise ValueError('step must be non-zero')
        if step > 0:
            while v <= stop:
                values.append(round(v, 6))
                v += step
        else:
            while v >= stop:
                values.append(round(v, 6))
                v += step
        return values
    else:
        parts = [p.strip() for p in s.split(',') if p.strip()]
        return [float(p) for p in parts]


def count_valid_combinations(highway_speeds, ramp_speeds, mainline_flows, ramp_flows):
    """Count combinations where highway_speed > ramp_speed without building the full grid."""
    c = 0
    for hs in highway_speeds:
        for rs in ramp_speeds:
            if float(hs) <= float(rs):
                continue
            for mf in mainline_flows:
                for rf in ramp_flows:
                    c += 1
    return c


def build_filtered_generator(highway_speeds, ramp_speeds, mainline_flows, ramp_flows):
    """Yield parameter dicts where highway_speed > ramp_speed (streaming, memory-light)."""
    for hs in highway_speeds:
        for rs in ramp_speeds:
            if float(hs) <= float(rs):
                continue
            for mf in mainline_flows:
                for rf in ramp_flows:
                    yield {
                        'highway_speed': float(hs),
                        'ramp_speed': float(rs),
                        'mainline_flow': int(mf),
                        'rampline_flow': int(rf),
                    }


def frange(start, stop, step):
    """Float range generator (inclusive when step fits exactly)."""
    x = float(start)
    if step == 0:
        raise ValueError('step must be non-zero')
    if step > 0:
        while x <= stop:
            yield round(x, 6)
            x += step
    else:
        while x >= stop:
            yield round(x, 6)
            x += step


def create_iteration_folder(iteration):
    """Create a folder for this iteration's results"""
    folder = f"Analysis/analysis_results/iteration_{iteration}"
    os.makedirs(folder, exist_ok=True)
    return folder


def main():
    # Hard-coded parameter lists (no CLI parameters). Adjust these lists here.
    highway_speeds = list(frange(25.0, 129.5, 0.5))   # 25.0 .. 129.5 by 0.5
    ramp_speeds = list(frange(15.0, 99.5, 0.5))       # 15.0 .. 99.5 by 0.5
    mainline_flows = list(range(800, 5000, 50))      # 800 .. 4950 step 50
    ramp_flows = list(range(200, 2000, 25))          # 200 .. 1975 step 25

    # Use streaming generator to avoid building the full grid in memory
    total = count_valid_combinations(highway_speeds, ramp_speeds, mainline_flows, ramp_flows)
    if total == 0:
        print('No parameter combinations generated (check that highway_speed > ramp_speed for at least one pair).')
        return

    print(f"Starting multiple simulation runs... total iterations: {total}")

    gen = build_filtered_generator(highway_speeds, ramp_speeds, mainline_flows, ramp_flows)
    for i, params in enumerate(gen):
        print(f"\nIteration {i+1}/{total} -- {params}")
        print("=" * 50)

        # Create folder for this iteration's results
        results_folder = create_iteration_folder(i + 1)

        # Generate new edges and routes for this parameter set
        print("Generating new edges...")
        edges_file = generate_new_edges(params['highway_speed'], params['ramp_speed'])

        print("Generating new routes...")
        routes_file = generate_new_routes(params['mainline_flow'], params['rampline_flow'])
        if not routes_file:
            print(f"Failed to generate routes for iteration {i+1}")
            continue

        # Run SUMO simulation (headless)
        print("Running SUMO simulation...")
        sumo_cmd = 'sumo -c "ramp/ramp.sumocfg" ' + \
                  '--summary-output "Output/summary.xml" ' + \
                  '--tripinfo-output "Output/tripinfo.xml" ' + \
                  '--edgedata-output "Output/edgeData.xml"'
        if not run_command(sumo_cmd):
            print("SUMO simulation failed")
            continue

        # Run analysis scripts
        print("Running analysis...")
        analysis_scripts = [
            'Analysis/edgedata_analysis.py',
            'Analysis/summary_analysis.py',
            'Analysis/tripinfo_analysis.py',
            'Analysis/extract_info.py',
        ]

        for script in analysis_scripts:
            if not run_command(f'python {script}'):
                print(f"Analysis script {script} failed")

        # Move results to iteration folder
        result_files = [
            'Analysis/analysis_results/edge_density.csv',
            'Analysis/analysis_results/summary_steps.csv',
            'Analysis/analysis_results/tripinfo_summary.csv',
            'Analysis/analysis_results/mean_speed_with_config.csv',
        ]

        for file in result_files:
            if os.path.exists(file):
                new_name = os.path.join(results_folder, os.path.basename(file))
                shutil.move(file, new_name)

        print(f"Completed iteration {i+1}")

    print("\nAll iterations complete!")
    print("Results are saved in Analysis/analysis_results/iteration_X folders")


if __name__ == "__main__":
    main()
import os
import subprocess
import shutil
from datetime import datetime
from Project_lab.generation.generate_xml import RouteXMLGenerator, EdgeXMLGenerator


def run_command(command):
    """Run a shell command. Return True on success, False on failure.

    Captures stderr for easier debugging on failures.
    """
    proc = subprocess.run(command, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Warning: Command '{command}' failed with error:\n{proc.stderr}")
        return False
    return True


def generate_new_routes(mainline_flow, rampline_flow, routes_file="ramp/ramp.rou.xml"):
    """Generate routes using RouteXMLGenerator with explicit flow rates."""
    generator = RouteXMLGenerator(
        mainline_vehs_per_hour=int(mainline_flow),
        rampline_vehs_per_hour=int(rampline_flow),
        output_file=routes_file,
    )
    generator.generate_xml()
    return routes_file


def generate_new_edges(highway_speed, ramp_speed, edges_file="ramp/ramp.edg.xml"):
    """Generate edges using EdgeXMLGenerator with explicit speeds."""
    edge_generator = EdgeXMLGenerator(
        highway_speed=float(highway_speed),
        ramp_speed=float(ramp_speed),
        output_file=edges_file,
    )
    edge_generator.generate_xml()
    return edges_file


def parse_list_or_range(s: str):
    """Parse a comma-separated list or a start:stop:step range into floats."""
    s = str(s)
    if ':' in s:
        parts = s.split(':')
        if len(parts) != 3:
            raise ValueError('Range form must be start:stop:step')
        start, stop, step = map(float, parts)
        values = []
        v = start
        if step == 0:
            raise ValueError('step must be non-zero')
        if step > 0:
            while v <= stop:
                values.append(round(v, 6))
                v += step
        else:
            while v >= stop:
                values.append(round(v, 6))
                v += step
        return values
    else:
        parts = [p.strip() for p in s.split(',') if p.strip()]
        return [float(p) for p in parts]


def count_valid_combinations(highway_speeds, ramp_speeds, mainline_flows, ramp_flows):
    """Count combinations where highway_speed > ramp_speed without building the full grid."""
    c = 0
    for hs in highway_speeds:
        for rs in ramp_speeds:
            if float(hs) <= float(rs):
                continue
            for mf in mainline_flows:
                for rf in ramp_flows:
                    c += 1
    return c


def build_filtered_generator(highway_speeds, ramp_speeds, mainline_flows, ramp_flows):
    """Yield parameter dicts where highway_speed > ramp_speed (streaming, memory-light)."""
    for hs in highway_speeds:
        for rs in ramp_speeds:
            if float(hs) <= float(rs):
                continue
            for mf in mainline_flows:
                for rf in ramp_flows:
                    yield {
                        'highway_speed': float(hs),
                        'ramp_speed': float(rs),
                        'mainline_flow': int(mf),
                        'rampline_flow': int(rf),
                    }


def frange(start, stop, step):
    """Float range generator (inclusive when step fits exactly)."""
    x = float(start)
    if step == 0:
        raise ValueError('step must be non-zero')
    if step > 0:
        while x <= stop:
            yield round(x, 6)
            x += step
    else:
        while x >= stop:
            yield round(x, 6)
            x += step


def create_iteration_folder(iteration):
    """Create a folder for this iteration's results"""
    folder = f"Analysis/analysis_results/iteration_{iteration}"
    os.makedirs(folder, exist_ok=True)
    return folder


def main():
    # Hard-coded parameter lists (no CLI parameters). Adjust these lists here.
    highway_speeds = list(frange(25.0, 129.5, 0.5))   # 25.0 .. 129.5 by 0.5
    ramp_speeds = list(frange(15.0, 99.5, 0.5))       # 15.0 .. 99.5 by 0.5
    mainline_flows = list(range(800, 5000, 50))      # 800 .. 4950 step 50
    ramp_flows = list(range(200, 2000, 25))          # 200 .. 1975 step 25

    # Use streaming generator to avoid building the full grid in memory
    total = count_valid_combinations(highway_speeds, ramp_speeds, mainline_flows, ramp_flows)
    if total == 0:
        print('No parameter combinations generated (check that highway_speed > ramp_speed for at least one pair).')
        return

    print(f"Starting multiple simulation runs... total iterations: {total}")

    gen = build_filtered_generator(highway_speeds, ramp_speeds, mainline_flows, ramp_flows)
    for i, params in enumerate(gen):
        print(f"\nIteration {i+1}/{total} -- {params}")
        print("=" * 50)

        # Create folder for this iteration's results
        results_folder = create_iteration_folder(i + 1)

        # Generate new edges and routes for this parameter set
        print("Generating new edges...")
        edges_file = generate_new_edges(params['highway_speed'], params['ramp_speed'])

        print("Generating new routes...")
        routes_file = generate_new_routes(params['mainline_flow'], params['rampline_flow'])
        if not routes_file:
            print(f"Failed to generate routes for iteration {i+1}")
            continue

        # Run SUMO simulation (headless)
        print("Running SUMO simulation...")
        sumo_cmd = 'sumo -c "ramp/ramp.sumocfg" ' + \
                  '--summary-output "Output/summary.xml" ' + \
                  '--tripinfo-output "Output/tripinfo.xml" ' + \
                  '--edgedata-output "Output/edgeData.xml"'
        if not run_command(sumo_cmd):
            print("SUMO simulation failed")
            continue

        # Run analysis scripts
        print("Running analysis...")
        analysis_scripts = [
            'Analysis/edgedata_analysis.py',
            'Analysis/summary_analysis.py',
            'Analysis/tripinfo_analysis.py',
            'Analysis/extract_info.py',
        ]

        for script in analysis_scripts:
            if not run_command(f'python {script}'):
                print(f"Analysis script {script} failed")

        # Move results to iteration folder
        result_files = [
            'Analysis/analysis_results/edge_density.csv',
            'Analysis/analysis_results/summary_steps.csv',
            'Analysis/analysis_results/tripinfo_summary.csv',
            'Analysis/analysis_results/mean_speed_with_config.csv',
        ]

        for file in result_files:
            if os.path.exists(file):
                new_name = os.path.join(results_folder, os.path.basename(file))
                shutil.move(file, new_name)

        print(f"Completed iteration {i+1}")

    print("\nAll iterations complete!")
    print("Results are saved in Analysis/analysis_results/iteration_X folders")


if __name__ == "__main__":
    main()
import os
import subprocess
import shutil
from datetime import datetime
from Project_lab.generation.generate_xml import RouteXMLGenerator, EdgeXMLGenerator
import numpy as np


def run_command(command):
    """Run a shell command and return True if it succeeds."""
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"⚠️ Warning: Command failed:\n{command}\nError:\n{process.stderr}")
    return process.returncode == 0


def generate_new_routes(mainline_flow, rampline_flow, routes_file="ramp/ramp.rou.xml"):
    """Generate a route XML file for given flow rates."""
    generator = RouteXMLGenerator(
        mainline_vehs_per_hour=int(mainline_flow),
        rampline_vehs_per_hour=int(rampline_flow),
        output_file=routes_file
    )
    generator.generate_xml()
    return routes_file


def generate_new_edges(highway_speed, ramp_speed, edges_file="ramp/ramp.edg.xml"):
    """Generate an edge XML file for given speeds."""
    edge_generator = EdgeXMLGenerator(
        highway_speed=float(highway_speed),
        ramp_speed=float(ramp_speed),
        output_file=edges_file
    )
    edge_generator.generate_xml()
    return edges_file


def count_valid_combinations(highway_speeds, ramp_speeds, mainline_flows, ramp_flows):
    """Count combinations where highway_speed > ramp_speed without storing them."""
    count = 0
    for hs in highway_speeds:
        for rs in ramp_speeds:
            if hs <= rs:
                continue
            for _ in mainline_flows:
                for _ in ramp_flows:
                    count += 1
    return count


def build_filtered_generator(highway_speeds, ramp_speeds, mainline_flows, ramp_flows):
    """Yield only valid parameter combinations (highway_speed > ramp_speed)."""
    for hs in highway_speeds:
        for rs in ramp_speeds:
            if hs <= rs:
                continue
            for mf in mainline_flows:
                for rf in ramp_flows:
                    yield {
                        "highway_speed": hs,
                        "ramp_speed": rs,
                        "mainline_flow": mf,
                        "rampline_flow": rf
                    }


def create_iteration_folder(iteration):
    """Create a folder for this iteration's results."""
    folder = f"Analysis/analysis_results/iteration_{iteration:04d}"
    os.makedirs(folder, exist_ok=True)
    return folder


def main():
    # === Parameter Space ===
    highway_speeds = np.arange(25.0, 130.0, 5.0).tolist()
    ramp_speeds = np.arange(15.0, 100.0, 5.0).tolist()
    mainline_flows = np.arange(800, 5000, 400).tolist()
    ramp_flows = np.arange(200, 2000, 200).tolist()

    # Count total valid combinations
    total_combos = count_valid_combinations(highway_speeds, ramp_speeds, mainline_flows, ramp_flows)
    print(f"🚀 Starting parameter sweep: {total_combos} total valid combinations\n")

    # === Main Simulation Loop ===
    for i, params in enumerate(build_filtered_generator(highway_speeds, ramp_speeds, mainline_flows, ramp_flows), start=1):
        print(f"\n▶ Iteration {i}/{total_combos} | {params}")
        print("=" * 60)

        iteration_folder = create_iteration_folder(i)

        # Generate XML files
        print("🛠️ Generating edges and routes...")
        generate_new_edges(params["highway_speed"], params["ramp_speed"])
        generate_new_routes(params["mainline_flow"], params["rampline_flow"])

        # Run SUMO simulation
        print("🚦 Running SUMO simulation...")
        sumo_cmd = (
            'sumo -c "ramp/ramp.sumocfg" '
            '--summary-output "Output/summary.xml" '
            '--tripinfo-output "Output/tripinfo.xml" '
            '--edgedata-output "Output/edgeData.xml"'
        )
        if not run_command(sumo_cmd):
            print("❌ SUMO simulation failed; skipping this iteration.")
            continue

        # Run analysis scripts
        print("📊 Running analysis scripts...")
        analysis_scripts = [
            "Analysis/edgedata_analysis.py",
            "Analysis/summary_analysis.py",
            "Analysis/tripinfo_analysis.py",
            "Analysis/extract_info.py"
        ]
        for script in analysis_scripts:
            if not run_command(f'python "{script}"'):
                print(f"⚠️ Analysis script {script} failed, continuing...")

        # Move results
        print("📁 Moving analysis results...")
        result_files = [
            "Analysis/analysis_results/edge_density.csv",
            "Analysis/analysis_results/summary_steps.csv",
            "Analysis/analysis_results/tripinfo_summary.csv",
            "Analysis/analysis_results/mean_speed_with_config.csv"
        ]
        for file in result_files:
            if os.path.exists(file):
                shutil.move(file, os.path.join(iteration_folder, os.path.basename(file)))

        print(f"✅ Completed iteration {i}/{total_combos}")

    print("\n🎉 All iterations complete! Results saved in:")
    print("   → Analysis/analysis_results/iteration_XXXX folders")


if __name__ == "__main__":
    main()
