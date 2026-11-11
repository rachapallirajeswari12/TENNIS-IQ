
-- TENNIS IQ PROJECT
-- MEMBER 3: SQL ANALYSIS QUERIES
-- Database: PostgreSQL

-- 1. Total records in all six tables
SELECT 'categories' AS table_name, COUNT(*) AS total_records FROM categories
UNION ALL
SELECT 'competitions', COUNT(*) FROM competitions
UNION ALL
SELECT 'complexes', COUNT(*) FROM complexes
UNION ALL
SELECT 'venues', COUNT(*) FROM venues
UNION ALL
SELECT 'competitor', COUNT(*) FROM competitor
UNION ALL
SELECT 'competitor_rankings', COUNT(*) FROM competitor_rankings;


-- 2. Competitions grouped by category
SELECT
    category_id,
    COUNT(*) AS total_competitions
FROM competitions
GROUP BY category_id
ORDER BY total_competitions DESC;


-- 3. Venues grouped by country
SELECT
    country_name,
    COUNT(*) AS total_venues
FROM venues
GROUP BY country_name
ORDER BY total_venues DESC;


-- 4. Venues in each complex
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
LEFT JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY c.complex_id, c.complex_name
ORDER BY total_venues DESC;


-- 5. Competitors grouped by country
SELECT
    country,
    COUNT(*) AS total_competitors
FROM competitor
GROUP BY country
ORDER BY total_competitors DESC;


-- 6. Ranking records by gender
SELECT
    gender,
    COUNT(*) AS total_players
FROM competitor_rankings
GROUP BY gender
ORDER BY total_players DESC;


-- 7. Ranking points analysis
SELECT
    MIN(points) AS minimum_points,
    MAX(points) AS maximum_points,
    ROUND(AVG(points), 2) AS average_points
FROM competitor_rankings;


-- 8. Top 10 ranked competitors by points
SELECT
    c.name,
    c.country,
    r.rank,
    r.points,
    r.movement,
    r.gender
FROM competitor c
JOIN competitor_rankings r
    ON c.competitor_id = r.competitor_id
ORDER BY r.points DESC
LIMIT 10;


-- 9. Ranking movement analysis
SELECT
    CASE
        WHEN movement > 0 THEN 'Rank Improved'
        WHEN movement < 0 THEN 'Rank Dropped'
        ELSE 'No Change'
    END AS movement_status,
    COUNT(*) AS total_players
FROM competitor_rankings
GROUP BY movement_status
ORDER BY total_players DESC;


-- 10. Latest ranking information
SELECT
    ranking_year,
    ranking_week,
    gender,
    COUNT(*) AS total_players
FROM competitor_rankings
GROUP BY ranking_year, ranking_week, gender
ORDER BY ranking_year DESC, ranking_week DESC, gender;
