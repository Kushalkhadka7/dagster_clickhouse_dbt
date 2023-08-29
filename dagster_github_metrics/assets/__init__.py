from dagster._utils import file_relative_path
from dagster_dbt import load_assets_from_dbt_project
from dagster import load_assets_from_package_module, AutoMaterializePolicy

from . import raw, api
from ..constants import DBT_PROJECT_PATH, DBT_PROJECT_CONFIG_PATH

DBT_PROJECT_DIR = file_relative_path(__file__, DBT_PROJECT_PATH)
DBT_PROFILES_DIR = file_relative_path(__file__, DBT_PROJECT_CONFIG_PATH)


# Load assets from modules and group them.
# All the assets form the package will be under `raw` group.
# All the downstream assets will get auto materialized when upstream asset gets materialized.
raw_assets = load_assets_from_package_module(
    package_module=raw,
    group_name="raw",
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)

# Load assets from modules and group them.
# All the assets form the package will be under `api` group.
# All the downstream assets will get auto materialized when upstream asset gets materialized.
api_assets = load_assets_from_package_module(
    package_module=api,
    group_name="api",
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)

# Load assets from dbt project.
# All the assets form the package will be under `raw` group.
# All the downstream assets will get auto materialized when upstream asset gets materialized.
dbt_assets = load_assets_from_dbt_project(
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
    key_prefix=["raw"],
    source_key_prefix=["raw_data"],
)
