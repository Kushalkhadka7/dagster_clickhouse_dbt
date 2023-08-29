import os

from dagster import Definitions

from .sensors import test_sensor
from .resources import RESOURCES_LOCAL
from .assets import dbt_assets, raw_assets, api_assets


resources_by_deployment_env = {
    "local": RESOURCES_LOCAL,
}

all_sensors = [test_sensor]

deployment_env = os.environ.get("DAGSTER_DEPLOYMENT_ENV", "local")

defs = Definitions(
    assets=[*dbt_assets, *raw_assets, *api_assets],
    resources=resources_by_deployment_env[deployment_env],
    sensors=all_sensors,
)
