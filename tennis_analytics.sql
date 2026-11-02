-- =====================================================
-- GAME ANALYTICS: UNLOCKING TENNIS DATA WITH SPORTRADAR
-- PostgreSQL
-- =====================================================

-- 1. DATABASE TABLES

CREATE TABLE categories(
category_id VARCHAR(50) PRIMARY KEY,
category_name VARCHAR(100)
);

CREATE TABLE competitions(
competition_id VARCHAR(50) PRIMARY KEY,
competition_name VARCHAR(100),
parent_id VARCHAR(50),
type VARCHAR(20),
gender VARCHAR(10),
category_id VARCHAR(50),
FOREIGN KEY (category_id)
REFERENCES categories(category_id)
);

CREATE TABLE complexes(
complex_id VARCHAR(50) PRIMARY KEY,
complex_name VARCHAR(100)
);

CREATE TABLE venues(
venue_id VARCHAR(50) PRIMARY KEY,
venue_name VARCHAR(100),
city_name VARCHAR(100),
country_name VARCHAR(100),
country_code CHAR(3),
timezone VARCHAR(100),
complex_id VARCHAR(50),
FOREIGN KEY(complex_id)
REFERENCES complexes(complex_id)
);

CREATE TABLE competitor(
competitor_id VARCHAR(50) PRIMARY KEY,
name VARCHAR(150),
country VARCHAR(100),
country_code CHAR(10),
abbreviation VARCHAR(20)
);

CREATE TABLE competitor_rankings(
rank_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
rank INT NOT NULL,
movement INT NOT NULL,
points INT NOT NULL,
competitions_played INT NOT NULL,
competitor_id VARCHAR(50),
FOREIGN KEY (competitor_id)
REFERENCES competitor(competitor_id)
);

-- 2. ADD RANKING METADATA COLUMNS

ALTER TABLE competitor_rankings
ADD COLUMN IF NOT EXISTS type_id INT,
ADD COLUMN IF NOT EXISTS ranking_name VARCHAR(50),
ADD COLUMN IF NOT EXISTS ranking_year INT,
ADD COLUMN IF NOT EXISTS ranking_week INT,
ADD COLUMN IF NOT EXISTS gender VARCHAR(10);

-- 3. VERIFY TABLES

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN(
'categories',
'competitions',
'complexes',
'venues',
'competitor',
'competitor_rankings'
)
ORDER BY table_name;

-- 4. VERIFY FOREIGN KEYS

SELECT 
tc.table_name,
kcu.column_name,
ccu.table_name AS referenced_table,
ccu.column_name AS referenced_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
ON tc.constraint_name = kcu.constraint_name
AND tc.constraint_schema = kcu.constraint_schema
JOIN information_schema.constraint_column_usage AS ccu
ON ccu.constraint_name = tc.constraint_name
AND ccu.constraint_schema = tc.constraint_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public';

-- 5. VERIFY TABLE COLUMNS

SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN (
      'categories',
      'competitions',
      'complexes',
      'venues',
      'competitor',
      'competitor_rankings'
  )
ORDER BY table_name, ordinal_position;

-- 6. RECORD COUNT

SELECT 'categories' AS table_name, COUNT(*) AS total_records
FROM categories

UNION ALL

SELECT 'competitions', COUNT(*)
FROM competitions

UNION ALL

SELECT 'complexes', COUNT(*)
FROM complexes

UNION ALL

SELECT 'venues', COUNT(*)
FROM venues

UNION ALL

SELECT 'competitor', COUNT(*)
FROM competitor

UNION ALL

SELECT 'competitor_rankings', COUNT(*)
FROM competitor_rankings;

-- 7.Data Quality Checks

SELECT category_id, COUNT(*)
FROM categories
GROUP BY category_id
HAVING COUNT(*) > 1;

-- Competitions with missing categories

SELECT COUNT(*) AS missing_category_references
FROM competitions c
LEFT JOIN categories ca
    ON c.category_id = ca.category_id
WHERE ca.category_id IS NULL;

-- Venues with missing complexes

SELECT COUNT(*) AS missing_complex_references
FROM venues v
LEFT JOIN complexes c
    ON v.complex_id = c.complex_id
WHERE c.complex_id IS NULL;

-- Rankings with missing competitors

SELECT COUNT(*) AS missing_competitor_references
FROM competitor_rankings cr
LEFT JOIN competitor c
    ON cr.competitor_id = c.competitor_id
WHERE c.competitor_id IS NULL;

-- Ranking points range

