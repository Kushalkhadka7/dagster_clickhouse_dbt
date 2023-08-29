import os

from dagster import Output, asset, AssetIn

from ...resources.api_io_manager import APIClient
from ...constants import (
    COMMITS_API_URL,
    COMMITS_DIR_PATH,
    COMMITS_FILE_NAME,
    FILE_CHANGES_API_URL,
    LINE_CHANGES_API_URL,
    FILE_CHANGES_DIR_PATH,
    FILE_CHANGES_FILE_NAME,
    LINE_CHANGES_DIR_PATH,
    LINE_CHANGES_FILE_NAME,
    COMMITS_FILE_NAME_ZIPPED,
    FILE_CHANGES_FILE_NAME_ZIPPED,
    LINE_CHANGES_FILE_NAME_ZIPPED,
)


@asset(
    key_prefix=["api"],
)
async def sync_files(context):
    return Output(
        value="SUCCESS",
        metadata={"action": "Sync files"},
    )


@asset(key_prefix=["api"], ins={"sync_files": AssetIn(key_prefix=["api"])})
async def commits(context, sync_files, github_api: APIClient):
    file_directory_path = os.getcwd() + COMMITS_DIR_PATH

    await github_api.download_file(
        url=COMMITS_API_URL,
        dirName=file_directory_path,
        fileName=COMMITS_FILE_NAME_ZIPPED,
    )

    return Output(
        value="SUCCESS",
        metadata={"file_name": COMMITS_FILE_NAME},
    )


@asset(key_prefix=["api"], ins={"sync_files": AssetIn(key_prefix=["api"])})
async def file_changes(context, sync_files, github_api: APIClient):
    file_directory_path = os.getcwd() + FILE_CHANGES_DIR_PATH

    await github_api.download_file(
        url=FILE_CHANGES_API_URL,
        dirName=file_directory_path,
        fileName=FILE_CHANGES_FILE_NAME_ZIPPED,
    )

    return Output(
        value="SUCCESS",
        metadata={"file_name": FILE_CHANGES_FILE_NAME},
    )


@asset(key_prefix=["api"], ins={"sync_files": AssetIn(key_prefix=["api"])})
async def line_changes(context, sync_files, github_api: APIClient):
    file_directory_path = os.getcwd() + LINE_CHANGES_DIR_PATH

    await github_api.download_file(
        url=LINE_CHANGES_API_URL,
        dirName=file_directory_path,
        fileName=LINE_CHANGES_FILE_NAME_ZIPPED,
    )

    return Output(
        value="SUCCESS",
        metadata={"file_name": LINE_CHANGES_FILE_NAME},
    )
