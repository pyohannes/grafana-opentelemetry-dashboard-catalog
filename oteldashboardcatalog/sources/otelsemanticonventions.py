import os
import shutil
import subprocess
import tempfile
import yaml

from ..types import Dashboard, DashboardGroup, DashboardMetric

def resolve():
    try:
        tmpdir =  tempfile.mkdtemp()

        subprocess.call(
                ["git", "clone", "--depth", "1", "https://github.com/open-telemetry/semantic-conventions", "."],
                cwd=tmpdir,
                stdout=subprocess.DEVNULL)

        metric_definition_dir = os.path.join(tmpdir, "model", "metrics")
        metric_groups = []

        for metric_file in os.listdir(metric_definition_dir):
            with open(os.path.join(metric_definition_dir, metric_file), "r") as f:
                    metric_definition = yaml.safe_load(f)

                    metrics = [ 
                        DashboardMetric(group["metric_name"], group["instrument"], group["unit"], group["brief"])
                        for group in metric_definition["groups"]
                        if group["type"] == "metric"
                    ]

                    metric_group_name = os.path.splitext(metric_file)[0]
                    metric_groups.append(DashboardGroup(metric_group_name, metrics))

        return Dashboard("OpenTelemetry semantic conventions", metric_groups)
    finally:
        shutil.rmtree(tmpdir)
