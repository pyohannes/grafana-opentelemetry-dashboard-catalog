import copy
import json

from . import templates

class Dashboard(object):
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups

    def to_json(self):
        jsondata = copy.deepcopy(templates.DASHBOARD)

        jsondata["title"] = self.name

        for group in self.groups:
            jsondata["panels"].extend(group.to_json())

        return jsondata

class DashboardGroup(object):
    def __init__(self, title, subtitle, metrics):
        self.title = title
        self.subtitle = subtitle
        self.metrics = metrics

    def to_json(self):
        items = []
        
        jsondata_header = copy.deepcopy(templates.SECTION_HEADER)
        jsondata_header["title"] = self.title
        jsondata_header["options"]["content"] = "# %s" % self.subtitle

        items.append(jsondata_header)

        for index, metric in enumerate(self.metrics):
            jsondata = copy.deepcopy(templates.ROW)
            jsondata["title"] = metric.name
            jsondata["panels"] = []
            metricjsons = metric.to_json()
            jsondata["panels"].extend(metricjsons)
            items.append(jsondata)

        return items

class DashboardMetric(object):

    unit_map = {
        "By": "bytes"
    }

    def __init__(self, name, instrument, unit, description, attributes=None):
        self.name = name
        self.instrument = instrument
        self.unit = unit
        self.description = description
        self.attributes = attributes or {}

        if self.unit in self.unit_map:
            self.unit = self.unit_map[self.unit]

    def to_json(self):
        panels = []

        if self.instrument == "histogram":
            extension = "_sum"
        else:
            extension = ""

        panels.append(self._to_json(
            self.name, 
            self.description, 
            "avg(%s)" % (self.name.replace('.', '_') + extension)))
        print(self.attributes)
        for required_attr in self.attributes.get("required", []):
            panels.append(self._to_json(
                "%s by %s" % (self.name, required_attr),
                self.description, 
                "avg by(%s) (%s)" % (required_attr.replace(".", "_"), self.name.replace('.', '_') + extension)))

        return panels


    def _to_json(self, name, description, query):
        jsondata = copy.deepcopy(templates.METRIC)

        jsondata["description"] = self.description
        jsondata["title"] = self.name
        jsondata["fieldConfig"]["defaults"]["unit"] = self.unit
        for target in jsondata["targets"]:
            extension = ""
            if self.instrument == "histogram":
                extension = "_sum"
            target["expr"] = query

        return jsondata

class MetricAttribute(object):
    def __init__(self, name, type, brief, stability):
        self.name = name
        self.type = type
        self.brief = brief
        self.stability = stability
