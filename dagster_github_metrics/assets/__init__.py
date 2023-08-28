from dagster._utils import file_relative_path
from dagster import load_assets_from_package_module, AutoMaterializePolicy
from dagster_dbt import load_assets_from_dbt_project

from . import raw, api

DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_github_metrics")
DBT_PROFILES_DIR = file_relative_path(__file__, "../../dbt_github_metrics/config")

raw_assets = load_assets_from_package_module(
    package_module=raw,
    group_name="raw",
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)

api_assets = load_assets_from_package_module(
    package_module=api,
    group_name="api",
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)

# # all assets live in the default dbt_schema
dbt_assets = load_assets_from_dbt_project(
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
    # the schemas are already specified in dbt, so we don't need to also specify them in the key
    # prefix here
    key_prefix=["raw"],
    source_key_prefix=["raw_data"],
)
