import xml.etree.ElementTree as ET
from xml.dom import minidom

class EdgeXMLGenerator:
    """
    A class to generate SUMO edge XML files defining the road network topology.
    """

    def __init__(self, highway_speed:int, ramp_speed:int, output_file: str = "edges.xml"):
        """
        Initialize the edge generator.

        Args:
            highway_speed (int): Speed limit for the highway edges.
            ramp_speed (int): Speed limit for the ramp edge.
            output_file (str): Output XML filename.
        """
        self.highway_speed = highway_speed
        self.ramp_speed = ramp_speed
        self.output_file = output_file

        # Define edge data
        self.edges = [
            {
                "comment": "Highway, 2 lanes, higher priority",
                "attrs": {
                    "id": "main_0",
                    "from": "N0",
                    "to": "N1",
                    "priority": "3",
                    "numLanes": "2",
                    "speed": f"{self.highway_speed}"
                }
            },
            {
                "comment": "Highway segment WITH acceleration lane (3 lanes right after the merge)",
                "attrs": {
                    "id": "main_1a",
                    "from": "N1",
                    "to": "N1A",
                    "priority": "3",
                    "numLanes": "3",
                    "speed": f"{self.highway_speed}"
                }
            },
            {
                "comment": "Highway segment AFTER acceleration lane ends (back to 2 lanes)",
                "attrs": {
                    "id": "main_1b",
                    "from": "N1A",
                    "to": "N2",
                    "priority": "3",
                    "numLanes": "2",
                    "speed": f"{self.highway_speed}"
                }
            },
            {
                "comment": "Driveway / on-ramp, 1 lane, lower priority",
                "attrs": {
                    "id": "ramp_0",
                    "from": "R0",
                    "to": "N1",
                    "priority": "1",
                    "numLanes": "1",
                    "speed": f"{self.ramp_speed}"
                }
            }
        ]

    def generate_xml(self):
        """Generate the XML structure and write it to a file."""
        edges_root = ET.Element("edges")

        # Add edges with comments
        for edge in self.edges:
            edges_root.append(ET.Comment(edge["comment"]))
            ET.SubElement(edges_root, "edge", edge["attrs"])

        # Pretty-print and write to file
        xml_str = minidom.parseString(ET.tostring(edges_root, encoding="utf-8")).toprettyxml(indent="  ")
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            for line in xml_str.splitlines()[1:]:  # Skip redundant header
                if line.strip():
                    f.write(line + "\n")

        print(f"✅ XML file '{self.output_file}' generated successfully.")


class RouteXMLGenerator:
    """
    A class to generate SUMO route XML files with configurable mainline
    and ramp flow vehicle rates.
    """

    def __init__(self, mainline_vehs_per_hour: int, rampline_vehs_per_hour: int, output_file: str = "ramp/routes.xml"):
        """
        Initialize the XML generator with traffic flow parameters.

        Args:
            mainline_vehs_per_hour (int): Vehicles per hour for the mainline flow.
            rampline_vehs_per_hour (int): Vehicles per hour for the ramp flow.
            output_file (str): Output XML filename.
        """
        self.mainline_vehs_per_hour = mainline_vehs_per_hour
        self.rampline_vehs_per_hour = rampline_vehs_per_hour
        self.output_file = output_file

        # Define vehicle type
        self.car_type = {
            "id": "car",
            "accel": "2.6",
            "decel": "4.5",
            "length": "5.0",
            "maxSpeed": "38.0",
            "sigma": "0.5",
            "lcStrategic": "1.0",
            "lcCooperative": "1.0",
            "lcSpeedGain": "1.0",
            "lcKeepRight": "1.5"
        }

        # Define flow configurations
        self.mainline_flow = {
            "id": "mainFlow",
            "type": "car",
            "begin": "0",
            "end": "600",
            "vehsPerHour": str(self.mainline_vehs_per_hour),
            "departLane": "free",
            "departSpeed": "max"
        }

        self.rampline_flow = {
            "id": "rampFlow",
            "type": "car",
            "begin": "0",
            "end": "600",
            "vehsPerHour": str(self.rampline_vehs_per_hour),
            "departLane": "free",
            "departSpeed": "max"
        }

    def generate_xml(self):
        """Generate the XML structure and write it to a file."""
        routes = ET.Element("routes")

        # Vehicle type
        routes.append(ET.Comment("Vehicle type with default LC2013 lane-change model"))
        ET.SubElement(routes, "vType", self.car_type)

        # Mainline flow
        routes.append(ET.Comment("Mainline flow: steady highway traffic"))
        main_flow = ET.SubElement(routes, "flow", self.mainline_flow)
        ET.SubElement(main_flow, "route", {"edges": "main_0 main_1a main_1b"})

        # Ramp flow
        routes.append(ET.Comment("Ramp flow: driveway vehicles merging in and using accel lane"))
        ramp_flow = ET.SubElement(routes, "flow", self.rampline_flow)
        ET.SubElement(ramp_flow, "route", {"edges": "ramp_0 main_1a main_1b"})

        # Pretty-print and write to file
        xml_str = minidom.parseString(ET.tostring(routes, encoding="utf-8")).toprettyxml(indent="  ")
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            for line in xml_str.splitlines()[1:]:  # Skip redundant header
                if line.strip():
                    f.write(line + "\n")

        print(f"✅ XML file '{self.output_file}' generated successfully.")


