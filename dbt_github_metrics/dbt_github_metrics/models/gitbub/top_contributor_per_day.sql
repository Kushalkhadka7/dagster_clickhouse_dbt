WITH top_contributor AS (
    SELECT
        top_author.day_of_week,
        top_author.author,
        top_author.author_work / all_work.total_work AS top_author_percent
    FROM
    (
        SELECT * FROM {{ ref('author_work_per_day')}}
    ) AS top_author
    INNER JOIN
    (
        SELECT
            day_of_week,
            sum(lines_added) + sum(lines_deleted) AS total_work
        FROM {{source('source_git', 'file_changes')}}
        WHERE time > (now() - toIntervalYear(1))
        GROUP BY dayOfWeek(time) AS day_of_week
    ) AS all_work USING (day_of_week)
)
SELECT * FROM top_contributor