# TENNIS IQ - Member 4 SQL Query Library

SQL_QUERIES = {

    "01 - Total Records by Table": """
        SELECT
            table_name,
            (xpath(
                '/row/cnt/text()',
                query_to_xml(
                    format(
                        'SELECT COUNT(*) AS cnt FROM %I.%I',
                        table_schema,
                        table_name
                    ),
                    false,
                    true,
                    ''
                )
            ))[1]::text::bigint AS total_records
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY total_records DESC;
    """,

    "02 - Competition Type Distribution": """
        SELECT
            type,
            COUNT(*) AS total_competitions
        FROM competitions
        GROUP BY type
        ORDER BY total_competitions DESC;
    """,

    "03 - Gender-wise Competition Analysis": """
        SELECT
            gender,
            COUNT(*) AS total_competitions
        FROM competitions
        GROUP BY gender
        ORDER BY total_competitions DESC;
    """,

    "04 - Category-wise Competition Analysis": """
        SELECT
            c.category_name,
            COUNT(co.competition_id) AS total_competitions
        FROM categories c
        LEFT JOIN competitions co
            ON c.category_id = co.category_id
        GROUP BY c.category_name
        ORDER BY total_competitions DESC;
    """,

    "05 - Top 10 Countries by Venues": """
        SELECT
            country_name,
            COUNT(*) AS total_venues
        FROM venues
        GROUP BY country_name
        ORDER BY total_venues DESC
        LIMIT 10;
    """,

    "06 - Top 10 Cities by Venues": """
        SELECT
            city_name,
            COUNT(*) AS total_venues
        FROM venues
        GROUP BY city_name
        ORDER BY total_venues DESC
        LIMIT 10;
    """,

    "07 - Venues by Complex": """
        SELECT
            c.complex_name,
            COUNT(v.venue_id) AS total_venues
        FROM complexes c
        LEFT JOIN venues v
            ON c.complex_id = v.complex_id
        GROUP BY c.complex_name
        ORDER BY total_venues DESC
        LIMIT 15;
    """,

    "08 - Top 10 Players by Ranking Points": """
        SELECT
            p.name,
            p.country,
            r.rank,
            r.points
        FROM competitor_rankings r
        INNER JOIN competitor p
            ON r.competitor_id = p.competitor_id
        ORDER BY r.points DESC
        LIMIT 10;
    """,

    "09 - Player Ranking Distribution": """
        SELECT
            CASE
                WHEN rank <= 10 THEN 'Top 10'
                WHEN rank <= 50 THEN '11-50'
                WHEN rank <= 100 THEN '51-100'
                ELSE 'Above 100'
            END AS ranking_group,
            COUNT(*) AS total_players
        FROM competitor_rankings
        GROUP BY ranking_group
        ORDER BY MIN(rank);
    """,

    "10 - Country-wise Ranked Players": """
        SELECT
            p.country,
            COUNT(*) AS total_players
        FROM competitor_rankings r
        INNER JOIN competitor p
            ON r.competitor_id = p.competitor_id
        GROUP BY p.country
        ORDER BY total_players DESC
        LIMIT 15;
    """,

    "11 - Average Ranking Points": """
        SELECT
            AVG(points) AS average_points,
            MAX(points) AS highest_points,
            MIN(points) AS lowest_points
        FROM competitor_rankings;
    """,

    "12 - Ranking Movement Distribution": """
        SELECT
            movement,
            COUNT(*) AS total_players
        FROM competitor_rankings
        GROUP BY movement
        ORDER BY total_players DESC;
    """

}
