
WITH commit_days AS
(
    SELECT
        author,
        day,
        any(day) OVER (PARTITION BY author ORDER BY day ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS previous_commit,
        dateDiff('day', previous_commit, day) AS days_since_last,
        if(days_since_last = 1, 1, 0) AS consecutive_day
    FROM
    (
        SELECT
            author,
            toStartOfDay(time) AS day
        FROM {{ source('source_git', 'commits')}}
        GROUP BY
            author,
            day
        ORDER BY
            author ASC,
            day ASC
    )
)
SELECT
    author,
    arrayMax(arrayMap(x -> length(x), arraySplit(x -> (x = 0), groupArray(consecutive_day)))) - 1 AS max_consecutive_days
FROM commit_days
GROUP BY author
ORDER BY max_consecutive_days DESC
LIMIT 10
