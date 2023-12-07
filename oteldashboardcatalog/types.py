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
        jsondata["panels"] = [ group.to_json() for group in self.groups ]

        return jsondata

class DashboardGroup(object):
    def __init__(self, name, metrics):
        self.name = name
        self.metrics = metrics

    def to_json(self):
        jsondata = copy.deepcopy(templates.ROW)
        
        jsondata["title"] = self.name
        jsondata["panels"] = []
        for index, metric in enumerate(self.metrics):
            metricjson = metric.to_json()
            metricjson["gridPos"]["y"] = index % 2
            jsondata["panels"].append(metricjson)

        return jsondata

class DashboardMetric(object):
    def __init__(self, name, instrument, unit, description):
        self.name = name
        self.instrument = instrument
        self.unit = unit
        self.description = description

    def to_json(self):
        jsondata = copy.deepcopy(templates.METRIC)

        jsondata["description"] = self.description
        jsondata["title"] = self.name
        for target in jsondata["targets"]:
            extension = ""
            if self.instrument == "histogram":
                extension = "_sum"
            target["expr"] = "avg(%s)" % (self.name.replace('.', '_') + extension)

        return jsondata
