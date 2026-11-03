# ============================================================
# 🎾 TENNIS IQ - SPORTS ANALYTICS PLATFORM
# Game Analytics: Unlocking Tennis Data with Sportradar API
# Python | Streamlit | PostgreSQL | Supabase | Plotly
# ============================================================

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

from psycopg2 import sql
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TENNIS IQ | Sports Analytics",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM DESIGN - TENNIS IQ
# ============================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #071526 0%,
        #0B1F33 50%,
        #102B3F 100%
    );
    color: #F1F5F9;
}

/* MAIN CONTENT */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* MAIN HEADINGS */

h1 {
    color: #42E8A5 !important;
    font-weight: 800 !important;
}

h2 {
    color: #55D6BE !important;
    font-weight: 700 !important;
}

h3 {
    color: #7DD3FC !important;
    font-weight: 700 !important;
}

/* PARAGRAPH */

p, label, span {
    color: #E2E8F0;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #06111F,
        #102B43,
        #0B3A3A
    );
    border-right: 2px solid #1D8A78;
}

/* SIDEBAR TITLE */

[data-testid="stSidebar"] h1 {
    color: #42E8A5 !important;
    text-align: center;
    font-size: 28px !important;
}

[data-testid="stSidebar"] h2 {
    color: #FACC15 !important;
}

/* SIDEBAR NAVIGATION RADIO BUTTONS */

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 9px;
}

/* INDIVIDUAL NAVIGATION ITEMS */

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: #142D42;
    border: 1px solid #28536B;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 5px;
    transition: 0.25s ease;
}

/* HOVER EFFECT */

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #176B62;
    border-color: #42E8A5;
}

/* SELECTED NAVIGATION */

[data-testid="stSidebar"] [role="radiogroup"] label:has(
    input:checked
) {
    background: linear-gradient(
        90deg,
        #087F5B,
        #16A085
    );
    border: 1px solid #42E8A5;
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(
        90deg,
        #087F5B,
        #16A085
    );
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    padding: 9px 20px;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #16A085,
        #42E8A5
    );
    color: #071526;
}

/* METRIC CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #142D42,
        #1B4556
    );
    border: 1px solid #267B75;
    border-radius: 13px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #A7F3D0 !important;
}

[data-testid="stMetricValue"] {
    color: #42E8A5 !important;
    font-weight: 800;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #267B75;
    border-radius: 10px;
}

/* INPUT FIELDS */

.stTextInput input,
.stNumberInput input,
.stSelectbox div,
.stMultiSelect div {
    background-color: #142D42 !important;
    color: white !important;
}

/* DIVIDER */

hr {
    border-color: #267B75;
}

/* INFO BOX */

.stAlert {
    border-radius: 10px;
}

/* EXPANDER */

[data-testid="stExpander"] {
    background-color: #102B43;
    border: 1px solid #267B75;
    border-radius: 10px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #94A3B8;
    padding: 20px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

APP_TITLE = "TENNIS IQ"

APP_SUBTITLE = "SPORTS ANALYTICS PLATFORM"

PROJECT_NAME = "Game Analytics"

PROJECT_DESCRIPTION = (
    "Unlocking Tennis Data with Sportradar API"
)


# ============================================================
# DATABASE TABLES
# ============================================================

TABLES = [
    "categories",
    "competitions",
    "complexes",
    "venues",
    "competitor",
    "competitor_rankings"
]


# ============================================================
# SESSION STATE
# ============================================================

if "db_config" not in st.session_state:
    st.session_state.db_config = None

if "db_connected" not in st.session_state:
    st.session_state.db_connected = False

if "db_version" not in st.session_state:
    st.session_state.db_version = None

if "sql_result" not in st.session_state:
    st.session_state.sql_result = None

if "sql_query_name" not in st.session_state:
    st.session_state.sql_query_name = None


# ============================================================
# SUPABASE CLOUD CONFIGURATION
# ============================================================

def get_cloud_config():

    try:

        if "postgresql" in st.secrets:

            config = dict(st.secrets["postgresql"])

            return config

        return None

    except Exception:

        return None


# ============================================================
# DATABASE CONNECTION HELPER
# ============================================================

def connect_with_config(config):

    db_params = dict(config)

    # psycopg2 requires dbname, not database

    if "database" in db_params:

        db_params["dbname"] = db_params.pop("database")

    db_params["port"] = int(
        db_params.get("port", 5432)
    )

    return psycopg2.connect(**db_params)


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():

    cloud_config = get_cloud_config()

    if cloud_config:

        return connect_with_config(
            cloud_config
        )

    if st.session_state.db_config:

        return connect_with_config(
            st.session_state.db_config
        )

    raise Exception(
        "Please configure PostgreSQL connection."
    )


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

def test_database_connection(config):

    connection = None

    try:

        connection = connect_with_config(config)

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT version();"
            )

            version = cursor.fetchone()[0]

        return True, version

    except Exception as error:

        return False, str(error)

    finally:

        if connection:

            connection.close()


# ============================================================
# FETCH DATA FROM POSTGRESQL
# ============================================================

def fetch_data(query, params=None):

    connection = None

    try:

        connection = get_connection()

        dataframe = pd.read_sql_query(
            query,
            connection,
            params=params
        )

        return dataframe

    finally:

        if connection:

            connection.close()


# ============================================================
# EXECUTE SQL QUERY
# ============================================================

def execute_query(query, params=None):

    connection = None

    try:

        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                params
            )

            if cursor.description:

                columns = [
                    description[0]
                    for description in cursor.description
                ]

                rows = cursor.fetchall()

                return pd.DataFrame(
                    rows,
                    columns=columns
                )

            connection.commit()

            return pd.DataFrame()

    finally:

        if connection:

            connection.close()


# ============================================================
# GET DATABASE TABLE INFORMATION
# ============================================================

def get_table_columns(table_name):

    query = """
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = %s
        ORDER BY ordinal_position;
    """

    return fetch_data(
        query,
        (table_name,)
    )


# ============================================================
# CHECK TABLE EXISTENCE
# ============================================================

def get_existing_tables():

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """

    dataframe = fetch_data(query)

    return dataframe["table_name"].tolist()


# ============================================================
# SAFE TABLE COUNT
# ============================================================

def get_table_count(table_name):

    if table_name not in TABLES:

        raise ValueError("Invalid table name")

    query = sql.SQL(
        "SELECT COUNT(*) FROM {}"
    ).format(
        sql.Identifier(table_name)
    )

    connection = None

    try:

        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute(query)

            return cursor.fetchone()[0]

    finally:

        if connection:

            connection.close()


# ============================================================
# FORMAT NUMBER
# ============================================================

def format_number(value):

    try:

        return f"{int(value):,}"

    except Exception:

        return "0"


# ============================================================
# SECTION HEADER HELPER
# ============================================================

def section_header(title, subtitle=None):

    st.markdown(
        f"""
        <h2>{title}</h2>
        """,
        unsafe_allow_html=True
    )

    if subtitle:

        st.markdown(
            f"""
            <p style="
                color:#94A3B8;
                font-size:14px;
            ">
                {subtitle}
            </p>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")


# ============================================================
# CSV DOWNLOAD HELPER
# ============================================================

def download_csv(dataframe, file_name):

    if dataframe is not None and not dataframe.empty:

        csv_data = dataframe.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=file_name,
            mime="text/csv"
        )

    else:

        st.info("No data available for download.")


# ============================================================
# PART 2 - SIDEBAR NAVIGATION + OVERVIEW DASHBOARD
# ============================================================


# ============================================================
# APPLICATION HEADER
# ============================================================