SELECT
    MIN(points) AS minimum_points,
    MAX(points) AS maximum_points,
    ROUND(AVG(points), 2) AS average_points
FROM competitor_rankings;

-- 8. COMPETITIONS ANALYSIS

-- Query 1: Total competitions

SELECT COUNT(*) AS total_competitions
FROM competitions;

-- Query 2: All competitions with category names

SELECT
    c.competition_id,
    c.competition_name,
    ca.category_name,
    c.type,
    c.gender
FROM competitions c
JOIN categories ca
    ON c.category_id = ca.category_id
ORDER BY c.competition_name;


-- Query 3: Number of competitions per category

SELECT
    ca.category_name,
    COUNT(c.competition_id) AS total_competitions
FROM categories ca
JOIN competitions c
    ON ca.category_id = c.category_id
GROUP BY ca.category_name
ORDER BY total_competitions DESC;

-- Query 4: Find all doubles competitions

SELECT
    competition_name,
    type,
    gender
FROM competitions
WHERE LOWER(type) LIKE '%doubles%'
ORDER BY competition_name;


-- Query 5: Competitions for ITF Men category

SELECT
    c.competition_name,
    ca.category_name,
    c.gender,
    c.type
FROM competitions c
JOIN categories ca
    ON c.category_id = ca.category_id
WHERE ca.category_name = 'ITF Men'
ORDER BY c.competition_name;


-- Query 6: Parent competitions and sub-competitions

SELECT
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM competitions child
JOIN competitions parent
    ON child.parent_id = parent.competition_id
ORDER BY parent.competition_name;


-- Query 7: Competition type distribution by category

SELECT
    ca.category_name,
    c.type,
    COUNT(*) AS total_competitions
FROM competitions c
JOIN categories ca
    ON c.category_id = ca.category_id
GROUP BY ca.category_name, c.type
ORDER BY ca.category_name, total_competitions DESC;


-- Query 8: Top-level competitions (no parent)

SELECT
    competition_id,
    competition_name,
    type,
    gender
FROM competitions
WHERE parent_id IS NULL
ORDER BY competition_name;


-- Additional competition analysis

SELECT
    gender,
    COUNT(*) AS total_competitions
FROM competitions
GROUP BY gender
ORDER BY total_competitions DESC;


SELECT
    type,
    COUNT(*) AS total_competitions
FROM competitions
GROUP BY type
ORDER BY total_competitions DESC;


SELECT
    c.competition_name,
    ca.category_name,
    c.gender,
    c.type
FROM competitions c
JOIN categories ca
    ON c.category_id = ca.category_id
ORDER BY c.competition_name
LIMIT 10;


-- =====================================================
-- 9. COMPLEXES AND VENUES ANALYSIS
-- =====================================================

-- Query 9: List venues with complex names

SELECT
    v.venue_name,
    v.city_name,
    v.country_name,
    c.complex_name
FROM venues v
JOIN complexes c
    ON v.complex_id = c.complex_id
ORDER BY c.complex_name;


-- Query 10: Count venues per complex

SELECT
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
LEFT JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY c.complex_name
ORDER BY total_venues DESC;


-- Query 11: Venues in Chile

SELECT
    venue_name,
    city_name,
    country_name
FROM venues
WHERE country_name = 'Chile'
ORDER BY city_name;


-- Query 12: Venues and timezones

SELECT
    venue_name,
    city_name,
    country_name,
    timezone
FROM venues
ORDER BY country_name, city_name;


-- Query 13: Complexes having more than one venue

SELECT
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY c.complex_id, c.complex_name
HAVING COUNT(v.venue_id) > 1
ORDER BY total_venues DESC;


-- Query 14: Venues grouped by country

SELECT
    country_name,
    COUNT(*) AS total_venues
FROM venues
GROUP BY country_name
ORDER BY total_venues DESC;


-- Query 15: Venues for a complex named Nacional

SELECT
    c.complex_name,
    v.venue_name,
    v.city_name,
    v.country_name
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
WHERE c.complex_name ILIKE '%Nacional%'
ORDER BY v.venue_name;


-- Additional venue analysis

SELECT
    country_name,
    COUNT(*) AS total_venues
FROM venues
GROUP BY country_name
ORDER BY total_venues DESC
LIMIT 10;


SELECT
    v.country_name,
    COUNT(DISTINCT c.complex_id) AS total_complexes
FROM complexes c
JOIN venues v
    ON c.complex_id = v.complex_id
GROUP BY v.country_name
ORDER BY total_complexes DESC
LIMIT 10;


