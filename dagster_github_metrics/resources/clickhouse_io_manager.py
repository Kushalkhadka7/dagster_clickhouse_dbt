import pandas as pd

from pandas import DataFrame, isna
from clickhouse_driver import Client
from infi.clickhouse_orm.models import ModelBase
from infi.clickhouse_orm.engines import MergeTree
from infi.clickhouse_orm.fields import Int64Field, DateTime64Field, NullableField
from dagster import (
    InputContext,
    ConfigurableIOManager,
)

from ..constants import MAP_TABLE_COLUMNS


class MyNullableField(NullableField):
    def to_db_string(self, value, quote=True):
        if isna(value):
            return "\\N"
        return super().to_db_string(value, quote=quote)


class MyModel(ModelBase):
    @classmethod
    def create_ad_hoc_field(cls, db_type):
        if db_type == "Nullable(Int64)":
            return MyNullableField(Int64Field())
        if db_type == "Nullable(DateTime64)":
            return MyNullableField(DateTime64Field())

        return ModelBase.create_ad_hoc_field(db_type)


def convert_fields(df: DataFrame, override={}):
    fields = []
    MAPPING = {
        "object": "String",
        "int64": "Int64",
        "uint8": "UInt8",
        "float64": "Float64",
        "datetime64[ns]": "DateTime64",
        "datetime64[ns, UTC]": "DateTime64",
    }

    for column, dtype in df.dtypes.items():
        fields.append((column, override.get(column, MAPPING[dtype.name])))

    return fields


class ClickhouseIOManager(ConfigurableIOManager):
    def handle_output(self, context, df: DataFrame):
        asset_key = context.asset_key.path[-1]
        columns = MAP_TABLE_COLUMNS[asset_key]

        client = Client(host="localhost")

        if asset_key == "line_changes":
            client.execute(
                "INSERT INTO raw_github_metrics.line_changes SELECT * FROM s3('https://datasets-documentation.s3.amazonaws.com/github/commits/clickhouse/line_changes.tsv.xz', 'TSV', 'sign Int8, line_number_old UInt32, line_number_new UInt32, hunk_num UInt32, hunk_start_line_number_old UInt32, hunk_start_line_number_new UInt32, hunk_lines_added UInt32, hunk_lines_deleted UInt32, hunk_context LowCardinality(String), line LowCardinality(String), indent UInt8, line_type String, prev_commit_hash String, prev_author LowCardinality(String), prev_time DateTime, file_change_type String, path LowCardinality(String), old_path LowCardinality(String), file_extension LowCardinality(String), file_lines_added UInt32, file_lines_deleted UInt32, file_hunks_added UInt32, file_hunks_removed UInt32, file_hunks_changed UInt32, commit_hash String, author LowCardinality(String), time DateTime, commit_message String, commit_files_added UInt32, commit_files_deleted UInt32, commit_files_renamed UInt32, commit_files_modified UInt32, commit_lines_added UInt32, commit_lines_deleted UInt32, commit_hunks_added UInt32, commit_hunks_removed UInt32, commit_hunks_changed UInt32')"
            )

            return

        for col in df.select_dtypes([bool]):
            df[col] = df[col].astype("uint8")

        fields = convert_fields(df, {})
        model = MyModel.create_ad_hoc_model(fields, asset_key)
        model.engine = MergeTree(partition_key=["time"])

        try:
            model_instances = []
            for _, row in df.iterrows():
                new_dict = {}
                for index, col in enumerate(columns):
                    test_dict = row.to_list()

                    new_dict[col] = (
                        "nan" if test_dict[index] == "nan" else test_dict[index]
                    )

                model_instances.append(new_dict)

            new_data_frame = pd.DataFrame.from_records(model_instances)

            query = f"INSERT INTO raw_github_metrics.{asset_key} ({','.join(columns)}) VALUES"

            print(query)

            client.insert_dataframe(
                query,
                new_data_frame,
                settings=dict(use_numpy=True),
            )
        except Exception as e:
            raise e

        print("++++++++++++++++++++++++Success++++++++++++++++++++++++")

    def load_input(self, context: InputContext):
        pass