st.markdown(
    """
    <div style="
        background:linear-gradient(100deg,#063B3B,#087F5B,#123B54);
        padding:25px;
        border-radius:16px;
        border:1px solid #42E8A5;
        margin-bottom:20px;
    ">
        <h1 style="
            color:#42E8A5;
            text-align:center;
            font-size:38px;
            margin-bottom:5px;
        ">
            🎾 TENNIS IQ
        </h1>

        <h3 style="
            color:white;
            text-align:center;
            letter-spacing:3px;
            margin-top:0;
        ">
            SPORTS ANALYTICS PLATFORM
        </h3>

        <p style="
            color:#CFFAFE;
            text-align:center;
            font-size:15px;
        ">
            Game Analytics | Unlocking Tennis Data with Sportradar API
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR BRANDING
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:18px 5px;
        background:linear-gradient(135deg,#064E3B,#0F766E);
        border-radius:14px;
        border:1px solid #42E8A5;
    ">
        <div style="font-size:45px;">🎾</div>

        <h1 style="
            color:#42E8A5;
            margin:0;
            font-size:27px;
        ">
            TENNIS IQ
        </h1>

        <p style="
            color:#CCFBF1;
            font-size:12px;
            letter-spacing:2px;
        ">
            SPORTS ANALYTICS
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATABASE CONNECTION STATUS
# ============================================================

st.sidebar.markdown("## 🔌 DATABASE CONNECTION")

cloud_config = get_cloud_config()

if cloud_config:

    st.sidebar.success(
        "☁️ Supabase Cloud Configuration Found"
    )

    try:

        test_connection = get_connection()

        with test_connection.cursor() as cursor:

            cursor.execute("SELECT version();")

            db_version = cursor.fetchone()[0]

        test_connection.close()

        st.session_state.db_connected = True
        st.session_state.db_version = db_version

        st.sidebar.success(
            "🟢 Database Connected Successfully!"
        )

    except Exception as error:

        st.session_state.db_connected = False

        st.sidebar.error(
            "Cloud Database Connection Failed"
        )

        with st.sidebar.expander("View Connection Error"):

            st.code(str(error))


else:

    st.sidebar.info(
        "Configure your local PostgreSQL database below."
    )

    with st.sidebar.expander(
        "⚙️ PostgreSQL Connection Settings"
    ):

        with st.form("database_connection_form"):

            db_host = st.text_input(
                "Host",
                value="localhost"
            )

            db_port = st.number_input(
                "Port",
                min_value=1,
                max_value=65535,
                value=5432
            )

            db_name = st.text_input(
                "Database Name",
                value="tennis_analytics"
            )

            db_user = st.text_input(
                "Username",
                value="postgres"
            )

            db_password = st.text_input(
                "Password",
                type="password"
            )

            connect_button = st.form_submit_button(
                "Connect Database"
            )

            if connect_button:

                local_config = {
                    "host": db_host,
                    "port": int(db_port),
                    "database": db_name,
                    "user": db_user,
                    "password": db_password
                }

                success, result = test_database_connection(
                    local_config
                )

                if success:

                    st.session_state.db_config = local_config

                    st.session_state.db_connected = True

                    st.session_state.db_version = result

                    st.rerun()

                else:

                    st.error(
                        f"Connection failed: {result}"
                    )


# ============================================================
# DATABASE CONNECTION INFORMATION
# ============================================================

if st.session_state.db_connected:

    st.sidebar.markdown(
        """
        <div style="
            background:#064E3B;
            padding:12px;
            border-radius:10px;
            border:1px solid #42E8A5;
        ">
            <p style="color:#86EFAC;margin:0;">
                ● DATABASE ONLINE
            </p>
            <p style="
                color:white;
                font-size:12px;
                margin-top:5px;
            ">
                PostgreSQL Database
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.sidebar.warning(
        "Database is not connected."
    )


# ============================================================
# NAVIGATION MENU
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "## 🧭 NAVIGATION"
)

PAGES = [
    "🏠 Overview",
    "🏆 Competition Analysis",
    "🌍 Venue Analysis",
    "👤 Player Rankings",
    "📊 SQL Insights",
    "🔍 Data Quality",
    "🗄️ Database Explorer"
]


selected_page = st.sidebar.radio(
    "Select Dashboard",
    PAGES,
    index=0,
    label_visibility="collapsed"
)


# ============================================================
# SIDEBAR PROJECT DETAILS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="
        background:#142D42;
        padding:15px;
        border-radius:12px;
        border:1px solid #28536B;
    ">
        <h3 style="
            color:#FACC15;
            font-size:16px;
        ">
            📁 PROJECT DETAILS
        </h3>

        <p style="color:#42E8A5;font-weight:bold;">
            Game Analytics
        </p>

        <p style="
            color:#CBD5E1;
            font-size:12px;
        ">
            Unlocking Tennis Data with Sportradar API
        </p>

        <hr>

        <p style="color:#7DD3FC;font-size:12px;">
            Python • Streamlit • PostgreSQL
        </p>

        <p style="color:#7DD3FC;font-size:12px;">
            Sportradar API • Plotly
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FOOTER
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:15px 5px;
        color:#94A3B8;
        font-size:11px;
    ">
        TENNIS IQ<br>
        Sports Analytics Platform<br>
        Version 1.0
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OVERVIEW DASHBOARD
# ============================================================

