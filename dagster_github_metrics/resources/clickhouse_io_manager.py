import pandahouse as ph
import pandas as pd
from clickhouse_driver import Client
# import clickhouse_connect

from pandas import DataFrame, isna
from infi.clickhouse_orm.models import ModelBase
from infi.clickhouse_orm.fields import Int64Field, DateTime64Field, NullableField
from dagster import (
    InputContext,
    ConfigurableIOManager,
)
from infi.clickhouse_orm.engines import MergeTree

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
        # print("nan" if column == "Unnamed: 2" or column == "Unnamed: 3" else column, dtype.name)
        fields.append((column, override.get(column, MAPPING[dtype.name])))

    # print(fields[:-1])

    return fields


class ClickhouseIOManager(ConfigurableIOManager):
    def handle_output(self, context, df: DataFrame):
        print('++=========================================')
        asset_key = context.asset_key.path[-1]
        columns = MAP_TABLE_COLUMNS[asset_key]


        if asset_key == "line_changes":
            print("++++++++++++++++++++++++returned++++++++++++++++++++++++")
            return

        for col in df.select_dtypes([bool]):
            df[col] = df[col].astype("uint8")

        # client = clickhouse_connect.get_client(
        #     host="localhost", username="default", password="default"
        # )

        fields = convert_fields(df, {})

        client = Client(host="localhost")

        model = MyModel.create_ad_hoc_model(fields, asset_key)
        model.engine = MergeTree(partition_key=["time"])

        try:
            model_instances = []
            for _, row in df.iterrows():
                new_dict = {}
                for index, col in enumerate(columns):
                    test_dict = row.to_list()

                    new_dict[col] = "nan" if test_dict[index] == "nan" else test_dict[index]

                model_instances.append(new_dict)

            new_data_frame = pd.DataFrame.from_records(model_instances)

            query = f"INSERT INTO raw_github_metrics.{asset_key} ({','.join(columns)}) VALUES"

            print(query)

            client.insert_dataframe(
                query,
                new_data_frame,
                settings=dict(use_numpy=True),
            )

            # client.execute(f"INSERT INTO raw_github_metrics.{asset_key} VALUES", new_data_frame.to_dict('records'))
        except Exception as e:
            print("______=++++++++++++++++++++++++++", e)

        print("++++++++++++++++++++++++Success++++++++++++++++++++++++")

    def load_input(self, context: InputContext):
        pass
