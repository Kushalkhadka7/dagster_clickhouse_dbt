{{ config(materialized='table') }}

WITH current_files AS
    (
        SELECT path
        FROM
        (
            SELECT
                old_path AS path,
                max(time) AS last_time,
                2 AS change_type
            FROM {{ source('source_git', "file_changes") }}
            GROUP BY old_path
            UNION ALL
            SELECT
                path,
                max(time) AS last_time,
                argMax(change_type, time) AS change_type
            FROM {{ source('source_git', "file_changes") }}
            GROUP BY path
        )
        GROUP BY path
        HAVING (argMax(change_type, last_time) != 2) AND (NOT match(path, '(^dbms/)|(^libs/)|(^tests/testflows/)|(^programs/server/store/)'))
        ORDER BY path ASC
    )
SELECT
    any(path) AS file_path,
    line,
    max(time) AS latest_change,
    any(file_change_type)
FROM {{ source('source_git', "line_changes") }}
WHERE path IN (current_files)
GROUP BY line
ORDER BY latest_change ASC