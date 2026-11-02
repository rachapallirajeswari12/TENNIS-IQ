
import streamlit as st
import pandas as pd
import psycopg2

# =========================================================
# TENNIS IQ - SPORTS ANALYTICS PLATFORM
# Python | Streamlit | PostgreSQL | Sportradar API
# =========================================================

st.set_page_config(
    page_title="TENNIS IQ | Sports Analytics",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------- DESIGN --------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#071522,#0b2030,#102b35);
    color: #f4f7f8;
}
[data-testid="stSidebar"] {
    background: #081923;
    border-right: 1px solid #31514d;
}
[data-testid="stSidebar"] * { color: #edf7f4; }
h1,h2,h3 { color: #f4f8f7 !important; }
.brand {
    font-size: 32px;
    font-weight: 900;
    color: #b7f34a;
    letter-spacing: 2px;
}
.subbrand {
    color: #9fb9bd;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
}
.hero {
    background: linear-gradient(110deg,#102c38,#17453e);
    border: 1px solid #3b665b;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 22px;
}
.hero-title {
    font-size: 29px;
    font-weight: 900;
    color: #c4f56b;
}
.hero-sub {
    color: #d2e2df;
    font-size: 12px;
    letter-spacing: 1.5px;
}
div[data-testid="stMetric"] {
    background: #102b37;
    border: 1px solid #28504e;
    padding: 15px;
    border-radius: 13px;
}
div[data-testid="stMetricLabel"] { color: #b5ccca !important; }
div[data-testid="stMetricValue"] { color: #c4f56b !important; }
.section-label {
    color: #bdf45e;
    font-weight: 800;
    letter-spacing: 1px;
    padding-bottom: 7px;
    border-bottom: 1px solid #31514d;
}
.footer {
    text-align: center;
    color: #91aaa9;
    padding: 25px 5px 10px 5px;
    font-size: 12px;
}
div.stButton > button {
    background: #b7ef50;
    color: #10251f;
    border: none;
    border-radius: 9px;
    font-weight: 800;
}
div.stButton > button:hover {
    background: #d0ff70;
    color: #10251f;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE ----------------------

for key, value in {
    "db_config": None,
    "connected": False,
    "connection_message": "",
    "connection_error": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- DATABASE FUNCTIONS --------------------

def get_connection(config=None):
    config = config or st.session_state.db_config
    if not config:
        raise ValueError("Please connect to PostgreSQL first.")

    return psycopg2.connect(
        host=config["host"],
        port=config["port"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        connect_timeout=5
    )


def fetch_data(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if cursor.description is None:
                return pd.DataFrame()
            columns = [item[0] for item in cursor.description]
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()


def get_count(query, params=None):
    data = fetch_data(query, params)
    return int(data.iloc[0, 0]) if not data.empty else 0


def get_options(query, params=None):
    data = fetch_data(query, params)
    if data.empty:
        return []
    return [
        str(x) for x in data.iloc[:, 0].dropna().tolist()
        if str(x).strip()
    ]


def csv_data(data):
    return data.to_csv(index=False).encode("utf-8-sig")


def show_download(data, filename, label="⬇️ Download CSV"):
    st.download_button(
        label=label,
        data=csv_data(data),
        file_name=filename,
        mime="text/csv"
    )


def make_where(conditions):
    return " WHERE " + " AND ".join(conditions) if conditions else ""


# ---------------------- SIDEBAR --------------------------

with st.sidebar:
    st.markdown('<div class="brand">🎾 TENNIS IQ</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="subbrand">SPORTS ANALYTICS PLATFORM</div>',
                unsafe_allow_html=True)
    st.divider()

    st.markdown("### 🔌 PostgreSQL Connection")

    with st.form("database_connection"):
        db_host = st.text_input("Host", "localhost")
        db_port = st.text_input("Port", "5432")
        db_name = st.text_input("Database", "tennis_analytics")
        db_user = st.text_input("Username", "postgres")
        db_password = st.text_input("Password", type="password")
        connect_button = st.form_submit_button(
            "Connect to Database",
            use_container_width=True
        )

    if connect_button:
        config = {
            "host": db_host,
            "port": db_port,
            "database": db_name,
            "user": db_user,
            "password": db_password
        }
        try:
            test_conn = get_connection(config)
            test_conn.close()
            st.session_state.db_config = config
            st.session_state.connected = True
            st.session_state.connection_message = "Database Connected Successfully!"
            st.session_state.connection_error = ""
        except Exception as error:
            st.session_state.connected = False
            st.session_state.connection_message = ""
            st.session_state.connection_error = str(error)

    if st.session_state.connection_message:
        st.success(st.session_state.connection_message)

    if st.session_state.connection_error:
        st.error(st.session_state.connection_error)

    st.divider()
    st.markdown("### 📍 NAVIGATION")

    page = st.radio(
        "Select Page",
        [
            "🏠 Overview",
            "🏆 Competition Analysis",
            "🌍 Venue Analysis",
            "👤 Doubles Player Rankings",
            "📊 SQL Insights",
            "🔍 Data Quality",
            "🗄️ Database Explorer"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### 📁 PROJECT")
    st.markdown("**Game Analytics**")
    st.caption("Unlocking Tennis Data with Sportradar API")
    st.caption("Python • Streamlit • PostgreSQL")

# ---------------------- MAIN HEADER ----------------------

st.markdown("""
<div class="hero">
  <div class="hero-title">🎾 TENNIS ANALYTICS</div>
  <div class="hero-sub">
    SPORTS INTELLIGENCE | COMPETITIONS | VENUES | PLAYER RANKINGS
  </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.connected:
    st.warning("Connect to PostgreSQL using the sidebar to open the dashboard.")
    st.stop()

# -------------------- TABLE DEFINITIONS ------------------

TABLES = [
    "categories",
    "competitions",
    "complexes",
    "venues",
    "competitor",
    "competitor_rankings"
]

# =========================================================
# 1. OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.title("🏠 Tournament Intelligence Overview")
    st.caption("Global snapshot of tennis competitions, venues and doubles rankings.")

    try:
        counts = {
            "Categories": get_count("SELECT COUNT(*) FROM categories"),
            "Competitions": get_count("SELECT COUNT(*) FROM competitions"),
            "Complexes": get_count("SELECT COUNT(*) FROM complexes"),
            "Venues": get_count("SELECT COUNT(*) FROM venues"),
            "Competitors": get_count("SELECT COUNT(*) FROM competitor"),
            "Competitor Rankings": get_count("SELECT COUNT(*) FROM competitor_rankings")
        }

        total_countries = get_count("""
            SELECT COUNT(DISTINCT country)
            FROM competitor
            WHERE country IS NOT NULL
        """)

        highest_points = get_count("""
            SELECT COALESCE(MAX(points),0)
            FROM competitor_rankings
        """)

        c1, c2, c3 = st.columns(3)
        c1.metric("🏆 Competitions", f"{counts['Competitions']:,}")
        c2.metric("👥 Competitors", f"{counts['Competitors']:,}")
        c3.metric("🌍 Player Countries", f"{total_countries:,}")

        c4, c5, c6 = st.columns(3)
        c4.metric("🎾 Categories", f"{counts['Categories']:,}")
        c5.metric("📍 Venues", f"{counts['Venues']:,}")
        c6.metric("⭐ Highest Points", f"{highest_points:,}")

        st.divider()
        left, right = st.columns(2)

        with left:
            st.markdown("### 🏆 Competitions by Category")
            category_data = fetch_data("""
                SELECT COALESCE(c.category_name,'Unknown') AS category,
                       COUNT(*) AS total
                FROM competitions co
                LEFT JOIN categories c
                  ON co.category_id = c.category_id
                GROUP BY c.category_name
                ORDER BY total DESC
            """)
            if not category_data.empty:
                st.bar_chart(category_data.set_index("category")["total"])

        with right:
            st.markdown("### 🌍 Top Countries by Competitors")
            country_data = fetch_data("""
                SELECT country, COUNT(*) AS total
                FROM competitor
                WHERE country IS NOT NULL
                GROUP BY country
                ORDER BY total DESC
                LIMIT 10
            """)
            if not country_data.empty:
                st.bar_chart(country_data.set_index("country")["total"])

        st.divider()
        st.markdown("### 📊 Complete Database Summary")
        summary = pd.DataFrame(
            [{"Table Name": name, "Records": value}
             for name, value in counts.items()]
        )
        st.dataframe(summary, use_container_width=True, hide_index=True)
        show_download(summary, "tennis_database_summary.csv")

    except Exception as error:
        st.error(f"Overview error: {error}")

# =========================================================
# 2. COMPETITION ANALYSIS
# =========================================================

elif page == "🏆 Competition Analysis":

    st.title("🏆 Competition Analysis")
    st.caption("Explore competitions by name, category, gender and event type.")

    try:
        categories = ["All"] + get_options("""
            SELECT DISTINCT category_name
            FROM categories
            WHERE category_name IS NOT NULL
            ORDER BY category_name
        """)

        genders = ["All"] + get_options("""
            SELECT DISTINCT gender
            FROM competitions
            WHERE gender IS NOT NULL AND gender <> ''
            ORDER BY gender
        """)

        event_types = ["All"] + get_options("""
            SELECT DISTINCT type
            FROM competitions
            WHERE type IS NOT NULL AND type <> ''
            ORDER BY type
        """)

        competition_names = ["All"] + get_options("""
            SELECT DISTINCT competition_name
            FROM competitions
            WHERE competition_name IS NOT NULL
            ORDER BY competition_name
        """)

        f1, f2 = st.columns(2)
        category = f1.selectbox("🎾 Category", categories)
        gender = f2.selectbox("👤 Gender", genders)

        f3, f4 = st.columns(2)
        event_type = f3.selectbox("🏆 Event Type", event_types)
        competition_name = f4.selectbox(
            "🔎 Competition Name",
            competition_names
        )

        conditions = []
        params = []

        if category != "All":
            conditions.append("ca.category_name = %s")
            params.append(category)

        if gender != "All":
            conditions.append("co.gender = %s")
            params.append(gender)

        if event_type != "All":
            conditions.append("co.type = %s")
            params.append(event_type)

        if competition_name != "All":
            conditions.append("co.competition_name = %s")
            params.append(competition_name)

        where = make_where(conditions)

        query = """
            SELECT co.competition_name,
                   COALESCE(ca.category_name,'Unknown') AS category_name,
                   co.gender, co.type, co.parent_id
            FROM competitions co
            LEFT JOIN categories ca
              ON co.category_id = ca.category_id
        """ + where + """
            ORDER BY co.competition_name
        """

        data = fetch_data(query, params)

        st.metric("🏆 Matching Competitions", f"{len(data):,}")
        st.markdown("### 📋 Competition Details")
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
            height=450
        )
        show_download(data, "all_matching_competitions.csv")

        st.divider()
        st.markdown("### 📈 Competition Distribution by Type")
        if not data.empty:
            type_data = (
                data["type"].fillna("Unknown")
                .value_counts()
                .rename_axis("Event Type")
                .to_frame("Competitions")
            )
            st.bar_chart(type_data)

    except Exception as error:
        st.error(f"Competition Analysis error: {error}")

# =========================================================
# 3. VENUE ANALYSIS
# =========================================================

elif page == "🌍 Venue Analysis":

    st.title("🌍 Global Tennis Venue Analysis")
    st.caption("Explore venues, cities, countries, time zones and complexes.")

    try:
        countries = ["All"] + get_options("""
            SELECT DISTINCT country_name
            FROM venues
            WHERE country_name IS NOT NULL
            ORDER BY country_name
        """)

        country = st.selectbox("🌍 Select Country", countries)

        city_query = """
            SELECT DISTINCT city_name
            FROM venues
            WHERE city_name IS NOT NULL
        """
        city_params = []

        if country != "All":
            city_query += " AND country_name = %s"
            city_params.append(country)

        city_query += " ORDER BY city_name"

        cities = ["All"] + get_options(city_query, city_params)
        city = st.selectbox("🏙️ Select City", cities)

        venue_query = """
            SELECT DISTINCT venue_name
            FROM venues
            WHERE venue_name IS NOT NULL
        """
        venue_params = []

        if country != "All":
            venue_query += " AND country_name = %s"
            venue_params.append(country)

        if city != "All":
            venue_query += " AND city_name = %s"
            venue_params.append(city)

        venue_query += " ORDER BY venue_name"

        venue_names = ["All"] + get_options(venue_query, venue_params)
        venue_name = st.selectbox("🎾 Select Venue", venue_names)

        conditions = []
        params = []

        if country != "All":
            conditions.append("v.country_name = %s")
            params.append(country)

        if city != "All":
            conditions.append("v.city_name = %s")
            params.append(city)

        if venue_name != "All":
            conditions.append("v.venue_name = %s")
            params.append(venue_name)

        where = make_where(conditions)

        query = """
            SELECT v.venue_name, v.city_name, v.country_name,
                   v.timezone, cx.complex_name
            FROM venues v
            LEFT JOIN complexes cx
              ON v.complex_id = cx.complex_id
        """ + where + """
            ORDER BY v.country_name, v.city_name, v.venue_name
        """

        data = fetch_data(query, params)

        countries_total = get_count("""
            SELECT COUNT(DISTINCT country_name)
            FROM venues
            WHERE country_name IS NOT NULL
        """)

        a, b = st.columns(2)
        a.metric("📍 Venues Displayed", f"{len(data):,}")
        b.metric("🌍 Countries Available", f"{countries_total:,}")

        st.markdown("### 📋 Venue Details")
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
            height=450
        )
        show_download(data, "tennis_venues.csv")

        st.divider()
        st.markdown("### 📊 Top 10 Countries by Venue Count")

        top = fetch_data("""
            SELECT country_name, COUNT(*) AS venue_count
            FROM venues
            WHERE country_name IS NOT NULL
            GROUP BY country_name
            ORDER BY venue_count DESC
            LIMIT 10
        """)

        if not top.empty:
            st.bar_chart(top.set_index("country_name")["venue_count"])

    except Exception as error:
        st.error(f"Venue Analysis error: {error}")

# =========================================================
# 4. DOUBLES PLAYER RANKINGS
# =========================================================

elif page == "👤 Doubles Player Rankings":

    st.title("👤 Doubles Player Rankings")
    st.caption("Explore doubles player points, ranking position, movement and country.")

    try:
        countries = ["All"] + get_options("""
            SELECT DISTINCT country
            FROM competitor
            WHERE country IS NOT NULL AND country <> ''
            ORDER BY country
        """)

        genders = ["All"] + get_options("""
            SELECT DISTINCT gender
            FROM competitor_rankings
            WHERE gender IS NOT NULL AND gender <> ''
            ORDER BY gender
        """)

        player_names = ["All"] + get_options("""
            SELECT DISTINCT cp.name
            FROM competitor cp
            INNER JOIN competitor_rankings cr
              ON cp.competitor_id = cr.competitor_id
            WHERE cp.name IS NOT NULL
            ORDER BY cp.name
        """)

        f1, f2, f3 = st.columns(3)
        country = f1.selectbox("🌍 Country", countries)
        gender = f2.selectbox("👤 Gender", genders)
        player_name = f3.selectbox("🎾 Player Name", player_names)

        minimum_points = st.slider(
            "Minimum Ranking Points",
            min_value=0,
            max_value=11000,
            value=0,
            step=100
        )

        conditions = ["COALESCE(cr.points,0) >= %s"]
        params = [minimum_points]

        if country != "All":
            conditions.append("cp.country = %s")
            params.append(country)

        if gender != "All":
            conditions.append("cr.gender = %s")
            params.append(gender)

        if player_name != "All":
            conditions.append("cp.name = %s")
            params.append(player_name)

        where = make_where(conditions)

        query = """
            SELECT cp.name AS player_name,
                   cp.country,
                   cr.gender,
                   cr.rank,
                   cr.movement,
                   cr.points,
                   cr.competitions_played
            FROM competitor_rankings cr
            LEFT JOIN competitor cp
              ON cr.competitor_id = cp.competitor_id
        """ + where + """
            ORDER BY cr.points DESC NULLS LAST,
                     cr.rank ASC NULLS LAST
        """

        data = fetch_data(query, params)

        highest = int(data["points"].max()) if (
            not data.empty and data["points"].notna().any()
        ) else 0

        average = float(data["points"].mean()) if (
            not data.empty and data["points"].notna().any()
        ) else 0

        a, b, c = st.columns(3)
        a.metric("👥 Players Displayed", f"{len(data):,}")
        b.metric("⭐ Highest Points", f"{highest:,}")
        c.metric("📊 Average Points", f"{average:,.2f}")

        st.markdown("### 🏅 Player Leaderboard")
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
            height=450
        )
        show_download(data, "doubles_player_rankings.csv")

        st.divider()
        st.markdown("### ⭐ Top 10 Players by Ranking Points")

        if not data.empty:
            chart_data = data.dropna(subset=["points"]).nlargest(10, "points").copy()
            chart_data["player_name"] = chart_data["player_name"].fillna("Unknown")
            chart_data = chart_data.drop_duplicates(
                subset=["player_name"], keep="first"
            )
            if not chart_data.empty:
                st.bar_chart(
                    chart_data.set_index("player_name")["points"]
                )

    except Exception as error:
        st.error(f"Player Rankings error: {error}")

# =========================================================
# 5. SQL INSIGHTS
# =========================================================

elif page == "📊 SQL Insights":

    st.title("📊 SQL Insights")
    st.caption("Explore PostgreSQL analysis using SQL queries and results.")

    sql_queries = {
        "1. Total Records in All Tables": """
            SELECT
              (SELECT COUNT(*) FROM categories) AS categories,
              (SELECT COUNT(*) FROM competitions) AS competitions,
              (SELECT COUNT(*) FROM complexes) AS complexes,
              (SELECT COUNT(*) FROM venues) AS venues,
              (SELECT COUNT(*) FROM competitor) AS competitors,
              (SELECT COUNT(*) FROM competitor_rankings) AS rankings;
        """,

        "2. Competitions by Category - GROUP BY": """
            SELECT c.category_name, COUNT(*) AS total_competitions
            FROM competitions co
            LEFT JOIN categories c ON co.category_id = c.category_id
            GROUP BY c.category_name
            ORDER BY total_competitions DESC;
        """,

        "3. Competitions by Gender": """
            SELECT gender, COUNT(*) AS total_competitions
            FROM competitions
            GROUP BY gender
            ORDER BY total_competitions DESC;
        """,

        "4. Competitions by Event Type": """
            SELECT type, COUNT(*) AS total_competitions
            FROM competitions
            GROUP BY type
            ORDER BY total_competitions DESC;
        """,

        "5. Top 10 Countries by Venue Count": """
            SELECT country_name, COUNT(*) AS total_venues
            FROM venues
            WHERE country_name IS NOT NULL
            GROUP BY country_name
            ORDER BY total_venues DESC
            LIMIT 10;
        """,

        "6. Top 10 Doubles Players": """
            SELECT cp.name, cp.country, cr.gender, cr.rank,
                   cr.points, cr.competitions_played
            FROM competitor_rankings cr
            JOIN competitor cp
              ON cr.competitor_id = cp.competitor_id
            ORDER BY cr.points DESC NULLS LAST
            LIMIT 10;
        """,

        "7. Average Points by Gender": """
            SELECT gender,
                   COUNT(*) AS total_rankings,
                   ROUND(AVG(points),2) AS average_points,
                   MAX(points) AS highest_points
            FROM competitor_rankings
            GROUP BY gender
            ORDER BY average_points DESC;
        """,

        "8. Player Ranking with CTE": """
            WITH PlayerStats AS (
                SELECT cp.name, cp.country, cr.gender,
                       cr.rank, cr.points
                FROM competitor_rankings cr
                JOIN competitor cp
                  ON cr.competitor_id = cp.competitor_id
            )
            SELECT *
            FROM PlayerStats
            ORDER BY points DESC NULLS LAST
            LIMIT 10;
        """,

        "9. Player Ranking with Window Function": """
            SELECT cp.name, cp.country, cr.gender, cr.points,
                   RANK() OVER (ORDER BY cr.points DESC) AS points_rank
            FROM competitor_rankings cr
            JOIN competitor cp
              ON cr.competitor_id = cp.competitor_id
            ORDER BY points_rank
            LIMIT 20;
        """,

        "10. Venue Count by Country": """
            SELECT country_name, COUNT(*) AS venue_count
            FROM venues
            GROUP BY country_name
            ORDER BY venue_count DESC;
        """,

        "11. Competitions with Category - JOIN": """
            SELECT co.competition_name, ca.category_name,
                   co.gender, co.type
            FROM competitions co
            LEFT JOIN categories ca
              ON co.category_id = ca.category_id
            ORDER BY co.competition_name;
        """,

        "12. Venues with Complex Names - JOIN": """
            SELECT v.venue_name, v.city_name, v.country_name,
                   cx.complex_name
            FROM venues v
            LEFT JOIN complexes cx
              ON v.complex_id = cx.complex_id
            ORDER BY v.country_name, v.city_name;
        """
    }

    selected_query = st.selectbox(
        "Select SQL Analysis",
        list(sql_queries.keys())
    )

    st.markdown("### 💻 SQL Query")
    st.code(sql_queries[selected_query], language="sql")

    if st.button("▶ Run SQL Analysis"):
        try:
            result = fetch_data(sql_queries[selected_query])
            st.success(
                f"Query executed successfully. Rows returned: {len(result):,}"
            )
            st.markdown("### 📋 Query Result")
            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )
            show_download(result, "sql_analysis_result.csv")
        except Exception as error:
            st.error(f"SQL query error: {error}")

    st.divider()
    st.markdown("### 🧠 SQL Concepts Used")

    concepts = pd.DataFrame({
        "SQL Concept": [
            "SELECT", "WHERE", "GROUP BY", "ORDER BY",
            "JOIN", "LEFT JOIN", "COUNT", "AVG",
            "MAX", "CTE", "Window Function", "RANK"
        ],
        "Purpose": [
            "Retrieve data",
            "Filter records",
            "Group similar records",
            "Sort query results",
            "Combine related tables",
            "Keep all left-table records",
            "Count records",
            "Calculate average",
            "Find maximum value",
            "Create a temporary named result",
            "Perform calculations across rows",
            "Assign ranking positions"
        ]
    })

    st.dataframe(
        concepts,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# 6. DATA QUALITY
# =========================================================

elif page == "🔍 Data Quality":

    st.title("🔍 Data Quality & Validation")
    st.caption(
        "Inspect NULL values, duplicate primary identifiers "
        "and database constraints."
    )

    try:
        table_choice = st.selectbox("Select Table", TABLES)

        columns_info = fetch_data("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position
        """, [table_choice])

        st.markdown("### 📋 Table Structure")
        st.dataframe(
            columns_info,
            use_container_width=True,
            hide_index=True
        )

        # NULL checks for every column
        null_results = []
        column_names = columns_info["column_name"].tolist()

        for column in column_names:
            safe_column = column.replace('"', '""')
            query = (
                'SELECT COUNT(*) FROM public."'
                + table_choice
                + '" WHERE "'
                + safe_column
                + '" IS NULL'
            )
            null_count = get_count(query)

            null_results.append({
                "Column": column,
                "Missing Values": null_count
            })

        null_df = pd.DataFrame(null_results)

        st.markdown("### 🔎 Missing Values by Column")
        st.dataframe(
            null_df,
            use_container_width=True,
            hide_index=True
        )

        total_missing = int(null_df["Missing Values"].sum()) if not null_df.empty else 0
        st.metric(
            "Total NULL Values in Selected Table",
            f"{total_missing:,}"
        )

        # Primary key and unique constraints
        key_info = fetch_data("""
            SELECT
                kcu.column_name,
                tc.constraint_type,
                tc.constraint_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            WHERE tc.table_schema = 'public'
              AND tc.table_name = %s
              AND tc.constraint_type IN (
                  'PRIMARY KEY','UNIQUE','FOREIGN KEY'
              )
            ORDER BY tc.constraint_type, kcu.column_name
        """, [table_choice])

        st.markdown("### 🔐 Primary Key / Unique / Foreign Key Constraints")

        if key_info.empty:
            st.info("No matching constraints were found for this table.")
        else:
            st.dataframe(
                key_info,
                use_container_width=True,
                hide_index=True
            )

        # Duplicate checks for primary key columns
        primary_keys = key_info[
            key_info["constraint_type"] == "PRIMARY KEY"
        ]["column_name"].tolist() if not key_info.empty else []

        st.markdown("### 🔁 Duplicate Primary Key Validation")

        duplicate_results = []

        for column in primary_keys:
            safe_column = column.replace('"', '""')
            duplicate_query = (
                'SELECT COUNT(*) FROM ('
                'SELECT "' + safe_column + '" '
                'FROM public."' + table_choice + '" '
                'GROUP BY "' + safe_column + '" '
                'HAVING COUNT(*) > 1'
                ') AS duplicate_rows'
            )

            duplicate_count = get_count(duplicate_query)

            duplicate_results.append({
                "Primary Key Column": column,
                "Duplicate Values": duplicate_count,
                "Status": "PASS" if duplicate_count == 0 else "CHECK"
            })

        if duplicate_results:
            duplicate_df = pd.DataFrame(duplicate_results)
            st.dataframe(
                duplicate_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No primary key column is defined for this table.")

        st.caption(
            "NULL values and duplicate checks are reported as observations. "
            "A NULL does not automatically mean the record is invalid."
        )

        show_download(null_df, table_choice + "_null_quality_report.csv")

    except Exception as error:
        st.error(f"Data Quality error: {error}")

# =========================================================
# 7. DATABASE EXPLORER
# =========================================================

elif page == "🗄️ Database Explorer":

    st.title("🗄️ PostgreSQL Database Explorer")
    st.caption("Explore all six project tables and their stored records.")

    try:
        table_choice = st.selectbox("Choose Database Table", TABLES)

        table_count = get_count(
            'SELECT COUNT(*) FROM public."' + table_choice + '"'
        )

        st.metric(
            "Total Records in Selected Table",
            f"{table_count:,}"
        )

        schema = fetch_data("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position
        """, [table_choice])

        st.markdown("### 🧱 Column Information")
        st.dataframe(
            schema,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 📋 Table Records")

        page_size = st.selectbox(
            "Rows per page",
            [100, 250, 500, 1000],
            index=1
        )

        total_pages = max(
            1,
            (table_count + page_size - 1) // page_size
        )

        selected_page = st.number_input(
            "Page Number",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )

        offset = (selected_page - 1) * page_size

        # Table name is restricted to the TABLES allowlist.
        query = (
            'SELECT * FROM public."'
            + table_choice
            + '" ORDER BY 1 LIMIT %s OFFSET %s'
        )

        table_data = fetch_data(
            query,
            [page_size, offset]
        )

        st.caption(
            f"Showing page {selected_page} of {total_pages} "
            f"| Total records: {table_count:,}"
        )

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True,
            height=450
        )

        show_download(
            table_data,
            table_choice + "_records_page_" + str(selected_page) + ".csv",
            "⬇️ Download Current Page CSV"
        )

    except Exception as error:
        st.error(f"Database Explorer error: {error}")

# ------------------------- FOOTER -------------------------

st.markdown("""
<div class="footer">
  <b>🎾 TENNIS IQ | SPORTS ANALYTICS PLATFORM</b><br>
  Game Analytics: Unlocking Tennis Data with Sportradar API<br>
  Python • Streamlit • PostgreSQL • SQL Analytics
</div>
""", unsafe_allow_html=True)
