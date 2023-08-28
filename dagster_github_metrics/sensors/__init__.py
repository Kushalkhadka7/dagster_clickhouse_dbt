from dagster import (
    sensor,
    define_asset_job,
    RunRequest,
    RunConfig,
    Config,
    DagsterEvent,
)
import os

MY_DIRECTORY = "./"

from ..assets import raw_assets


class FileConfig(Config):
    filename: str


raw_github_commits_job = define_asset_job(
    "raw_github_commits_job", selection=[*raw_assets]
)


@sensor(name="test_sensor", job=raw_github_commits_job)
def test_sensor(context):
    yield RunRequest(
        run_key="test",
        run_config=RunConfig(ops={"process_file": FileConfig(filename="test")}),
    )
