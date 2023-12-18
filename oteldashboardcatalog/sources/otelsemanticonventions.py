import glob
import os
import shutil
import subprocess
import tempfile
import yaml

from .opentelemetry.semconv.model import semantic_convention, semantic_attribute
from ..types import Dashboard, DashboardGroup, DashboardMetric, MetricAttribute

def resolve():
    try:
        tmpdir =  tempfile.mkdtemp()

        subprocess.call(
                ["git", "clone", "--depth", "1", "https://github.com/open-telemetry/semantic-conventions", "."],
                cwd=tmpdir,
                stdout=subprocess.DEVNULL)

        yaml_files = set(
            glob.glob(f"{tmpdir}/model/**/*.yaml", recursive=True)
        ).union(set(glob.glob(f"{tmpdir}/model/**/*.yml", recursive=True)))

        semconv = semantic_convention.SemanticConventionSet(False)

        for file in yaml_files:
            semconv.parse(file)

        semconv.finish()

        if semconv.has_error():
            raise SyntaxError()

        metric_groups = {}

        for name, model in semconv.models.items():
            if isinstance(model, semantic_convention.MetricSemanticConvention):
                group_name = os.path.splitext(os.path.basename(model.sourcefile))[0]
                group_name = group_name.replace("-metrics", "")

                if not group_name in metric_groups:
                    metric_groups[group_name] = DashboardGroup(
                        "OpenTelemetry Semantic Conventions", 
                        group_name.upper(), 
                        [])

                required_attributes = [ attr.fqn for attr in model.attributes if attr.requirement_level and attr.requirement_level.value == semantic_attribute.RequirementLevel.REQUIRED.value ]

                metric = DashboardMetric(
                    model.metric_name,
                    model.instrument, 
                    model.unit, 
                    model.brief,
                    required_attributes)

                metric_groups[group_name].metrics.append(metric)

        return Dashboard("OpenTelemetry semantic conventions", sorted(metric_groups.values(), key=lambda group: group.subtitle))
    finally:
        shutil.rmtree(tmpdir)
