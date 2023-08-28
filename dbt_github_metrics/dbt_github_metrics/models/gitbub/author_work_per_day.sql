WITH author_work AS (
     SELECT
        day_of_week,
        author,
        sum(lines_added) + sum(lines_deleted) AS author_work
    FROM {{ source('source_git', 'file_changes') }}
    WHERE time > (now() - toIntervalYear(1))
    GROUP BY
        author,
        dayOfWeek(time) AS day_of_week
    ORDER BY
        day_of_week ASC,
        author_work DESC
    LIMIT 1 BY day_of_week
)
SELECT * FROM author_work