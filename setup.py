import glob

from setuptools import find_packages, setup

setup(
    name="dagster_github_metrics",
    packages=find_packages(exclude=["dagster_github_metrics_tests"]),
    # package data paths are relative to the package key
    package_data={
        "dagster_github_metrics": [
            "../" + path for path in glob.glob("dbt_github_metrics/**", recursive=True)
        ]
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "dagster-dbt",
        "dbt-clickhouse",
        "pandas",
        "numpy",
        "scipy",
        "dbt-core",
        "dbt-duckdb",
        "dagster-duckdb",
        "dagster-duckdb-pandas",
        "infi.clickhouse_orm",
        "clickhouse-connect",
        "pandahouse",
        # packaging v22 has build compatibility issues with dbt as of 2022-12-07
        "packaging<22.0",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
