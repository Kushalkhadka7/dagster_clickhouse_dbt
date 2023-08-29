from dagster_dbt import DbtCliClientResource
from dagster._utils import file_relative_path

from .api_io_manager import GithubApiClient
from .clickhouse_io_manager import ClickhouseIOManager
from ..constants import DBT_PROJECT_CONFIG_PATH, DBT_PROJECT_PATH

DBT_PROJECT_DIR = file_relative_path(__file__, DBT_PROJECT_PATH)
DBT_PROFILES_DIR = file_relative_path(__file__, DBT_PROJECT_CONFIG_PATH)


# Load dbt models using `local` profile.
dbt_local_resource = DbtCliClientResource(
    profiles_dir=DBT_PROFILES_DIR,
    project_dir=DBT_PROJECT_DIR,
    target="local",
)

RESOURCES_LOCAL = {
    "dbt": dbt_local_resource,
    "github_api": GithubApiClient(),
    "clickhouse_io_manager": ClickhouseIOManager(),
}
