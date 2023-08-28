WITH top_author_percent_max_consecutive_days AS (
    SELECT
        author,
        max_consecutive_days,
        top_author_percent,
        day_of_week
    FROM {{ ref('max_consecutive_days') }}
    INNER JOIN {{ ref('top_contributor_per_day') }} using (author)
)
SELECT * FROM top_author_percent_max_consecutive_days