-- =====================================================
-- 10. COMPETITOR RANKINGS ANALYSIS
-- =====================================================

-- Query 16: Competitors with rank and points

SELECT
    c.name,
    c.country,
    cr.rank,
    cr.points,
    cr.movement,
    cr.competitions_played
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
ORDER BY cr.rank;


-- Query 17: Top 5 competitors by rank

SELECT
    c.name,
    c.country,
    cr.rank,
    cr.points
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE cr.rank <= 5
ORDER BY cr.rank, c.name;


-- Query 18: Competitors with no rank movement

SELECT
    c.name,
    c.country,
    cr.rank,
    cr.movement
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE cr.movement = 0
ORDER BY cr.rank;


-- Query 19: Total points of competitors from Croatia

SELECT
    c.country,
    SUM(cr.points) AS total_points
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;


-- Query 20: Count competitors per country

SELECT
    country,
    COUNT(*) AS total_competitors
FROM competitor
GROUP BY country
ORDER BY total_competitors DESC;


-- Query 21: Highest points in the latest available ranking week

SELECT
    c.name,
    c.country,
    cr.rank,
    cr.points,
    cr.ranking_year,
    cr.ranking_week
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
WHERE (cr.ranking_year, cr.ranking_week) = (
    SELECT ranking_year, ranking_week
    FROM competitor_rankings
    WHERE ranking_year IS NOT NULL
      AND ranking_week IS NOT NULL
    ORDER BY ranking_year DESC, ranking_week DESC
    LIMIT 1
)
ORDER BY cr.points DESC
LIMIT 10;


-- =====================================================
-- 11. ADDITIONAL RANKING ANALYSIS
-- =====================================================

-- Top 10 competitors by ranking points

SELECT
    c.name,
    c.country,
    cr.rank,
    cr.points
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
ORDER BY cr.points DESC
LIMIT 10;


-- Highest ranking points by country

SELECT
    c.country,
    MAX(cr.points) AS highest_points
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
GROUP BY c.country
ORDER BY highest_points DESC
LIMIT 10;


-- Average ranking points by country

SELECT
    c.country,
    ROUND(AVG(cr.points), 2) AS average_points
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
GROUP BY c.country
ORDER BY average_points DESC
LIMIT 10;


-- Number of competitors by country

SELECT
    country,
    COUNT(*) AS total_competitors
FROM competitor
GROUP BY country
ORDER BY total_competitors DESC
LIMIT 10;


-- Zero movement records

SELECT COUNT(*) AS zero_movement_records
FROM competitor_rankings
WHERE movement = 0;


-- Positive movement records

SELECT COUNT(*) AS positive_movement_records
FROM competitor_rankings
WHERE movement > 0;


-- Negative movement records

SELECT COUNT(*) AS negative_movement_records
FROM competitor_rankings
WHERE movement < 0;


-- Top 10 competitors by competitions played

SELECT
    c.name,
    c.country,
    cr.competitions_played
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
ORDER BY cr.competitions_played DESC
LIMIT 10;


-- Average competitions played by country

SELECT
    c.country,
    ROUND(AVG(cr.competitions_played), 2) AS average_competitions
FROM competitor c
JOIN competitor_rankings cr
    ON c.competitor_id = cr.competitor_id
GROUP BY c.country
ORDER BY average_competitions DESC
LIMIT 10;


-- Ranking distribution by gender

SELECT
    gender,
    COUNT(*) AS total_rankings,
    ROUND(AVG(points), 2) AS average_points
FROM competitor_rankings
GROUP BY gender
ORDER BY total_rankings DESC;


-- Highest and lowest ranking points

SELECT
    MAX(points) AS highest_points,
    MIN(points) AS lowest_points,
    ROUND(AVG(points), 2) AS average_points
FROM competitor_rankings;


-- Top 5 competitors in each gender
-- RANK handles tied points

SELECT
    gender,
    player_name,
    country,
    points,
    player_rank
FROM (
    SELECT
        cr.gender,
        c.name AS player_name,
        c.country,
        cr.points,
        cr.rank AS player_rank,
        RANK() OVER (
            PARTITION BY cr.gender
            ORDER BY cr.points DESC
        ) AS row_num
    FROM competitor c
    JOIN competitor_rankings cr
        ON c.competitor_id = cr.competitor_id
) ranking_data
WHERE row_num <= 5
ORDER BY gender, row_num, player_name;

-- =====================================================
-- END OF SQL SCRIPT
-- =====================================================

