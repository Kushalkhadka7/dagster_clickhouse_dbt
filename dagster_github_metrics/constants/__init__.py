COMMITS_API_URL = "https://datasets-documentation.s3.amazonaws.com/github/commits/clickhouse/commits.tsv.xz"
COMMITS_DIR_PATH = "/dagster_github_metrics/data/commits/"
COMMITS_FILE_NAME = "commits.tsv"
COMMITS_FILE_NAME_ZIPPED = "commits.tsv.xz"

FILE_CHANGES_API_URL = "https://datasets-documentation.s3.amazonaws.com/github/commits/clickhouse/file_changes.tsv.xz"
FILE_CHANGES_DIR_PATH = "/dagster_github_metrics/data/file_changes/"
FILE_CHANGES_FILE_NAME = "file_changes.tsv"
FILE_CHANGES_FILE_NAME_ZIPPED = "file_changes.tsv.xz"

LINE_CHANGES_API_URL = "https://datasets-documentation.s3.amazonaws.com/github/commits/clickhouse/line_changes.tsv.xz"
LINE_CHANGES_DIR_PATH = "/dagster_github_metrics/data/line_changes/"
LINE_CHANGES_FILE_NAME = "line_changes.tsv"
LINE_CHANGES_FILE_NAME_ZIPPED = "line_changes.tsv.xz"


# Column names
COMMIT_TABLE_COLUMNS = [
    "hash",
    "author",
    "time",
    "message",
    "files_added",
    "files_deleted",
    "files_renamed",
    "files_modified",
    "lines_added",
    "lines_deleted",
    "hunks_added",
    "hunks_removed",
    "hunks_changed",
]

FILE_CHANGES_TABLE_COLUMNS = [
    "change_type",
    "path",
    "old_path",
    "file_extension",
    "lines_added",
    "lines_deleted",
    "hunks_added",
    "hunks_removed",
    "hunks_changed",
    "commit_hash",
    "author",
    "time",
    "commit_message",
    "commit_files_added",
    "commit_files_deleted",
    "commit_files_renamed",
    "commit_files_modified",
    "commit_lines_added",
    "commit_lines_deleted",
    "commit_hunks_added",
    "commit_hunks_removed",
    "commit_hunks_changed",
]

LINE_CHANGES_TABLE_COLUMNS = [
    "sign",
    "line_number_old",
    "line_number_new",
    "hunk_num",
    "hunk_start_line_number_old",
    "hunk_start_line_number_new",
    "hunk_lines_added",
    "hunk_lines_deleted",
    "hunk_context",
    "line",
    "indent",
    "line_type",
    "prev_commit_hash",
    "prev_author",
    "prev_time",
    "file_change_type",
    "path",
    "old_path",
    "file_extension",
    "file_lines_added",
    "file_lines_deleted",
    "file_hunks_added",
    "file_hunks_removed",
    "file_hunks_changed",
    "commit_hash",
    "author",
    "time",
    "commit_message",
    "commit_files_added",
    "commit_files_deleted",
    "commit_files_renamed",
    "commit_files_modified",
    "commit_lines_added",
    "commit_lines_deleted",
    "commit_hunks_added",
    "commit_hunks_removed",
    "commit_hunks_changed",
]

MAP_TABLE_COLUMNS = {
    "commits": COMMIT_TABLE_COLUMNS,
    "file_changes": FILE_CHANGES_TABLE_COLUMNS,
    "line_changes": LINE_CHANGES_TABLE_COLUMNS,
}

CLICK_HOUSE_CONFIG = {
    "db_name": "raw_github_metrics",
    "db_url": "http://localhost:8123",
    "username": "default",
    "password": "default",
}

DBT_PROJECT_PATH = "../../dbt_github_metrics"
DBT_PROJECT_CONFIG_PATH = "../../dbt_github_metrics/config"
