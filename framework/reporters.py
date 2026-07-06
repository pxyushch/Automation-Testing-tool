
import xml.etree.ElementTree as ET

def generate_junit_xml(results, output_path="junit.xml"):
    testsuite = ET.Element("testsuite", name="AutomationSuite", tests=str(len(results)))
    for r in results:
        tc = ET.SubElement(testsuite, "testcase", name=r["name"], time=str(r.get("duration", 0.1)))
        if not r.get("passed", True):
            ET.SubElement(tc, "failure", message="Assertion failed")
    tree = ET.ElementTree(testsuite)
    tree.write(output_path)
