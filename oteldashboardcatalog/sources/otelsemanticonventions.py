import os
import shutil
import subprocess
import tempfile
import yaml

from ..types import Dashboard, DashboardGroup, DashboardMetric, MetricAttribute

def _parse_metric(metricyaml):
    attributes = {}
    for attr in metricyaml.get("attributes", []):
        requirement_level = attr.get("requirement_level")
        try:
            if requirement_level["conditionally_required"]:
                requirement_level = "required"
        except:
            pass
        print(requirement_level)
        if "ref" in attr:
            attributes.setdefault(requirement_level, []).append(attr["ref"])
        elif "id" in attr:
            attributes.setdefault(requirement_level, []).append(attr["id"])
    return DashboardMetric(
            metricyaml["metric_name"], 
            metricyaml["instrument"], 
            metricyaml["unit"], 
            metricyaml["brief"],
            attributes)

def _parse_attributes(groupyaml):
    prefix = groupyaml.get("prefix", "")
    attrs = []
    for attryaml in groupyaml.get("attributes", []):
        if not "id" in attryaml:
            continue
        name = attryaml["id"]
        if prefix:
            name = "%s.%s" % (prefix, name)
        attrs.append(MetricAttribute(
            name,
            groupyaml["type"],
            groupyaml["brief"],
            groupyaml.get("stability", None)))
    return attrs

def _get_all_yaml_files(directory):
    dirs = [directory]

    while dirs:
        d = dirs.pop()
        for fname in os.listdir(d):
            full_path = os.path.join(d, fname)
            if os.path.isdir(full_path):
                dirs.append(full_path)
                continue
            if full_path.endswith(".yaml"):
                yield full_path

def resolve():
    try:
        tmpdir =  tempfile.mkdtemp()

        subprocess.call(
                ["git", "clone", "--depth", "1", "https://github.com/open-telemetry/semantic-conventions", "."],
                cwd=tmpdir,
                stdout=subprocess.DEVNULL)

        metric_definition_dir = os.path.join(tmpdir, "model")
        metric_groups = []
        attributes = []

        for fname in _get_all_yaml_files(metric_definition_dir):
            metrics = []

            with open(fname, "r") as f:
                metric_definition = yaml.safe_load(f)

                for group in metric_definition["groups"]:
                    if group["type"] == "metric":
                        metrics.append(_parse_metric(group))
                    elif group["type"] == "attribute_group":
                        attributes.extend(_parse_attributes(group))

            if metrics:
                metric_group_name = os.path.splitext(os.path.basename(fname))[0]
                metric_group_name = metric_group_name.replace("-metrics", "")
                metric_groups.append(DashboardGroup(
                    "OpenTelemetry Semantic Conventions", 
                    metric_group_name.upper(), 
                    metrics))

        return Dashboard("OpenTelemetry semantic conventions", metric_groups)
    finally:
        shutil.rmtree(tmpdir)
