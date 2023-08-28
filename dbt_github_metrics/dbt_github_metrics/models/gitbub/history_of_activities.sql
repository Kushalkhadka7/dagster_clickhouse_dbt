{{ config(materialized='table') }}

WITH history_of_activities AS (
    SELECT
        week,
        sum(lines_added) AS lines_added,
        sum(lines_deleted) AS lines_deleted,
        uniq(commit_hash) AS num_commits,
        uniq(author) AS authors
    FROM {{ source('source_git', 'file_changes')}}
    WHERE path LIKE 'src/Storages%'
    GROUP BY toStartOfWeek(time) AS week
    ORDER BY week ASC
)
SELECT * FROM history_of_activities