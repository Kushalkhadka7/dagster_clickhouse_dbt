from dagster import Definitions, define_asset_job

import os

from .assets import dbt_assets, raw_assets, api_assets

from .sensors import test_sensor

from .resources import RESOURCES_LOCAL


resources_by_deployment_name = {
    "local": RESOURCES_LOCAL,
}


all_sensors = [test_sensor]

deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")

defs = Definitions(
    assets=[*dbt_assets, *raw_assets, *api_assets],
    resources=resources_by_deployment_name[deployment_name],
    sensors=all_sensors,
)
