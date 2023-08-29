import os
import pandas as pd

from dagster import asset, AssetIn, OutputContext, SkipReason, Output

from ...constants import (
    COMMITS_DIR_PATH,
    COMMITS_FILE_NAME,
    FILE_CHANGES_DIR_PATH,
    FILE_CHANGES_FILE_NAME,
    LINE_CHANGES_DIR_PATH,
    LINE_CHANGES_FILE_NAME,
    COMMIT_TABLE_COLUMNS,
    FILE_CHANGES_TABLE_COLUMNS,
    LINE_CHANGES_TABLE_COLUMNS,
)


@asset(
    key_prefix=["raw"],
    io_manager_key="clickhouse_io_manager",
    ins={"commits": AssetIn(key_prefix=["api"])},
)
def commits(context: OutputContext, commits):
    if commits != "SUCCESS":
        print("Skipping transformation no files is loaded")

        return SkipReason("Skipping transformation no files is loaded")

    curr_dir = os.getcwd()

    file_directory_path = os.getcwd() + COMMITS_DIR_PATH

    os.chdir(file_directory_path)

    df = pd.read_csv(COMMITS_FILE_NAME, sep="\t")

    os.chdir(curr_dir)

    return Output(
        pd.DataFrame(df),
        metadata={"table_name": "commits", "columns": COMMIT_TABLE_COLUMNS},
    )


@asset(
    key_prefix=["raw"],
    io_manager_key="clickhouse_io_manager",
    ins={"file_changes": AssetIn(key_prefix=["api"])},
)
def file_changes(file_changes):
    if file_changes != "SUCCESS":
        print("Skipping transformation no files is loaded")

        return SkipReason("Skipping transformation no files is loaded")

    curr_dir = os.getcwd()

    file_directory_path = os.getcwd() + FILE_CHANGES_DIR_PATH

    os.chdir(file_directory_path)

    df = pd.read_csv(FILE_CHANGES_FILE_NAME, sep="\t")

    os.chdir(curr_dir)

    return Output(
        pd.DataFrame(df),
        metadata={"table_name": "file_changes", "columns": FILE_CHANGES_TABLE_COLUMNS},
    )


@asset(
    key_prefix=["raw"],
    io_manager_key="clickhouse_io_manager",
    ins={"line_changes": AssetIn(key_prefix=["api"])},
)
def line_changes(line_changes):
    if line_changes != "SUCCESS":
        print("Skipping transformation no files is loaded")

        return SkipReason("Skipping transformation no files is loaded")

    curr_dir = os.getcwd()

    file_directory_path = os.getcwd() + LINE_CHANGES_DIR_PATH

    os.chdir(file_directory_path)

    df = pd.read_csv(LINE_CHANGES_FILE_NAME, nrows=253750, sep="\t")
    os.chdir(curr_dir)

    return Output(
        pd.DataFrame(df),
        metadata={"table_name": "line_changes", "columns": LINE_CHANGES_TABLE_COLUMNS},
    )


@asset(
    key_prefix=["raw_data"],
    ins={
        "commits": AssetIn(key_prefix=["raw"]),
        "line_changes": AssetIn(key_prefix=["raw"]),
        "file_changes": AssetIn(key_prefix=["raw"]),
    },
)
def data_loaded(commits, file_changes, line_changes):
    return commits, file_changes, line_changes
