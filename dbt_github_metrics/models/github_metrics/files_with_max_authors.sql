WITH current_files AS
(
    SELECT path
    FROM
    (
        SELECT
            old_path AS path,
            max(time) AS last_time,
            2 AS change_type
        FROM {{ source('raw_data', 'file_changes')}}
        GROUP BY old_path
        UNION ALL
        SELECT
            path,
            max(time) AS last_time,
            argMax(cast(change_type as UInt32), time) AS change_type
        FROM {{ source('raw_data', 'file_changes')}}
        GROUP BY path
    )
    GROUP BY path
    HAVING (argMax(cast(change_type as UInt32), last_time) != 2) AND (NOT match(path, '(^dbms/)|(^libs/)|(^tests/testflows/)|(^programs/server/store/)'))
    ORDER BY path ASC
)
SELECT
    path,
    uniq(author) AS num_authors
FROM {{ source('raw_data', 'file_changes')}}
WHERE path IN (current_files)
GROUP BY path
ORDER BY num_authors DESC