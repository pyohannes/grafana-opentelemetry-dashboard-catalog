import json

from oteldashboardcatalog.sources import otelsemanticonventions
from oteldashboardcatalog.types import Dashboard

if __name__ == "__main__":
    sources = [ otelsemanticonventions ]

    if len(sources) == 1:
        dashboard = sources[0].resolve()
    else:
        dashboard = Dashboard("Merged semantic conventions")
        for source in sources:
            dashboard.groups.extend(source.resolve().groups)

    print(json.dumps(dashboard.to_json(), indent=4))
