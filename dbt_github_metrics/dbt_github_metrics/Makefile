virtualenv:
	@virtualenv dbt-github-metrics
	@source dbt-github-metrics/bin/activate
	@pip install dbt-clickhouse
	@cp -r profiles.yml /home/kushal/.dbt/

dbt-debug:
	@dbt debug && cd ..

dbt-run: dbt-debug
	@dbt run

dbt-generate-docs:
	@dbt docs generate

dbt-serve-docs:
	@dbt docs serve --port 4000