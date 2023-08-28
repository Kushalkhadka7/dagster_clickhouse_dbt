WITH current_files AS
    (
        SELECT path
        FROM
        (
            SELECT
                old_path AS path,
                max(time) AS last_time,
                2 AS change_type
            FROM {{ source('source_git', 'file_changes')}}
            GROUP BY old_path
            UNION ALL
            SELECT
                path,
                max(time) AS last_time,
                argMax(change_type, time) AS change_type
            FROM {{ source('source_git', 'file_changes')}}
            GROUP BY path
        )
        GROUP BY path
        HAVING (argMax(change_type, last_time) != 2) AND (NOT match(path, '(^dbms/)|(^libs/)|(^tests/testflows/)|(^programs/server/store/)'))
        ORDER BY path ASC
    )
SELECT
    count() AS c,
    path,
    max(time) AS latest_change
FROM {{ source('source_git', 'file_changes')}}
WHERE path IN (current_files)
GROUP BY path
ORDER BY c DESC