if selected_page == "🏠 Overview":

    section_header(
        "🏠 OVERVIEW DASHBOARD",
        "Complete summary of your tennis analytics database"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database "
            "to view the dashboard."
        )

    else:

        try:

            # ------------------------------------------------
            # GET EXISTING TABLES
            # ------------------------------------------------

            existing_tables = get_existing_tables()

            available_tables = [
                table
                for table in TABLES
                if table in existing_tables
            ]

            missing_tables = [
                table
                for table in TABLES
                if table not in existing_tables
            ]

            # ------------------------------------------------
            # DATABASE SUMMARY
            # ------------------------------------------------

            total_tables = len(available_tables)

            total_records = 0

            table_counts = {}

            for table in available_tables:

                count = get_table_count(table)

                table_counts[table] = count

                total_records += count

            # ------------------------------------------------
            # KPI CARDS
            # ------------------------------------------------

            st.markdown(
                "### 📊 DATABASE PERFORMANCE"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    label="📁 Total Tables",
                    value=format_number(total_tables)
                )

            with col2:

                st.metric(
                    label="🗃️ Total Records",
                    value=format_number(total_records)
                )

            with col3:

                st.metric(
                    label="✅ Available Tables",
                    value=format_number(len(available_tables))
                )

            with col4:

                st.metric(
                    label="⚠️ Missing Tables",
                    value=format_number(len(missing_tables))
                )

            st.markdown("---")

            # ------------------------------------------------
            # TABLE RECORD DISTRIBUTION
            # ------------------------------------------------

            st.markdown(
                "### 📚 TABLE RECORD DISTRIBUTION"
            )

            if table_counts:

                count_df = pd.DataFrame(
                    list(table_counts.items()),
                    columns=[
                        "Table Name",
                        "Total Records"
                    ]
                )

                col1, col2 = st.columns(
                    [1.2, 1]
                )

                with col1:

                    fig = px.bar(
                        count_df,
                        x="Table Name",
                        y="Total Records",
                        color="Table Name",
                        text="Total Records",
                        title="Records Available in Each Table",
                        template="plotly_dark"
                    )

                    fig.update_layout(
                        plot_bgcolor="#102B43",
                        paper_bgcolor="#102B43",
                        font_color="white",
                        showlegend=False,
                        xaxis_title="Database Tables",
                        yaxis_title="Record Count"
                    )

                    fig.update_traces(
                        textposition="outside"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                with col2:

                    fig_pie = px.pie(
                        count_df,
                        names="Table Name",
                        values="Total Records",
                        title="Table Distribution",
                        hole=0.45,
                        template="plotly_dark"
                    )

                    fig_pie.update_layout(
                        paper_bgcolor="#102B43",
                        font_color="white"
                    )

                    st.plotly_chart(
                        fig_pie,
                        use_container_width=True
                    )

                # --------------------------------------------
                # TABLE SUMMARY
                # --------------------------------------------

                st.markdown(
                    "### 📋 DATABASE TABLE SUMMARY"
                )

                count_df["Total Records"] = (
                    count_df["Total Records"].apply(
                        format_number
                    )
                )

                st.dataframe(
                    count_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning(
                    "No project tables found in the database."
                )

            # ------------------------------------------------
            # DATABASE TABLE STATUS
            # ------------------------------------------------

            st.markdown("---")

            st.markdown(
                "### 🔎 DATABASE TABLE STATUS"
            )

            status_data = []

            for table in TABLES:

                if table in existing_tables:

                    status_data.append({
                        "Table Name": table,
                        "Status": "Available",
                        "Records": format_number(
                            table_counts.get(table, 0)
                        )
                    })

                else:

                    status_data.append({
                        "Table Name": table,
                        "Status": "Missing",
                        "Records": "0"
                    })

            status_df = pd.DataFrame(
                status_data
            )

            st.dataframe(
                status_df,
                use_container_width=True,
                hide_index=True
            )

            if missing_tables:

                st.warning(
                    "Missing tables: "
                    + ", ".join(missing_tables)
                )

            else:

                st.success(
                    "All six expected project tables are available!"
                )

            # ------------------------------------------------
            # PROJECT TECHNOLOGY STACK
            # ------------------------------------------------

            st.markdown("---")

            st.markdown(
                "### 🛠️ TECHNOLOGY STACK"
            )

            tech1, tech2, tech3, tech4 = st.columns(4)

            with tech1:

                st.info(
                    "🐍 Python\n\nData Processing"
                )

            with tech2:

                st.info(
                    "📊 Streamlit\n\nDashboard Development"
                )

            with tech3:

                st.info(
                    "🐘 PostgreSQL\n\nDatabase Management"
                )

            with tech4:

                st.info(
                    "📈 Plotly\n\nData Visualization"
                )

            # ------------------------------------------------
            # OVERVIEW FOOTNOTE
            # ------------------------------------------------

            st.markdown(
                """
                <div style="
                    background:#142D42;
                    padding:15px;
                    border-radius:10px;
                    border-left:4px solid #42E8A5;
                    margin-top:20px;
                ">
                    <p style="color:#42E8A5;font-weight:bold;">
                        🎾 TENNIS IQ - DATA INSIGHTS
                    </p>

                    <p style="color:#CBD5E1;font-size:13px;">
                        This dashboard provides an overview
                        of the tennis database, table availability,
                        record distribution and technology stack.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as error:

            st.error(
                "Unable to load Overview Dashboard."
            )

            st.exception(error)


# ============================================================
# PART 3 - COMPETITION ANALYSIS + VENUE ANALYSIS
# ============================================================


# ============================================================
# COMPETITION ANALYSIS
# ============================================================

elif selected_page == "🏆 Competition Analysis":

    section_header(
        "🏆 COMPETITION ANALYSIS",
        "Explore tennis competitions, categories and tournament distribution"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database first."
        )

    else:

        try:

            competition_tables = get_existing_tables()

            if "competitions" not in competition_tables:

                st.error(
                    "Competitions table is not available."
                )

            else:

                competition_df = fetch_data(
                    'SELECT * FROM "competitions"'
                )

                if competition_df.empty:

                    st.warning(
                        "No competition records found."
                    )

                else:

                    # ----------------------------------------
                    # DATA PREPARATION
                    # ----------------------------------------

                    total_competitions = len(
                        competition_df
                    )

                    competition_columns = (
                        competition_df.columns.tolist()
                    )

                    st.markdown(
                        "### 📊 COMPETITION OVERVIEW"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "🏆 Total Competitions",
                            format_number(total_competitions)
                        )

                    with col2:

                        if "type" in competition_columns:

                            total_types = competition_df[
                                "type"
                            ].nunique()

                        else:

                            total_types = 0

                        st.metric(
                            "🎾 Competition Types",
                            format_number(total_types)
                        )

                    with col3:

                        if "gender" in competition_columns:

                            total_genders = competition_df[
                                "gender"
                            ].nunique()

                        else:

                            total_genders = 0

                        st.metric(
                            "👥 Gender Categories",
                            format_number(total_genders)
                        )

                    with col4:

                        if "category_id" in competition_columns:

                            total_categories = competition_df[
                                "category_id"
                            ].nunique()

                        else:

                            total_categories = 0

                        st.metric(
                            "📁 Categories",
                            format_number(total_categories)
                        )

                    st.markdown("---")

                    # ----------------------------------------
                    # FILTER SECTION
                    # ----------------------------------------

                    st.markdown(
                        "### 🔎 COMPETITION FILTERS"
                    )

                    filtered_competitions = (
                        competition_df.copy()
                    )

                    filter_col1, filter_col2 = st.columns(2)

                    if "type" in competition_columns:

                        with filter_col1:

                            type_options = sorted(
                                competition_df["type"]
                                .dropna()
                                .astype(str)
                                .unique()
                                .tolist()
                            )

                            selected_types = st.multiselect(
                                "Select Competition Type",
                                type_options,
                                default=type_options,
                                key="competition_type_filter"
                            )

                            filtered_competitions = (
                                filtered_competitions[
                                    filtered_competitions[
                                        "type"
                                    ].astype(str).isin(
                                        selected_types
                                    )
                                ]
                            )

                    if "gender" in competition_columns:

                        with filter_col2:

                            gender_options = sorted(
                                competition_df["gender"]
                                .dropna()
                                .astype(str)
                                .unique()
                                .tolist()
                            )

                            selected_genders = st.multiselect(
                                "Select Gender",
                                gender_options,
                                default=gender_options,
                                key="competition_gender_filter"
                            )

                            filtered_competitions = (
                                filtered_competitions[
                                    filtered_competitions[
                                        "gender"
                                    ].astype(str).isin(
                                        selected_genders
                                    )
                                ]
                            )

                    # ----------------------------------------
                    # FILTERED KPI
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📈 FILTERED RESULTS"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Filtered Competitions",
                            format_number(
                                len(filtered_competitions)
                            )
                        )

                    with col2:

                        st.metric(
                            "Available Columns",
                            format_number(
                                len(competition_columns)
                            )
                        )

                    # ----------------------------------------
                    # COMPETITION TYPE ANALYSIS
                    # ----------------------------------------

                    if (
                        "type" in competition_columns
                        and not filtered_competitions.empty
                    ):

                        st.markdown("---")

                        st.markdown(
                            "### 🎾 COMPETITION TYPE DISTRIBUTION"
                        )

                        type_df = (
                            filtered_competitions[
                                "type"
                            ]
                            .fillna("Unknown")
                            .value_counts()
                            .reset_index()
                        )

                        type_df.columns = [
                            "Competition Type",
                            "Count"
                        ]

                        fig_type = px.bar(
                            type_df,
                            x="Competition Type",
                            y="Count",
                            color="Competition Type",
                            text="Count",
                            title="Competitions by Type",
                            template="plotly_dark"
                        )

                        fig_type.update_layout(
                            plot_bgcolor="#102B43",
                            paper_bgcolor="#102B43",
                            font_color="white",
                            showlegend=False
                        )

                        st.plotly_chart(
                            fig_type,
                            use_container_width=True
                        )

                    # ----------------------------------------
                    # GENDER ANALYSIS
                    # ----------------------------------------

                    if (
                        "gender" in competition_columns
                        and not filtered_competitions.empty
                    ):

                        st.markdown("---")

                        st.markdown(
                            "### 👥 GENDER DISTRIBUTION"
                        )

                        gender_df = (
                            filtered_competitions[
                                "gender"
                            ]
                            .fillna("Unknown")
                            .value_counts()
                            .reset_index()
                        )

                        gender_df.columns = [
                            "Gender",
                            "Count"
                        ]

                        col1, col2 = st.columns(2)

                        with col1:

                            fig_gender = px.pie(
                                gender_df,
                                names="Gender",
                                values="Count",
                                title="Competition Gender Distribution",
                                hole=0.4,
                                template="plotly_dark"
                            )

                            fig_gender.update_layout(
                                paper_bgcolor="#102B43",
                                font_color="white"
                            )

                            st.plotly_chart(
                                fig_gender,
                                use_container_width=True
                            )

                        with col2:

                            fig_gender_bar = px.bar(
                                gender_df,
                                x="Gender",
                                y="Count",
                                color="Gender",
                                text="Count",
                                title="Gender-wise Competitions",
                                template="plotly_dark"
                            )

                            fig_gender_bar.update_layout(
                                plot_bgcolor="#102B43",
                                paper_bgcolor="#102B43",
                                font_color="white",
                                showlegend=False
                            )

                            st.plotly_chart(
                                fig_gender_bar,
                                use_container_width=True
                            )

                    # ----------------------------------------
                    # CATEGORY ANALYSIS
                    # ----------------------------------------

                    if (
                        "category_id" in competition_columns
                        and "categories" in competition_tables
                    ):

                        st.markdown("---")

                        st.markdown(
                            "### 📁 CATEGORY-WISE COMPETITIONS"
                        )

                        category_columns = get_table_columns(
                            "categories"
                        )["column_name"].tolist()

                        if (
                            "category_id" in category_columns
                            and "category_name" in category_columns
                        ):

                            category_query = """
                                SELECT
                                    c.category_name,
                                    COUNT(co.competition_id)
                                    AS total_competitions
                                FROM categories c
                                LEFT JOIN competitions co
                                    ON c.category_id = co.category_id
                                GROUP BY c.category_name
                                ORDER BY total_competitions DESC;
                            """

                            category_df = fetch_data(
                                category_query
                            )

                            if not category_df.empty:

                                fig_category = px.bar(
                                    category_df,
                                    x="category_name",
                                    y="total_competitions",
                                    color="category_name",
                                    text="total_competitions",
                                    title="Competitions by Category",
                                    template="plotly_dark"
                                )

                                fig_category.update_layout(
                                    plot_bgcolor="#102B43",
                                    paper_bgcolor="#102B43",
                                    font_color="white",
                                    showlegend=False,
                                    xaxis_title="Category",
                                    yaxis_title="Total Competitions"
                                )

                                st.plotly_chart(
                                    fig_category,
                                    use_container_width=True
                                )

                        else:

                            st.info(
                                "Category name columns are not available."
                            )

                    # ----------------------------------------
                    # COMPETITION DATA TABLE
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📋 COMPETITION DATA EXPLORER"
                    )

                    st.dataframe(
                        filtered_competitions,
                        use_container_width=True,
                        hide_index=True
                    )

                    download_csv(
                        filtered_competitions,
                        "tennis_competition_analysis.csv"
                    )

        except Exception as error:

            st.error(
                "Competition Analysis could not be loaded."
            )

            st.exception(error)


# ============================================================
# VENUE ANALYSIS
# ============================================================

elif selected_page == "🌍 Venue Analysis":

    section_header(
        "🌍 VENUE ANALYSIS",
        "Explore tennis venues, cities, countries and complexes"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database first."
        )

    else:

        try:

            venue_tables = get_existing_tables()

            if "venues" not in venue_tables:

                st.error(
                    "Venues table is not available."
                )

            else:

                venue_df = fetch_data(
                    'SELECT * FROM "venues"'
                )

                if venue_df.empty:

                    st.warning(
                        "No venue records found."
                    )

                else:

                    # ----------------------------------------
                    # DATA PREPARATION
                    # ----------------------------------------

                    venue_columns = (
                        venue_df.columns.tolist()
                    )

                    total_venues = len(venue_df)

                    # ----------------------------------------
                    # VENUE KPI CARDS
                    # ----------------------------------------

                    st.markdown(
                        "### 📊 VENUE OVERVIEW"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "🌍 Total Venues",
                            format_number(total_venues)
                        )

                    with col2:

                        if "country_name" in venue_columns:

                            country_count = venue_df[
                                "country_name"
                            ].nunique()

                        else:

                            country_count = 0

                        st.metric(
                            "🌐 Countries",
                            format_number(country_count)
                        )

                    with col3:

                        if "city_name" in venue_columns:

                            city_count = venue_df[
                                "city_name"
                            ].nunique()

                        else:

                            city_count = 0

                        st.metric(
                            "🏙️ Cities",
                            format_number(city_count)
                        )

                    with col4:

                        if "complex_id" in venue_columns:

                            complex_count = venue_df[
                                "complex_id"
                            ].nunique()

                        else:

                            complex_count = 0

                        st.metric(
                            "🏟️ Complexes",
                            format_number(complex_count)
                        )

                    st.markdown("---")

                    # ----------------------------------------
                    # VENUE FILTERS
                    # ----------------------------------------

                    st.markdown(
                        "### 🔎 VENUE FILTERS"
                    )

                    filtered_venues = venue_df.copy()

                    filter_col1, filter_col2 = st.columns(2)

                    if "country_name" in venue_columns:

                        with filter_col1:

                            country_options = sorted(
                                venue_df["country_name"]
                                .dropna()
                                .astype(str)
                                .unique()
                                .tolist()
                            )

                            selected_countries = st.multiselect(
                                "Select Country",
                                country_options,
                                default=country_options,
                                key="venue_country_filter"
                            )

                            filtered_venues = (
                                filtered_venues[
                                    filtered_venues[
                                        "country_name"
                                    ].astype(str).isin(
                                        selected_countries
                                    )
                                ]
                            )

                    if "city_name" in venue_columns:

                        with filter_col2:

                            city_options = sorted(
                                filtered_venues["city_name"]
                                .dropna()
                                .astype(str)
                                .unique()
                                .tolist()
                            )

                            selected_cities = st.multiselect(
                                "Select City",
                                city_options,
                                default=city_options,
                                key="venue_city_filter"
                            )

                            filtered_venues = (
                                filtered_venues[
                                    filtered_venues[
                                        "city_name"
                                    ].astype(str).isin(
                                        selected_cities
                                    )
                                ]
                            )

                    # ----------------------------------------
                    # FILTERED VENUE RESULTS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📈 FILTERED VENUE RESULTS"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Filtered Venues",
                            format_number(
                                len(filtered_venues)
                            )
                        )

                    with col2:

                        st.metric(
                            "Available Columns",
                            format_number(
                                len(venue_columns)
                            )
                        )

                    # ----------------------------------------
                    # COUNTRY-WISE VENUE ANALYSIS
                    # ----------------------------------------

                    if (
                        "country_name" in venue_columns
                        and not filtered_venues.empty
                    ):

                        st.markdown("---")

                        st.markdown(
                            "### 🌐 COUNTRY-WISE VENUE DISTRIBUTION"
                        )

                        country_df = (
                            filtered_venues[
                                "country_name"
                            ]
                            .fillna("Unknown")
                            .value_counts()
                            .reset_index()
                        )

                        country_df.columns = [
                            "Country",
                            "Venue Count"
                        ]

                        col1, col2 = st.columns(2)

                        with col1:

                            fig_country = px.bar(
                                country_df.head(15),
                                x="Country",
                                y="Venue Count",
                                color="Country",
                                text="Venue Count",
                                title="Top 15 Countries by Venues",
                                template="plotly_dark"
                            )

                            fig_country.update_layout(
                                plot_bgcolor="#102B43",
                                paper_bgcolor="#102B43",
                                font_color="white",
                                showlegend=False,
                                xaxis_tickangle=-45
                            )

                            st.plotly_chart(
                                fig_country,
                                use_container_width=True
                            )

                        with col2:

                            fig_country_pie = px.pie(
                                country_df.head(10),
                                names="Country",
                                values="Venue Count",
                                title="Top 10 Countries",
                                hole=0.4,
                                template="plotly_dark"
                            )

                            fig_country_pie.update_layout(
                                paper_bgcolor="#102B43",
                                font_color="white"
                            )

                            st.plotly_chart(
                                fig_country_pie,
                                use_container_width=True
                            )

                    # ----------------------------------------
                    # CITY-WISE VENUE ANALYSIS
                    # ----------------------------------------

                    if (
                        "city_name" in venue_columns
                        and not filtered_venues.empty
                    ):

                        st.markdown("---")

                        st.markdown(
                            "### 🏙️ CITY-WISE VENUE DISTRIBUTION"
                        )

                        city_df = (
                            filtered_venues[
                                "city_name"
                            ]
                            .fillna("Unknown")
                            .value_counts()
                            .head(15)
                            .reset_index()
                        )

                        city_df.columns = [
                            "City",
                            "Venue Count"
                        ]

                        fig_city = px.bar(
                            city_df,
                            x="City",
                            y="Venue Count",
                            color="City",
                            text="Venue Count",
                            title="Top 15 Cities by Venue Count",
                            template="plotly_dark"
                        )

                        fig_city.update_layout(
                            plot_bgcolor="#102B43",
                            paper_bgcolor="#102B43",
                            font_color="white",
                            showlegend=False,
                            xaxis_tickangle=-45
                        )

                        st.plotly_chart(
                            fig_city,
                            use_container_width=True
                        )

                    # ----------------------------------------
                    # COMPLEX ANALYSIS
                    # ----------------------------------------

                    if (
                        "complex_id" in venue_columns
                        and "complexes" in venue_tables
                    ):

                        st.markdown("---")

                        st.markdown(
                            "### 🏟️ VENUE COMPLEX ANALYSIS"
                        )

                        complex_columns = get_table_columns(
                            "complexes"
                        )["column_name"].tolist()

                        if (
                            "complex_id" in complex_columns
                            and "complex_name" in complex_columns
                        ):

                            complex_query = """
                                SELECT
                                    c.complex_name,
                                    COUNT(v.venue_id) AS total_venues
                                FROM complexes c
                                LEFT JOIN venues v
                                    ON c.complex_id = v.complex_id
                                GROUP BY c.complex_name
                                ORDER BY total_venues DESC;
                            """

                            complex_df = fetch_data(
                                complex_query
                            )

                            if not complex_df.empty:

                                st.dataframe(
                                    complex_df,
                                    use_container_width=True,
                                    hide_index=True
                                )

                        else:

                            st.info(
                                "Complex name columns are not available."
                            )

                    # ----------------------------------------
                    # VENUE DATA TABLE
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📋 VENUE DATA EXPLORER"
                    )

                    st.dataframe(
                        filtered_venues,
                        use_container_width=True,
                        hide_index=True
                    )

                    download_csv(
                        filtered_venues,
                        "tennis_venue_analysis.csv"
                    )

        except Exception as error:

            st.error(
                "Venue Analysis could not be loaded."
            )

            st.exception(error)


# ============================================================
# PART 4 - PLAYER RANKINGS + SQL INSIGHTS
# ============================================================


# ============================================================
# PLAYER RANKINGS
# ============================================================

elif selected_page == "👤 Player Rankings":

    section_header(
        "👤 PLAYER RANKINGS",
        "Explore tennis player rankings, points and ranking movements"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database first."
        )

    else:

        try:

            ranking_tables = get_existing_tables()

            if (
                "competitor_rankings" not in ranking_tables
                or "competitor" not in ranking_tables
            ):

                st.error(
                    "Competitor or Competitor Rankings table is missing."
                )

            else:

                ranking_columns = get_table_columns(
                    "competitor_rankings"
                )["column_name"].tolist()

                player_columns = get_table_columns(
                    "competitor"
                )["column_name"].tolist()

                required_ranking_columns = [
                    "competitor_id",
                    "rank",
                    "points"
                ]

                required_player_columns = [
                    "competitor_id",
                    "name"
                ]

                missing_ranking_columns = [
                    column
                    for column in required_ranking_columns
                    if column not in ranking_columns
                ]

                missing_player_columns = [
                    column
                    for column in required_player_columns
                    if column not in player_columns
                ]

                if (
                    missing_ranking_columns
                    or missing_player_columns
                ):

                    st.warning(
                        "Required ranking columns are not available."
                    )

                    st.write(
                        "Missing ranking columns:",
                        missing_ranking_columns
                    )

                    st.write(
                        "Missing player columns:",
                        missing_player_columns
                    )

                else:

                    # ----------------------------------------
                    # BUILD PLAYER RANKING QUERY
                    # ----------------------------------------

                    optional_player_fields = []

                    if "country" in player_columns:

                        optional_player_fields.append(
                            "p.country"
                        )

                    optional_ranking_fields = []

                    for column in [
                        "movement",
                        "competitions_played"
                    ]:

                        if column in ranking_columns:

                            optional_ranking_fields.append(
                                f"r.{column}"
                            )

                    select_fields = [
                        "p.competitor_id",
                        "p.name",
                        "r.rank",
                        "r.points"
                    ]

                    select_fields.extend(
                        optional_player_fields
                    )

                    select_fields.extend(
                        optional_ranking_fields
                    )

                    select_clause = ", ".join(
                        select_fields
                    )

                    ranking_query = f"""
                        SELECT
                            {select_clause}
                        FROM competitor_rankings r
                        INNER JOIN competitor p
                            ON r.competitor_id = p.competitor_id
                        ORDER BY r.rank ASC;
                    """

                    ranking_df = fetch_data(
                        ranking_query
                    )

                    if ranking_df.empty:

                        st.warning(
                            "No player ranking records found."
                        )

                    else:

                        # ------------------------------------
                        # RANKING OVERVIEW
                        # ------------------------------------

                        st.markdown(
                            "### 📊 RANKING OVERVIEW"
                        )

                        total_players = len(
                            ranking_df
                        )

                        total_points = pd.to_numeric(
                            ranking_df["points"],
                            errors="coerce"
                        ).fillna(0).sum()

                        average_points = pd.to_numeric(
                            ranking_df["points"],
                            errors="coerce"
                        ).mean()

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:

                            st.metric(
                                "👥 Ranked Players",
                                format_number(total_players)
                            )

                        with col2:

                            st.metric(
                                "🏆 Top Rank",
                                format_number(
                                    ranking_df["rank"].min()
                                )
                            )

                        with col3:

                            st.metric(
                                "⭐ Total Points",
                                format_number(total_points)
                            )

                        with col4:

                            st.metric(
                                "📈 Average Points",
                                format_number(
                                    average_points
                                )
                            )

                        st.markdown("---")

                        # ------------------------------------
                        # PLAYER FILTERS
                        # ------------------------------------

                        st.markdown(
                            "### 🔎 PLAYER FILTERS"
                        )

                        filtered_rankings = ranking_df.copy()

                        filter_col1, filter_col2 = st.columns(2)

                        if "country" in ranking_df.columns:

                            with filter_col1:

                                country_options = sorted(
                                    ranking_df["country"]
                                    .dropna()
                                    .astype(str)
                                    .unique()
                                    .tolist()
                                )

                                selected_countries = st.multiselect(
                                    "Select Country",
                                    country_options,
                                    default=country_options,
                                    key="ranking_country_filter"
                                )

                                filtered_rankings = (
                                    filtered_rankings[
                                        filtered_rankings[
                                            "country"
                                        ].astype(str).isin(
                                            selected_countries
                                        )
                                    ]
                                )

                        with filter_col2:

                            max_rank = int(
                                pd.to_numeric(
                                    ranking_df["rank"],
                                    errors="coerce"
                                ).max()
                            )

                            selected_top_rank = st.slider(
                                "Show Top Rankings",
                                min_value=1,
                                max_value=max(1, max_rank),
                                value=min(100, max(1, max_rank)),
                                key="top_rank_filter"
                            )

                            filtered_rankings = (
                                filtered_rankings[
                                    pd.to_numeric(
                                        filtered_rankings["rank"],
                                        errors="coerce"
                                    ) <= selected_top_rank
                                ]
                            )

                        # ------------------------------------
                        # FILTERED KPI
                        # ------------------------------------

                        st.markdown("---")

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "Filtered Players",
                                format_number(
                                    len(filtered_rankings)
                                )
                            )

                        with col2:

                            st.metric(
                                "Top Ranking Selected",
                                format_number(
                                    selected_top_rank
                                )
                            )

                        # ------------------------------------
                        # TOP PLAYERS TABLE
                        # ------------------------------------

                        st.markdown("---")

                        st.markdown(
                            "### 🏆 TOP 10 PLAYERS"
                        )

                        top_players = (
                            ranking_df
                            .sort_values(
                                "rank",
                                ascending=True
                            )
                            .head(10)
                        )

                        st.dataframe(
                            top_players,
                            use_container_width=True,
                            hide_index=True
                        )

                        # ------------------------------------
                        # TOP PLAYER POINTS CHART
                        # ------------------------------------

                        st.markdown("---")

                        st.markdown(
                            "### ⭐ TOP PLAYER POINTS ANALYSIS"
                        )

                        chart_df = (
                            ranking_df
                            .sort_values(
                                "points",
                                ascending=False
                            )
                            .head(15)
                        )

                        fig_points = px.bar(
                            chart_df,
                            x="name",
                            y="points",
                            color="points",
                            text="points",
                            title="Top 15 Players by Ranking Points",
                            template="plotly_dark"
                        )

                        fig_points.update_layout(
                            plot_bgcolor="#102B43",
                            paper_bgcolor="#102B43",
                            font_color="white",
                            xaxis_title="Player",
                            yaxis_title="Ranking Points",
                            xaxis_tickangle=-45,
                            showlegend=False
                        )

                        st.plotly_chart(
                            fig_points,
                            use_container_width=True
                        )

                        # ------------------------------------
                        # COUNTRY-WISE PLAYER ANALYSIS
                        # ------------------------------------

                        if (
                            "country" in ranking_df.columns
                            and not ranking_df.empty
                        ):

                            st.markdown("---")

                            st.markdown(
                                "### 🌍 COUNTRY-WISE PLAYER DISTRIBUTION"
                            )

                            country_df = (
                                ranking_df[
                                    "country"
                                ]
                                .fillna("Unknown")
                                .value_counts()
                                .head(15)
                                .reset_index()
                            )

                            country_df.columns = [
                                "Country",
                                "Players"
                            ]

                            fig_country = px.bar(
                                country_df,
                                x="Country",
                                y="Players",
                                color="Country",
                                text="Players",
                                title="Top 15 Countries by Ranked Players",
                                template="plotly_dark"
                            )

                            fig_country.update_layout(
                                plot_bgcolor="#102B43",
                                paper_bgcolor="#102B43",
                                font_color="white",
                                showlegend=False,
                                xaxis_tickangle=-45
                            )

                            st.plotly_chart(
                                fig_country,
                                use_container_width=True
                            )

                        # ------------------------------------
                        # MOVEMENT ANALYSIS
                        # ------------------------------------

                        if "movement" in ranking_df.columns:

                            st.markdown("---")

                            st.markdown(
                                "### 📈 RANKING MOVEMENT ANALYSIS"
                            )

                            movement_df = (
                                ranking_df[
                                    "movement"
                                ]
                                .fillna("Unknown")
                                .astype(str)
                                .value_counts()
                                .reset_index()
                            )

                            movement_df.columns = [
                                "Movement",
                                "Players"
                            ]

                            fig_movement = px.pie(
                                movement_df,
                                names="Movement",
                                values="Players",
                                title="Player Ranking Movement",
                                hole=0.4,
                                template="plotly_dark"
                            )

                            fig_movement.update_layout(
                                paper_bgcolor="#102B43",
                                font_color="white"
                            )

                            st.plotly_chart(
                                fig_movement,
                                use_container_width=True
                            )

                        # ------------------------------------
                        # COMPLETE RANKING TABLE
                        # ------------------------------------

                        st.markdown("---")

                        st.markdown(
                            "### 📋 COMPLETE PLAYER RANKINGS"
                        )

                        st.dataframe(
                            filtered_rankings,
                            use_container_width=True,
                            hide_index=True
                        )

                        download_csv(
                            filtered_rankings,
                            "tennis_player_rankings.csv"
                        )

        except Exception as error:

            st.error(
                "Player Rankings could not be loaded."
            )

            st.exception(error)


# ============================================================
# SQL INSIGHTS
# ============================================================

elif selected_page == "📊 SQL Insights":

    section_header(
        "📊 SQL INSIGHTS",
        "Explore tennis data using PostgreSQL queries"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database first."
        )

    else:

        try:

            existing_tables = get_existing_tables()

            sql_queries = {

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

            # --------------------------------------------
            # SQL QUERY SELECTION
            # --------------------------------------------

            st.markdown(
                "### 🧠 SELECT SQL ANALYSIS"
            )

            selected_query_name = st.selectbox(
                "Choose SQL Query",
                list(sql_queries.keys()),
                key="sql_query_selection"
            )

            selected_sql = sql_queries[
                selected_query_name
            ]

            # --------------------------------------------
            # QUERY PREVIEW
            # --------------------------------------------

            with st.expander(
                "👨‍💻 View SQL Query"
            ):

                st.code(
                    selected_sql,
                    language="sql"
                )

            # --------------------------------------------
            # RUN SQL
            # --------------------------------------------

            if st.button(
                "▶️ RUN SQL QUERY",
                key="run_sql_query"
            ):

                required_tables = []

                for table in TABLES:

                    if table in selected_sql.lower():

                        required_tables.append(table)

                missing_required_tables = [
                    table
                    for table in required_tables
                    if table not in existing_tables
                ]

                if missing_required_tables:

                    st.error(
                        "Required tables are missing: "
                        + ", ".join(missing_required_tables)
                    )

                    st.session_state.sql_result = None

                else:

                    try:

                        result_df = fetch_data(
                            selected_sql
                        )

                        st.session_state.sql_result = (
                            result_df
                        )

                        st.session_state.sql_query_name = (
                            selected_query_name
                        )

                        st.success(
                            "SQL Query executed successfully!"
                        )

                    except Exception as query_error:

                        st.session_state.sql_result = None

                        st.error(
                            "SQL execution failed."
                        )

                        st.exception(query_error)

            # --------------------------------------------
            # DISPLAY SQL RESULTS
            # --------------------------------------------

            if st.session_state.sql_result is not None:

                st.markdown("---")

                st.markdown(
                    "### 📋 SQL QUERY RESULTS"
                )

                st.info(
                    "Query: "
                    + str(
                        st.session_state.sql_query_name
                    )
                )

                result_df = st.session_state.sql_result

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Result Rows",
                        format_number(len(result_df))
                    )

                with col2:

                    st.metric(
                        "Result Columns",
                        format_number(len(result_df.columns))
                    )

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True
                )

                download_csv(
                    result_df,
                    "tennis_sql_insights.csv"
                )

        except Exception as error:

            st.error(
                "SQL Insights could not be loaded."
            )

            st.exception(error)


# ============================================================
# PART 5 - DATA QUALITY + DATABASE EXPLORER
# ============================================================


# ============================================================
# DATA QUALITY
# ============================================================

elif selected_page == "🔍 Data Quality":

    section_header(
        "🔍 DATA QUALITY",
        "Monitor database health, missing values, duplicates and data consistency"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database first."
        )

    else:

        try:

            existing_tables = get_existing_tables()

            available_tables = [
                table
                for table in TABLES
                if table in existing_tables
            ]

            if not available_tables:

                st.warning(
                    "No project tables available."
                )

            else:

                # --------------------------------------------
                # TABLE SELECTION
                # --------------------------------------------

                st.markdown(
                    "### 📁 SELECT TABLE FOR QUALITY CHECK"
                )

                selected_quality_table = st.selectbox(
                    "Choose Database Table",
                    available_tables,
                    key="quality_table_selection"
                )

                # --------------------------------------------
                # LOAD TABLE DATA
                # --------------------------------------------

                quality_query = sql.SQL(
                    "SELECT * FROM {} LIMIT 5000"
                ).format(
                    sql.Identifier(
                        selected_quality_table
                    )
                )

                connection = None

                try:

                    connection = get_connection()

                    quality_df = pd.read_sql_query(
                        quality_query.as_string(connection),
                        connection
                    )

                finally:

                    if connection:

                        connection.close()

                if quality_df.empty:

                    st.warning(
                        "Selected table has no records."
                    )

                else:

                    # ----------------------------------------
                    # TABLE QUALITY OVERVIEW
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📊 DATA QUALITY OVERVIEW"
                    )

                    total_rows = len(quality_df)

                    total_columns = len(
                        quality_df.columns
                    )

                    missing_cells = int(
                        quality_df.isnull().sum().sum()
                    )

                    duplicate_rows = int(
                        quality_df.duplicated().sum()
                    )

                    total_cells = (
                        total_rows * total_columns
                    )

                    if total_cells > 0:

                        completeness = (
                            (total_cells - missing_cells)
                            / total_cells
                        ) * 100

                    else:

                        completeness = 0

                    col1, col2, col3, col4, col5 = (
                        st.columns(5)
                    )

                    with col1:

                        st.metric(
                            "📄 Total Rows",
                            format_number(total_rows)
                        )

                    with col2:

                        st.metric(
                            "📋 Total Columns",
                            format_number(total_columns)
                        )

                    with col3:

                        st.metric(
                            "❌ Missing Cells",
                            format_number(missing_cells)
                        )

                    with col4:

                        st.metric(
                            "♻️ Duplicate Rows",
                            format_number(duplicate_rows)
                        )

                    with col5:

                        st.metric(
                            "✅ Completeness",
                            f"{completeness:.2f}%"
                        )

                    # ----------------------------------------
                    # COMPLETENESS INDICATOR
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📈 DATA COMPLETENESS"
                    )

                    st.progress(
                        min(
                            max(completeness / 100, 0),
                            1
                        )
                    )

                    st.write(
                        f"Data completeness: {completeness:.2f}%"
                    )

                    # ----------------------------------------
                    # MISSING VALUES BY COLUMN
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### ❌ MISSING VALUES ANALYSIS"
                    )

                    missing_df = pd.DataFrame({

                        "Column Name": quality_df.columns,

                        "Missing Values": [
                            int(value)
                            for value in quality_df.isnull().sum()
                        ],

                        "Missing Percentage": [
                            round(
                                (
                                    value / total_rows
                                ) * 100,
                                2
                            )
                            for value in quality_df.isnull().sum()
                        ]

                    })

                    missing_df = (
                        missing_df.sort_values(
                            "Missing Values",
                            ascending=False
                        )
                    )

                    st.dataframe(
                        missing_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    missing_chart_df = missing_df[
                        missing_df["Missing Values"] > 0
                    ]

                    if not missing_chart_df.empty:

                        fig_missing = px.bar(
                            missing_chart_df,
                            x="Column Name",
                            y="Missing Values",
                            color="Missing Values",
                            text="Missing Values",
                            title="Missing Values by Column",
                            template="plotly_dark"
                        )

                        fig_missing.update_layout(
                            plot_bgcolor="#102B43",
                            paper_bgcolor="#102B43",
                            font_color="white",
                            showlegend=False
                        )

                        st.plotly_chart(
                            fig_missing,
                            use_container_width=True
                        )

                    else:

                        st.success(
                            "No missing values found in the loaded sample."
                        )

                    # ----------------------------------------
                    # DUPLICATE RECORD ANALYSIS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### ♻️ DUPLICATE RECORD ANALYSIS"
                    )

                    duplicate_df = quality_df[
                        quality_df.duplicated(
                            keep=False
                        )
                    ]

                    if not duplicate_df.empty:

                        st.warning(
                            f"{len(duplicate_df)} rows belong to duplicate groups."
                        )

                        st.dataframe(
                            duplicate_df.head(100),
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.success(
                            "No completely duplicate rows found in the loaded sample."
                        )

                    # ----------------------------------------
                    # COLUMN DATA TYPE ANALYSIS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 🧾 COLUMN DATA TYPES"
                    )

                    datatype_df = pd.DataFrame({

                        "Column Name": quality_df.columns,

                        "Data Type": [
                            str(dtype)
                            for dtype in quality_df.dtypes
                        ],

                        "Unique Values": [
                            int(quality_df[column].nunique())
                            for column in quality_df.columns
                        ],

                        "Non-Null Values": [
                            int(quality_df[column].notnull().sum())
                            for column in quality_df.columns
                        ]

                    })

                    st.dataframe(
                        datatype_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # ----------------------------------------
                    # UNIQUE VALUE ANALYSIS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 🔢 COLUMN UNIQUENESS ANALYSIS"
                    )

                    unique_df = datatype_df[
                        [
                            "Column Name",
                            "Unique Values",
                            "Non-Null Values"
                        ]
                    ].copy()

                    fig_unique = px.bar(
                        unique_df,
                        x="Column Name",
                        y="Unique Values",
                        color="Unique Values",
                        title="Unique Values by Column",
                        template="plotly_dark"
                    )

                    fig_unique.update_layout(
                        plot_bgcolor="#102B43",
                        paper_bgcolor="#102B43",
                        font_color="white",
                        showlegend=False
                    )

                    st.plotly_chart(
                        fig_unique,
                        use_container_width=True
                    )

                    # ----------------------------------------
                    # QUALITY CHECK SUMMARY
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 📝 QUALITY CHECK SUMMARY"
                    )

                    if missing_cells == 0:

                        st.success(
                            "No missing values found in this sample."
                        )

                    else:

                        st.warning(
                            f"Missing values detected: {missing_cells}"
                        )

                    if duplicate_rows == 0:

                        st.success(
                            "No completely duplicate rows found in this sample."
                        )

                    else:

                        st.warning(
                            f"Duplicate rows detected: {duplicate_rows}"
                        )

                    st.info(
                        "Quality checks are based on a maximum of "
                        "5,000 loaded rows. They do not modify or "
                        "delete your database records."
                    )

                    download_csv(
                        missing_df,
                        "tennis_data_quality_report.csv"
                    )

        except Exception as error:

            st.error(
                "Data Quality analysis could not be loaded."
            )

            st.exception(error)


# ============================================================
# DATABASE EXPLORER
# ============================================================

elif selected_page == "🗄️ Database Explorer":

    section_header(
        "🗄️ DATABASE EXPLORER",
        "Explore PostgreSQL tables, columns, records and database structure"
    )

    if not st.session_state.db_connected:

        st.warning(
            "Please connect your PostgreSQL database first."
        )

    else:

        try:

            existing_tables = get_existing_tables()

            available_tables = [
                table
                for table in TABLES
                if table in existing_tables
            ]

            if not available_tables:

                st.warning(
                    "No project tables found."
                )

            else:

                # --------------------------------------------
                # DATABASE SUMMARY
                # --------------------------------------------

                st.markdown(
                    "### 📊 DATABASE SUMMARY"
                )

                total_records = 0

                table_summary = []

                for table in available_tables:

                    record_count = get_table_count(
                        table
                    )

                    total_records += record_count

                    table_summary.append({

                        "Table Name": table,

                        "Total Records": record_count

                    })

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "📁 Available Tables",
                        format_number(
                            len(available_tables)
                        )
                    )

                with col2:

                    st.metric(
                        "🗃️ Total Records",
                        format_number(total_records)
                    )

                with col3:

                    st.metric(
                        "⚙️ Database",
                        "PostgreSQL"
                    )

                # --------------------------------------------
                # TABLE SUMMARY
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 📋 TABLE RECORD SUMMARY"
                )

                summary_df = pd.DataFrame(
                    table_summary
                )

                st.dataframe(
                    summary_df,
                    use_container_width=True,
                    hide_index=True
                )

                # --------------------------------------------
                # TABLE RECORD CHART
                # --------------------------------------------

                fig_tables = px.bar(
                    summary_df,
                    x="Table Name",
                    y="Total Records",
                    color="Table Name",
                    text="Total Records",
                    title="Records by Database Table",
                    template="plotly_dark"
                )

                fig_tables.update_layout(
                    plot_bgcolor="#102B43",
                    paper_bgcolor="#102B43",
                    font_color="white",
                    showlegend=False
                )

                st.plotly_chart(
                    fig_tables,
                    use_container_width=True
                )

                # --------------------------------------------
                # SELECT TABLE
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 🔎 EXPLORE DATABASE TABLE"
                )

                selected_table = st.selectbox(
                    "Select Table",
                    available_tables,
                    key="explorer_table_selection"
                )

                # --------------------------------------------
                # COLUMN INFORMATION
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 🧾 TABLE STRUCTURE"
                )

                structure_df = get_table_columns(
                    selected_table
                )

                if not structure_df.empty:

                    st.dataframe(
                        structure_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.metric(
                        "Total Columns",
                        format_number(
                            len(structure_df)
                        )
                    )

                else:

                    st.warning(
                        "No column information available."
                    )

                # --------------------------------------------
                # SELECT RECORD COUNT
                # --------------------------------------------

                selected_table_count = get_table_count(
                    selected_table
                )

                st.markdown("---")

                st.markdown(
                    "### 📊 SELECTED TABLE INFORMATION"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Selected Table",
                        selected_table
                    )

                with col2:

                    st.metric(
                        "Total Records",
                        format_number(
                            selected_table_count
                        )
                    )

                # --------------------------------------------
                # DATA PREVIEW LIMIT
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 👀 TABLE DATA PREVIEW"
                )

                preview_limit = st.selectbox(
                    "Number of Records to Preview",
                    [10, 25, 50, 100, 500],
                    index=2,
                    key="database_preview_limit"
                )

                preview_query = sql.SQL(
                    "SELECT * FROM {} LIMIT %s"
                ).format(
                    sql.Identifier(
                        selected_table
                    )
                )

                connection = None

                try:

                    connection = get_connection()

                    preview_df = pd.read_sql_query(
                        preview_query.as_string(
                            connection
                        ),
                        connection,
                        params=(preview_limit,)
                    )

                finally:

                    if connection:

                        connection.close()

                if not preview_df.empty:

                    st.dataframe(
                        preview_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    download_csv(
                        preview_df,
                        f"{selected_table}_preview.csv"
                    )

                else:

                    st.info(
                        "No records available in this table."
                    )

                # --------------------------------------------
                # TABLE DATA TYPES
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 🔧 COLUMN DATA TYPE DETAILS"
                )

                type_chart_df = structure_df.copy()

                if not type_chart_df.empty:

                    type_count_df = (
                        type_chart_df["data_type"]
                        .value_counts()
                        .reset_index()
                    )

                    type_count_df.columns = [
                        "Data Type",
                        "Column Count"
                    ]

                    fig_types = px.pie(
                        type_count_df,
                        names="Data Type",
                        values="Column Count",
                        title="Column Data Type Distribution",
                        hole=0.4,
                        template="plotly_dark"
                    )

                    fig_types.update_layout(
                        paper_bgcolor="#102B43",
                        font_color="white"
                    )

                    st.plotly_chart(
                        fig_types,
                        use_container_width=True
                    )

                # --------------------------------------------
                # DATABASE INFORMATION
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 🐘 POSTGRESQL INFORMATION"
                )

                if st.session_state.db_version:

                    st.code(
                        st.session_state.db_version,
                        language="text"
                    )

        except Exception as error:

            st.error(
                "Database Explorer could not be loaded."
            )

            st.exception(error)


# ============================================================
# PART 6 - FINAL FOOTER + APP COMPLETION
# ============================================================


# ============================================================
# PROJECT INFORMATION SECTION
# ============================================================

st.markdown("---")

with st.expander(
    "📁 ABOUT TENNIS IQ PROJECT"
):

    st.markdown(
        """
        <div style="
            background:linear-gradient(
                135deg,
                #102B43,
                #064E3B
            );
            padding:22px;
            border-radius:14px;
            border:1px solid #42E8A5;
        ">

            <h2 style="
                color:#42E8A5;
                text-align:center;
            ">
                🎾 TENNIS IQ
            </h2>

            <h3 style="
                color:white;
                text-align:center;
            ">
                SPORTS ANALYTICS PLATFORM
            </h3>

            <p style="
                color:#CBD5E1;
                text-align:center;
            ">
                Game Analytics: Unlocking Tennis Data
                with Sportradar API
            </p>

            <hr>

            <h3 style="color:#FACC15;">
                PROJECT TECHNOLOGIES
            </h3>

            <p style="color:#E2E8F0;">
                Python | Streamlit | PostgreSQL |
                Supabase | Sportradar API | Plotly
            </p>

            <h3 style="color:#FACC15;">
                PROJECT MODULES
            </h3>

            <p style="color:#E2E8F0;">
                • Competition Analysis<br>
                • Venue Analysis<br>
                • Player Rankings<br>
                • SQL Insights<br>
                • Data Quality<br>
                • Database Explorer
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATABASE CONNECTION SUMMARY
# ============================================================

if st.session_state.db_connected:

    st.markdown("---")

    st.markdown(
        """
        <h3 style="color:#42E8A5;">
            🟢 DATABASE STATUS
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "PostgreSQL database connection is active."
    )

else:

    st.markdown("---")

    st.info(
        "Connect your PostgreSQL database to access "
        "all TENNIS IQ dashboard features."
    )


# ============================================================
# FINAL FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        background:linear-gradient(
            90deg,
            #06111F,
            #064E3B,
            #102B43
        );
        padding:25px;
        border-radius:14px;
        border:1px solid #267B75;
        margin-top:25px;
        text-align:center;
    ">

        <h2 style="
            color:#42E8A5;
            margin-bottom:5px;
        ">
            🎾 TENNIS IQ
        </h2>

        <p style="
            color:#FFFFFF;
            font-size:14px;
            letter-spacing:2px;
        ">
            SPORTS ANALYTICS PLATFORM
        </p>

        <p style="
            color:#CBD5E1;
            font-size:13px;
        ">
            Game Analytics | Unlocking Tennis Data
            with Sportradar API
        </p>

        <hr style="border-color:#267B75;">

        <p style="
            color:#94A3B8;
            font-size:12px;
        ">
            Built with Python • Streamlit • PostgreSQL • Plotly
        </p>

        <p style="
            color:#42E8A5;
            font-size:12px;
            font-weight:bold;
        ">
            DATA • ANALYTICS • INSIGHTS
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# END OF TENNIS IQ APPLICATION
# ============================================================