METRIC = {
  "datasource": {
    "type": "prometheus",
    "uid": "${DS_INPUT}"
  },
  "description": "%(description)s",
  "fieldConfig": {
    "defaults": {
      "color": {
        "mode": "palette-classic"
      },
      "custom": {
        "axisBorderShow": False,
        "axisCenteredZero": False,
        "axisColorMode": "text",
        "axisLabel": "",
        "axisPlacement": "auto",
        "barAlignment": 0,
        "drawStyle": "line",
        "fillOpacity": 0,
        "gradientMode": "none",
        "hideFrom": {
          "legend": False,
          "tooltip": False,
          "viz": False
        },
        "insertNulls": False,
        "lineInterpolation": "linear",
        "lineWidth": 1,
        "pointSize": 5,
        "scaleDistribution": {
          "type": "linear"
        },
        "showPoints": "auto",
        "spanNulls": False,
        "stacking": {
          "group": "A",
          "mode": "none"
        },
        "thresholdsStyle": {
          "mode": "off"
        }
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": None 
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      }
    },
    "overrides": []
  },
  "gridPos": {
      "h": 8,
      "w": 12,
      "x": 0,
      "y": 0
  },
  "id": 1,
  "options": {
    "legend": {
      "calcs": [],
      "displayMode": "list",
      "placement": "bottom",
      "showLegend": True
    },
    "tooltip": {
      "mode": "single",
      "sort": "none"
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_INPUT}"
      },
      "disableTextWrap": False,
      "editorMode": "builder",
      "expr": "%(name)s",
      "fullMetaSearch": False,
      "includeNullMetadata": True,
      "instant": False,
      "legendFormat": "__auto",
      "range": True,
      "refId": "A",
      "useBackend": False
    }
  ],
  "title": "%(name)s",
  "type": "timeseries"
}, 8

DASHBOARD = {
  "__inputs": [
    {
      "name": "DS_INPUT",
      "label": "input",
      "description": "",
      "type": "datasource",
      "pluginId": "prometheus",
      "pluginName": "Prometheus"
    }
  ],
  "__elements": {},
  "__requires": [
    {
      "type": "grafana",
      "id": "grafana",
      "name": "Grafana",
      "version": "10.3.0-64082"
    },
    {
      "type": "datasource",
      "id": "prometheus",
      "name": "Prometheus",
      "version": "1.0.0"
    },
    {
      "type": "panel",
      "id": "timeseries",
      "name": "Time series",
      "version": ""
    }
  ],
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {
          "type": "grafana",
          "uid": "${DS_INPUT}"
        },
        "enable": True,
        "hide": True,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": True,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": None,
  "links": [],
  "liveNow": False,
  "panels": [],
  "refresh": "",
  "schemaVersion": 39,
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-2d",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "OTel semantic convention metrics",
  "uid": "e601c316-7813-498e-a4c7-b72854961a62",
  "version": 1,
  "weekStart": ""
}, None

ROW = {
    "title": "%(row_title)s",
    "type": "row",
    "collapsed": True,
    "gridPos": {
      "h": 1,
      "w": 24,
      "x": 0,
      "y": 0
    },
  }, 1

SECTION_HEADER = {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_INPUT}"
      },
      "gridPos": {
        "h": 3,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 95,
      "options": {
        "code": {
          "language": "plaintext",
          "showLineNumbers": False,
          "showMiniMap": False
        },
        "content": "# FAAS",
        "mode": "markdown"
      },
      "pluginVersion": "10.3.0-64167",
      "title": "OpenTelemetry Semantic Conventions",
      "type": "text"
    }, 3

METRIC_AVAILABLE = {
      "datasource": {
        "type": "prometheus",
        "uid": "${DS_INPUT}"
      },
      "description": "",
      "fieldConfig": {
        "defaults": {
          "mappings": [
            {
              "options": {
                "match": "null",
                "result": {
                  "index": 0,
                  "text": "not available"
                }
              },
              "type": "special"
            }
          ],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "red",
                "value": None
              },
              {
                "color": "green",
                "value": 1
              }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 2,
        "w": 2,
        "x": 0,
        "y": 3 
      },
      "id": 252,
      "options": {
        "colorMode": "background",
        "graphMode": "none",
        "justifyMode": "auto",
        "orientation": "auto",
        "reduceOptions": {
          "calcs": [
            "lastNotNull"
          ],
          "fields": "",
          "values": False
        },
        "textMode": "auto",
        "wideLayout": True
      },
      "pluginVersion": "10.3.0-64167",
      "targets": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${DS_INPUT}"
          },
          "disableTextWrap": False,
          "editorMode": "builder",
          "expr": "count(aspnetcore_routing_match_attempts)",
          "fullMetaSearch": False,
          "includeNullMetadata": True,
          "instant": False,
          "legendFormat": "__auto",
          "range": True,
          "refId": "A",
          "useBackend": False
        }
      ],
      "title": " ",
      "transparent": True,
      "type": "stat"
    }, 2
