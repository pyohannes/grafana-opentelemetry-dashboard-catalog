import copy
import json

from . import templates

class Dashboard(object):
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups

    def to_json(self, position=0):
        jsondata, size = copy.deepcopy(templates.DASHBOARD)

        jsondata["title"] = self.name

        for group in self.groups:
            panels, position = group.to_json(position)
            jsondata["panels"].extend(panels)

        return jsondata, position

class DashboardGroup(object):
    def __init__(self, title, subtitle, metrics):
        self.title = title
        self.subtitle = subtitle
        self.metrics = metrics

    def to_json(self, position):
        items = []
       
        template, size = templates.SECTION_HEADER

        jsondata_header = copy.deepcopy(template)
        jsondata_header["title"] = self.title
        jsondata_header["options"]["content"] = "# %s" % self.subtitle
        jsondata_header["gridPos"]["y"] = position

        items.append(jsondata_header)
        position += size

        for index, metric in enumerate(self.metrics):
            panel, position = metric.to_availability_json(position)
            items.append(panel)

            template, size = templates.ROW

            jsondata = copy.deepcopy(template)
            jsondata["title"] = metric.name
            jsondata["panels"] = []
            jsondata["gridPos"]["y"] = position

            metricjsons, position = metric.to_json(position)
            jsondata["panels"].extend(metricjsons)

            items.append(jsondata)
            position += size

        return items, position

class DashboardMetric(object):

    unit_map = {
        "By": "bytes"
    }

    def __init__(self, name, instrument, unit, description, required_attributes=None):
        self.name = name
        self.instrument = instrument
        self.unit = unit
        self.description = description
        self.required_attributes = required_attributes or []

        if self.unit in self.unit_map:
            self.unit = self.unit_map[self.unit]

    def to_availability_json(self, position):
        template, size = templates.METRIC_AVAILABLE

        jsondata = copy.deepcopy(template)

        for target in jsondata["targets"]:
            target["expr"] = "count(%s)" % self.name.replace(".", "_")

        jsondata["gridPos"]["y"] = position

        position += size

        return jsondata, position

    def to_json(self, position):
        panels = []

        if self.instrument == "histogram":
            extension = "_sum"
        else:
            extension = ""

        panels.append(self._to_json(
            self.name, 
            self.description, 
            "avg(%s)" % (self.name.replace('.', '_') + extension),
            position,
            (len(panels)/ 2),
            len(panels)% 2))
        for required_attr in self.required_attributes:
            panels.append(self._to_json(
                "%s by %s" % (self.name, required_attr),
                self.description, 
                "avg by(%s) (%s)" % (required_attr.replace(".", "_"), self.name.replace('.', '_') + extension),
                position,
                (len(panels)/ 2) + 1,
                len(panels)% 2))

        return panels, position


    def _to_json(self, name, description, query, start_position, row, column):
        jsondata, size = copy.deepcopy(templates.METRIC)

        jsondata["description"] = description
        jsondata["title"] = name
        jsondata["fieldConfig"]["defaults"]["unit"] = self.unit
        for target in jsondata["targets"]:
            extension = ""
            if self.instrument == "histogram":
                extension = "_sum"
            target["expr"] = query
        jsondata["gridPos"]["x"] = jsondata["gridPos"]["w"] * column
        jsondata["gridPos"]["y"] = start_position + size * row

        return jsondata

class MetricAttribute(object):
    def __init__(self, name, type, brief, stability):
        self.name = name
        self.type = type
        self.brief = brief
        self.stability = stability
