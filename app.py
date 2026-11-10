# ============================================================
#  TENNIS IQ - SPORTS ANALYTICS PLATFORM
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
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM DESIGN - TENNIS IQ
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F3F7FC;
    color: #14213D;
}

/* PLOTLY GRAPH TEXT - BLACK COLOR */
.js-plotly-plot .plotly text {
    fill: #000000 !important;
}

.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .g-xtitle,
.js-plotly-plot .g-ytitle,
.js-plotly-plot .legend text {
    fill: #000000 !important;
}

.js-plotly-plot .gtitle {
    fill: #000000 !important;
}

/* DATA QUALITY TABLE - WHITE TEXT */
div[data-testid="stDataFrame"] th,
div[data-testid="stDataFrame"] td,
div[data-testid="stDataFrame"] [role="columnheader"],
div[data-testid="stDataFrame"] [role="gridcell"] {
    color: #FFFFFF !important;
}

/* MAIN CONTENT TEXT */

.main .block-container p,
.main .block-container label,
.main .block-container span {
    color: #172B4D;
}

/* OVERVIEW DASHBOARD - WHITE */
.main h1,
.main h2,
.main h3 {
    color: #FFFFFF !important;
}

/* DATABASE SUCCESS MESSAGE - WHITE */
[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #FFFFFF !important;
}

/* TECHNOLOGY STACK - WHITE TEXT */
div:has(> h4) {
    color: #FFFFFF !important;
}

div:has(> h4) h4,
div:has(> h4) p {
    color: #FFFFFF !important;
}

.main h1, .main h2, .main h3 {
    color: #063B78 !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #75C9F5, #3B9DDB, #1676B8) !important;
    border-right: 2px solid #A9DFFF;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 900 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: #0B315C !important;
    border: 1px solid #245582 !important;
    border-radius: 9px;
    padding: 9px 12px;
    margin-bottom: 4px;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #0756A5 !important;
    border-color: #61B5FF !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #0876F9 !important;
    border: 1px solid #67B7FF !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label * {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* SECTION HEADINGS */

.main h2 {
    color: #FFFFFF !important;
}

/* KPI METRIC CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #E5F0FF, #D5E6FF);
    border: 1px solid #A9CCFA;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 6px rgba(10, 55, 100, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #102B55 !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    color: #082D69 !important;
    font-weight: 900 !important;
}

/* COLOURFUL KPI CARDS */

[data-testid="stMetric"]:nth-child(4n+1) {
    background: linear-gradient(135deg, #E0EDFF, #C5DCFF) !important;
    border: 1px solid #8DBBFA;
}

[data-testid="stMetric"]:nth-child(4n+2) {
    background: linear-gradient(135deg, #DDF7E8, #BDECCF) !important;
    border: 1px solid #8BD5A8;
}

[data-testid="stMetric"]:nth-child(4n+3) {
    background: linear-gradient(135deg, #F0E5FF, #DDC8FF) !important;
    border: 1px solid #B99AEF;
}

[data-testid="stMetric"]:nth-child(4n) {
    background: linear-gradient(135deg, #FFF0DB, #FFDCB0) !important;
    border: 1px solid #F2BD79;
}

/* BUTTONS */

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #0876F9, #0756B5);
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    font-weight: 700;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #064A9B;
    color: #FFFFFF !important;
}

/* INPUTS AND FILTERS */

.stTextInput input,
.stNumberInput input {
    background: #FFFFFF !important;
    color: #102B55 !important;
    border: 1px solid #B8CCE8 !important;
}

[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #102B55 !important;
    border-color: #B8CCE8 !important;
}

/* PROFESSIONAL DROPDOWN FILTERS */

[data-baseweb="select"] > div {
    min-height: 44px !important;
    border: 1px solid #8DBBEB !important;
    border-radius: 9px !important;
    box-shadow: 0 2px 5px rgba(6, 59, 120, 0.06);
}

[data-baseweb="select"] > div:hover {
    border-color: #0876C9 !important;
}

[data-baseweb="tag"] {
    background: #DCEBFF !important;
    color: #063B78 !important;
    border: 1px solid #A9CCFA !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}

[data-baseweb="popover"] {
    border: 1px solid #B8CCE8 !important;
    border-radius: 9px !important;
    box-shadow: 0 5px 15px rgba(6, 59, 120, 0.12) !important;
}

/* SCROLLABLE DROPDOWN OPTIONS */

div[data-baseweb="popover"] [role="listbox"] {
    max-height: 250px !important;
    overflow-y: auto !important;
}

div[data-baseweb="popover"] ul[role="listbox"] {
    max-height: 250px !important;
    overflow-y: auto !important;
}

div[data-baseweb="popover"] [role="option"] {
    min-height: 38px !important;
}


/* DATA TABLES */

[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #AFCBEA !important;
    border-radius: 12px !important;
    padding: 6px !important;
    box-shadow: 0 4px 12px rgba(6, 59, 120, 0.08);
    overflow: hidden;
}

[data-testid="stDataFrame"] canvas {
    border-radius: 8px;
}

[data-testid="stDataFrame"] button {
    color: #063B78 !important;
}

/* CHART CONTAINERS */

[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border: 1px solid #C5D9F0 !important;
    border-radius: 14px !important;
    padding: 12px !important;
    box-shadow: 0 4px 12px rgba(6, 59, 120, 0.08);
    transition: box-shadow 0.2s ease;
}

[data-testid="stPlotlyChart"]:hover {
    box-shadow: 0 7px 18px rgba(6, 59, 120, 0.14);
}

/* EXPANDERS */

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #AFCBEA !important;
    border-radius: 12px !important;
    box-shadow: 0 3px 10px rgba(6, 59, 120, 0.07);
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #063B78 !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] summary:hover {
    color: #0876C9 !important;
}

/* ALERTS */

[data-testid="stAlert"] {
    border-radius: 9px;
}

/* DIVIDERS */

hr {
    border-color: #B8CCE8;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #526783;
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
        st.write(
            "DEBUG - Secrets sections:",
            list(st.secrets.keys())
        )

        st.write(
            "DEBUG - PostgreSQL section found:",
            "postgresql" in st.secrets
        )

        config = dict(st.secrets["postgresql"])

        required_keys = [
            "host", "port", "database",
            "user", "password", "sslmode"
        ]

        missing_keys = [
            key for key in required_keys
            if key not in config
        ]

        if missing_keys:
            st.error(
                f"Missing database settings: {missing_keys}"
            )
            return None

        return config

    except Exception as error:
        st.error(
            f"Supabase Secrets Error: {error}"
        )
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

    st.html(f"""
        <div style="
            background:linear-gradient(100deg,#063B78,#0876C9,#1595D4);
            padding:15px 22px;
            border-radius:10px;
            border-left:6px solid #D7FF64;
            margin:20px 0 12px 0;
            box-shadow:0 3px 10px rgba(6,59,120,0.15);
        ">
            <div style="
                color:#FFFFFF !important;
                -webkit-text-fill-color:#FFFFFF !important;
                font-size:21px;
                font-weight:800;
                margin:0;
                letter-spacing:0.5px;
                text-shadow:0 1px 3px rgba(0,0,0,0.3);
            ">
                {title}
            </div>
        </div>
    """)

    if subtitle:
        st.html(f"""
            <p style="
                color:#526783 !important;
                -webkit-text-fill-color:#526783 !important;
                font-size:14px;
                margin:5px 0 14px 3px;
            ">
                {subtitle}
            </p>
        """)

# ============================================================
# CSV DOWNLOAD HELPER
# ============================================================

def download_csv(dataframe, file_name):

    if dataframe is not None and not dataframe.empty:

        csv_data = dataframe.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label=" Download CSV",
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
# APPLICATION HEADER - TENNIS IQ
# ============================================================


st.html(f"""
<div style="
    background:
    radial-gradient(ellipse at 50% 0%, rgba(70,160,255,0.35), transparent 55%),
    linear-gradient(135deg,#020B1C 0%,#063B70 50%,#04152D 100%);
    padding:18px 15px 10px;
    border:2px solid #4598DD;
    border-bottom:5px solid #D7FF64;
    border-radius:18px;
    margin-bottom:22px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,25,65,0.25);
">

    <div style="
    display:flex;
    flex-direction:row;
    align-items:center;
    justify-content:center;
    gap:25px;
    flex-wrap:nowrap;
    width:100%;
">

        
        <!-- TILTED TENNIS RACKET AND SIDE BALL -->
        <div style="position:relative;width:145px;height:175px;flex-shrink:0;">

            <!-- TILTED RACKET -->
            <div style="
                position:absolute;
                left:18px;
                top:5px;
                width:75px;
                height:160px;
                transform:rotate(22deg);
                transform-origin:center center;
            ">

                <!-- RACKET HEAD -->
                <div style="
                    position:absolute;
                    left:5px;
                    top:0;
                    width:66px;
                    height:82px;
                    border:7px solid #39A0FF;
                    border-radius:50%;
                    box-sizing:border-box;
                    background:
                    repeating-linear-gradient(90deg,transparent 0px,transparent 8px,#EAF4FF 9px,#EAF4FF 10px),
                    repeating-linear-gradient(0deg,transparent 0px,transparent 8px,#EAF4FF 9px,#EAF4FF 10px);
                "></div>

                <!-- CONNECTED HANDLE -->
                <div style="
                    position:absolute;
                    left:32px;
                    top:74px;
                    width:13px;
                    height:60px;
                    background:#FFFFFF;
                    border-radius:4px;
                "></div>

                <!-- GRIP -->
                <div style="
                    position:absolute;
                    left:30px;
                    top:120px;
                    width:17px;
                    height:29px;
                    background:#B7FF00;
                    border:1px solid white;
                    border-radius:4px;
                "></div>

            </div>

            <!-- BALL BESIDE RACKET -->
            <div style="
                position:absolute;
                right:2px;
                top:82px;
                width:34px;
                height:34px;
                background:#D7FF00;
                border:2px solid white;
                border-radius:50%;
                box-sizing:border-box;
                box-shadow:0 3px 8px rgba(0,0,0,0.4);
            ">
                <div style="
                    position:absolute;
                    left:8px;
                    top:3px;
                    width:13px;
                    height:24px;
                    border-left:2px solid white;
                    border-radius:50%;
                    transform:rotate(25deg);
                "></div>
            </div>

       </div>

    <!-- TENNIS IQ HEADING -->
       <div style="
    text-align:center;
    flex:0 1 auto;
    min-width:0;
">

            <div style="
                color:#D7FF64;
                font-size:11px;
                font-weight:800;
                letter-spacing:4px;
                margin-bottom:7px;
            ">
                GAME ANALYTICS
            </div>

            <h1 style="
                color:white;
                font-size:36px;
                font-weight:900;
                letter-spacing:4px;
                margin:0;
                line-height:1.15;
            ">
                TENNIS <span style="color:#D7FF64;">IQ</span>
            </h1>

            <h3 style="
                color:#EAF4FF;
                font-size:17px;
                letter-spacing:3px;
                margin:9px 0;
            ">
                SPORTS ANALYTICS PLATFORM
            </h3>

            <p style="color:#D9EAFE;font-size:13px;margin:0;">
                Game Analytics | Unlocking Tennis Data with Sportradar API
            </p>

        </div>

    </div>

    <!-- TECHNOLOGY STRIP -->
    <div style="
        border-top:1px solid rgba(255,255,255,0.30);
        margin-top:14px;
        padding:8px 5px 2px;
        color:white;
        font-size:12px;
        font-weight:800;
        letter-spacing:1.5px;
    ">
        PYTHON &nbsp; | &nbsp;
        STREAMLIT &nbsp; | &nbsp;
        POSTGRESQL &nbsp; | &nbsp;
        PLOTLY &nbsp; | &nbsp;
        SPORTRADAR API
        <span style="color:#D7FF64;">
            &nbsp; | &nbsp; DATA ANALYTICS INSIGHTS
        </span>
    </div>

</div>
""")

# ============================================================
# SIDEBAR BRANDING
# ============================================================

st.sidebar.html(
    """
    <div style="
        text-align:center;
        padding:18px 5px;
        background:linear-gradient(135deg,#041B3A,#073B70,#06264B);
        border-radius:14px;
        border:1px solid #1685D8;
        box-shadow:0 4px 12px rgba(0,0,0,0.20);
    ">

        <h1 style="
            color:#FFFFFF !important;
            margin:0;
            font-size:27px;
            font-weight:900;
        ">
            TENNIS IQ
        </h1>

        <p style="
            color:#FFFFFF !important;
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            margin-bottom:0;
        ">
            SPORTS ANALYTICS
        </p>

    </div>
    """
)

# ============================================================
# DATABASE CONNECTION STATUS - BACKGROUND
# ============================================================

cloud_config = get_cloud_config()

if cloud_config:

    st.session_state.db_config = cloud_config

    try:

        test_connection = get_connection()

        with test_connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]

        test_connection.close()

        st.session_state.db_connected = True
        st.session_state.db_version = db_version

    except Exception as error:

        st.session_state.db_connected = False
        st.session_state.db_version = None

else:

    st.session_state.db_connected = False


# ============================================================
# NAVIGATION MENU
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(

    "## NAVIGATION"
)

PAGES = [
    "Overview",
    "Competition Analysis",
    "Venue Analysis",
    "Player Rankings",
    "SQL Insights",
    "Data Quality",
    "Database Explorer"
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

st.sidebar.html(
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
             PROJECT DETAILS
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
            Python  Streamlit  PostgreSQL
        </p>

        <p style="color:#7DD3FC;font-size:12px;">
            Sportradar API  Plotly
        </p>
    </div>
    """
    )


# ============================================================
# SIDEBAR FOOTER
# ============================================================

st.sidebar.html(
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
    """
   )


# ============================================================
# OVERVIEW DASHBOARD
# ============================================================

if selected_page == "Overview":

    st.html("""
    <div style="
        background:linear-gradient(100deg,#063B78,#0876C9,#1595D4);
        padding:15px 22px;
        border-radius:10px;
        border-left:6px solid #D7FF64;
        margin:20px 0 12px 0;
    ">
        <h2 style="
            color:white !important;
            -webkit-text-fill-color:white !important;
            font-size:21px;
            font-weight:800;
            margin:0;
            opacity:1;
        ">OVERVIEW DASHBOARD</h2>
    </div>
    """)

    st.markdown(
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
                "### DATABASE PERFORMANCE"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    label=" Total Tables",
                    value=format_number(total_tables)
                )

            with col2:

                st.metric(
                    label=" Total Records",
                    value=format_number(total_records)
                )

            with col3:

                st.metric(
                    label="Available Tables",
                    value=format_number(len(available_tables))
                )

            with col4:

                st.metric(
                    label="Missing Tables",
                    value=format_number(len(missing_tables))
                )

            st.markdown("---")

            # ------------------------------------------------
            # TABLE RECORD DISTRIBUTION
            # ------------------------------------------------

            st.markdown(
                "### TABLE RECORD DISTRIBUTION"
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
                        template="plotly_white"
                    )

                    fig.update_layout(
                        plot_bgcolor="#FFFFFF",                        paper_bgcolor="#FFFFFF",                        font_color="#1E293B",
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
                        template="plotly_white"
                    )

                    fig_pie.update_layout(
                        paper_bgcolor="#FFFFFF",                        font_color="#1E293B"
                    )

                    st.plotly_chart(
                        fig_pie,
                        use_container_width=True
                    )

                # --------------------------------------------
                # TABLE SUMMARY
                # --------------------------------------------

                st.markdown(
                    "###  DATABASE TABLE SUMMARY"
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
                "###  DATABASE TABLE STATUS"
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

                                st.html("""
                    <div style="
                        background:#04152D;
                        color:#FFFFFF;
                        padding:18px 20px;
                        border-radius:12px;
                        border-left:6px solid #D7FF64;
                        font-size:16px;
                        font-weight:700;
                        width:100%;
                        box-sizing:border-box;
                        box-shadow:0 4px 15px rgba(0,0,0,0.20);
                    ">
                        <span style="color:#FFFFFF;">
                            All six expected project tables are available!
                        </span>
                    </div>
                """)

            # ------------------------------------------------
            # PROJECT TECHNOLOGY STACK
            # ------------------------------------------------

            st.markdown("---")

            st.markdown(
                "###   TECHNOLOGY STACK"
            )

            tech1, tech2, tech3, tech4 = st.columns(4)

            with tech1:
                st.markdown(
                    """
                    <div style="background:#1769AA; color:white; padding:18px; border-radius:10px; text-align:center;">
                        <h4 style="color:white;">Python</h4>
                        <p style="color:white;">Data Processing</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with tech2:
                st.markdown(
                    """
                    <div style="background:#1769AA; color:white; padding:18px; border-radius:10px; text-align:center;">
                        <h4 style="color:white;">Streamlit</h4>
                        <p style="color:white;">Dashboard Development</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with tech3:
                st.markdown(
                    """
                    <div style="background:#1769AA; color:white; padding:18px; border-radius:10px; text-align:center;">
                        <h4 style="color:white;">PostgreSQL</h4>
                        <p style="color:white;">Database Management</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with tech4:
                st.markdown(
                    """
                    <div style="background:#1769AA; color:white; padding:18px; border-radius:10px; text-align:center;">
                        <h4 style="color:white;">Plotly</h4>
                        <p style="color:white;">Data Visualization</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ------------------------------------------------
            # OVERVIEW FOOTNOTE
            # ------------------------------------------------

            st.html(
                """
                <div style="
                    background:#142D42;
                    padding:15px;
                    border-radius:10px;
                    border-left:4px solid #42E8A5;
                    margin-top:20px;
                ">
                    <p style="color:#42E8A5;font-weight:bold;">
                         TENNIS IQ - DATA INSIGHTS
                    </p>

                    <p style="color:#CBD5E1;font-size:13px;">
                        This dashboard provides an overview
                        of the tennis database, table availability,
                        record distribution and technology stack.
                    </p>
                </div>
                """
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

elif selected_page == "Competition Analysis":

    section_header(
        "  COMPETITION ANALYSIS",
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
                        "###  COMPETITION OVERVIEW"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "  Total Competitions",
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
                            " Competition Types",
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
                            " Gender Categories",
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
                            " Categories",
                            format_number(total_categories)
                        )

                    st.markdown("---")

                    # ----------------------------------------
                    # SCROLLABLE FILTER DROPDOWN OPTIONS
                    # ----------------------------------------

                    st.markdown(
                        """
                        <style>
                        div[data-baseweb="popover"] ul[role="listbox"] {
                            max-height: 220px !important;
                            overflow-y: auto !important;
                        }

                        div[data-baseweb="popover"] [role="listbox"] {
                            max-height: 220px !important;
                            overflow-y: auto !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                   # ----------------------------------------
                    # FILTER SECTION
                    # ----------------------------------------

                    st.markdown(
                        "### COMPETITION FILTERS"
                    )

                    filtered_competitions = competition_df.copy()

                    filter_col1, filter_col2, filter_col3 = st.columns(3)

                    # COMPETITION TYPE FILTER
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
                                    filtered_competitions["type"]
                                    .astype(str).isin(selected_types)
                                ]
                            )
                    # GENDER FILTER
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
                                    filtered_competitions["gender"]
                                    .astype(str).isin(selected_genders)
                                ]
                            )

                   
                    # COMPETITION NAMES FILTER
                    if "name" in competition_columns:

                        st.markdown("### COMPETITION NAME SEARCH")

                        competition_name_options = sorted(
                            filtered_competitions["name"]
                            .dropna()
                            .astype(str)
                            .unique()
                            .tolist()
                        )

                        selected_competition_names = st.multiselect(
                            "Select Competition Names",
                            competition_name_options,
                            default=[],
                            key="competition_names_filter",
                            placeholder="Search competition names"
                        )

                        if selected_competition_names:

                            filtered_competitions = (
                                filtered_competitions[
                                    filtered_competitions["name"]
                                    .astype(str).isin(
                                        selected_competition_names
                                    )
                                ]
                            )

                                
                    # ----------------------------------------
                    # FILTERED KPI
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "###  FILTERED RESULTS"
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
                            "###  COMPETITION TYPE DISTRIBUTION"
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
                            template="plotly_white"
                        )

                        fig_type.update_layout(
                            plot_bgcolor="#FFFFFF",                            paper_bgcolor="#FFFFFF",                            font_color="#1E293B",
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
                            "###  GENDER DISTRIBUTION"
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
                                template="plotly_white"
                            )

                            fig_gender.update_layout(
                                paper_bgcolor="#FFFFFF",                                font_color="#1E293B"
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
                                template="plotly_white"
                            )

                            fig_gender_bar.update_layout(
                                plot_bgcolor="#FFFFFF",                                paper_bgcolor="#FFFFFF",                                font_color="#1E293B",
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
                            "###  CATEGORY-WISE COMPETITIONS"
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
                                    template="plotly_white"
                                )

                                fig_category.update_layout(
                                    plot_bgcolor="#FFFFFF",                                    paper_bgcolor="#FFFFFF",                                    font_color="#1E293B",
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
                        "###  COMPETITION DATA EXPLORER"
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

elif selected_page == "Venue Analysis":

    section_header(
        " VENUE ANALYSIS",
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
                        "###  VENUE OVERVIEW"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            " Total Venues",
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
                            " Countries",
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
                            " Cities",
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
                            " Complexes",
                            format_number(complex_count)
                        )

                    st.markdown("---")

                   # ----------------------------------------
                    # VENUE FILTERS
                    # ----------------------------------------

                    st.markdown(
                        "### VENUE FILTERS"
                    )

                    filtered_venues = venue_df.copy()

                    filter_col1, filter_col2, filter_col3 = st.columns(3)

                    # COUNTRY FILTER
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
                                    filtered_venues["country_name"]
                                    .astype(str).isin(selected_countries)
                                ]
                            )

                    # CITY FILTER
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
                                    filtered_venues["city_name"]
                                    .astype(str).isin(selected_cities)
                                ]
                            )

                    # VENUE NAME FILTER
                    if "name" in venue_columns:

                        with filter_col3:

                            venue_name_options = sorted(
                                filtered_venues["name"]
                                .dropna()
                                .astype(str)
                                .unique()
                                .tolist()
                            )

                            selected_venue_names = st.multiselect(
                                "Select Venue Names",
                                venue_name_options,
                                default=[],
                                key="venue_names_filter",
                                placeholder="Search venue names"
                            )

                            if selected_venue_names:

                                filtered_venues = (
                                    filtered_venues[
                                        filtered_venues["name"]
                                        .astype(str).isin(selected_venue_names)
                                    ]
                                )

                    # ----------------------------------------
                    # FILTERED VENUE RESULTS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "###  FILTERED VENUE RESULTS"
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
                            "###  COUNTRY-WISE VENUE DISTRIBUTION"
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
                                template="plotly_white"
                            )

                            fig_country.update_layout(
                                plot_bgcolor="#FFFFFF",                                paper_bgcolor="#FFFFFF",                                font_color="#1E293B",
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
                                template="plotly_white"
                            )

                            fig_country_pie.update_layout(
                                paper_bgcolor="#FFFFFF",                                font_color="#1E293B"
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
                            "###  CITY-WISE VENUE DISTRIBUTION"
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
                            template="plotly_white"
                        )

                        fig_city.update_layout(
                            plot_bgcolor="#FFFFFF",                            paper_bgcolor="#FFFFFF",                            font_color="#1E293B",
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
                            "###  VENUE COMPLEX ANALYSIS"
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
                        "###  VENUE DATA EXPLORER"
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

elif selected_page == "Player Rankings":

    section_header(
        " PLAYER RANKINGS",
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
                            "###  RANKING OVERVIEW"
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
                                " Ranked Players",
                                format_number(total_players)
                            )

                        with col2:

                            st.metric(
                                "  Top Rank",
                                format_number(
                                    ranking_df["rank"].min()
                                )
                            )

                        with col3:

                            st.metric(
                                " Total Points",
                                format_number(total_points)
                            )

                        with col4:

                            st.metric(
                                " Average Points",
                                format_number(
                                    average_points
                                )
                            )

                        st.markdown("---")

                        # ------------------------------------
                        # PLAYER FILTERS
                        # ------------------------------------
                        
                        st.markdown(
                        "### PLAYER FILTERS"
                        )
                        
                        filtered_rankings = ranking_df.copy()
                        
                        filter_col1, filter_col2, filter_col3 = st.columns(3)
                        
                        # COUNTRY FILTER
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
                                        filtered_rankings["country"]
                                        .astype(str).isin(selected_countries)
                                        ]
                                )
                        
                        # TOP RANKINGS FILTER
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
                        
                        # PLAYER NAME FILTER
                        if "name" in ranking_df.columns:
                        
                            with filter_col3:
                        
                                player_options = sorted(
                                    filtered_rankings["name"]
                                    .dropna()
                                    .astype(str)
                                    .unique()
                                    .tolist()
                                    )
                        
                                selected_players = st.multiselect(
                                    "Select Player Names",
                                    player_options,
                                    default=[],
                                    key="ranking_player_names_filter",
                                    placeholder="Search player names"
                                    )
                        
                                if selected_players:
                        
                                    filtered_rankings = (
                                        filtered_rankings[
                                            filtered_rankings["name"]
                                            .astype(str).isin(selected_players)
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
                            "###   TOP 10 PLAYERS"
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
                            "###  TOP PLAYER POINTS ANALYSIS"
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
                            template="plotly_white"
                        )

                        fig_points.update_layout(
                            plot_bgcolor="#FFFFFF",                            paper_bgcolor="#FFFFFF",                            font_color="#1E293B",
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
                                "###  COUNTRY-WISE PLAYER DISTRIBUTION"
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
                                template="plotly_white"
                            )

                            fig_country.update_layout(
                                plot_bgcolor="#FFFFFF",                                paper_bgcolor="#FFFFFF",                                font_color="#1E293B",
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
                                "###  RANKING MOVEMENT ANALYSIS"
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
                                template="plotly_white"
                            )

                            fig_movement.update_layout(
                                paper_bgcolor="#FFFFFF",                                font_color="#1E293B"
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
                            "###  COMPLETE PLAYER RANKINGS"
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

elif selected_page == "SQL Insights":

    section_header(
        " SQL INSIGHTS",
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
                "###  SELECT SQL ANALYSIS"
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
                " View SQL Query"
            ):

                st.code(
                    selected_sql,
                    language="sql"
                )

            # --------------------------------------------
            # RUN SQL
            # --------------------------------------------

            if st.button(
                " RUN SQL QUERY",
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

                        st.html("""
<div style="
    background-color:#04152D;
    color:#FFFFFF;
    padding:14px 18px;
    border-radius:8px;
    border-left:5px solid #D7FF64;
    font-weight:700;
    margin:10px 0;
">
    SQL Query executed successfully!
</div>
""")

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
                    "###  SQL QUERY RESULTS"
                )

                st.html(f"""
<div style="
    background-color:#04152D;
    color:#FFFFFF;
    padding:14px 18px;
    border-radius:8px;
    border-left:5px solid #D7FF64;
    font-size:16px;
    font-weight:700;
    margin:10px 0;
">
    Query: {st.session_state.sql_query_name}
</div>
""")

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

elif selected_page == "Data Quality":

    section_header(
        " DATA QUALITY",
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
                    "###  SELECT TABLE FOR QUALITY CHECK"
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
                        "###  DATA QUALITY OVERVIEW"
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
                            " Total Rows",
                            format_number(total_rows)
                        )

                    with col2:

                        st.metric(
                            " Total Columns",
                            format_number(total_columns)
                        )

                    with col3:

                        st.metric(
                            " Missing Cells",
                            format_number(missing_cells)
                        )

                    with col4:

                        st.metric(
                            " Duplicate Rows",
                            format_number(duplicate_rows)
                        )

                    with col5:

                        st.metric(
                            " Completeness",
                            f"{completeness:.2f}%"
                        )

                    # ----------------------------------------
                    # COMPLETENESS INDICATOR
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "###  DATA COMPLETENESS"
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
                        "###  MISSING VALUES ANALYSIS"
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
                            template="plotly_white"
                        )

                        fig_missing.update_layout(
                            plot_bgcolor="#FFFFFF",                            paper_bgcolor="#FFFFFF",                            font_color="#1E293B",
                            showlegend=False
                        )

                        st.plotly_chart(
                            fig_missing,
                            use_container_width=True
                        )

                    else:

                        st.html("""
                        <div style="
                            background-color:#04152D;
                            color:#FFFFFF;
                            padding:14px 18px;
                            border-radius:8px;
                            border-left:5px solid #D7FF64;
                            font-weight:700;
                            margin:10px 0;
                        ">
                            No missing values found in the loaded sample.
                        </div>
                        """)

                    # ----------------------------------------
                    # DUPLICATE RECORD ANALYSIS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "###  DUPLICATE RECORD ANALYSIS"
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

                        st.html("""
                        <div style="
                            background-color:#04152D;
                            color:#FFFFFF;
                            padding:14px 18px;
                            border-radius:8px;
                            border-left:5px solid #D7FF64;
                            font-weight:700;
                            margin:10px 0;
                        ">
                            No completely duplicate rows found in the loaded sample.
                        </div>
                        """)

      
                    # ----------------------------------------
                    # COLUMN DATA TYPE ANALYSIS
                    # ----------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "###  COLUMN DATA TYPES"
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
                        "###  COLUMN UNIQUENESS ANALYSIS"
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
                        template="plotly_white"
                    )

                    fig_unique.update_layout(
                        plot_bgcolor="#FFFFFF",                        paper_bgcolor="#FFFFFF",                        font_color="#1E293B",
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

                    st.html("""
                    <div style="
                        background-color:#04152D;
                        color:#FFFFFF;
                        padding:14px 18px;
                        border-radius:8px;
                        border-left:5px solid #D7FF64;
                        font-size:18px;
                        font-weight:800;
                        margin:10px 0;
                    ">
                        QUALITY CHECK SUMMARY
                    </div>
                    """)

                    if missing_cells == 0:

                        st.html("""
                        <div style="
                            background-color:#04152D;
                            color:#FFFFFF;
                            padding:14px 18px;
                            border-radius:8px;
                            border-left:5px solid #D7FF64;
                            font-weight:700;
                            margin:10px 0;
                        ">
                            No missing values found in this sample.
                        </div>
                        """)

                    else:

                        st.warning(
                            f"Missing values detected: {missing_cells}"
                        )

                    if duplicate_rows == 0:

                        st.html("""
                        <div style="
                            background-color:#04152D;
                            color:#FFFFFF;
                            padding:14px 18px;
                            border-radius:8px;
                            border-left:5px solid #D7FF64;
                            font-weight:700;
                            margin:10px 0;
                        ">
                            No completely duplicate rows found in this sample.
                        </div>
                        """)

                    else:

                        st.warning(
                            f"Duplicate rows detected: {duplicate_rows}"
                        )

                    st.html("""
                    <div style="
                        background-color:#04152D;
                        color:#FFFFFF;
                        padding:14px 18px;
                        border-radius:8px;
                        border-left:5px solid #D7FF64;
                        font-weight:600;
                        margin:10px 0;
                    ">
                        Quality checks are based on a maximum of 5,000 loaded rows.
                        They do not modify or delete your database records.
                    </div>
                    """)

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

elif selected_page == "Database Explorer":

    section_header(
        " DATABASE EXPLORER",
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
                    "###  DATABASE SUMMARY"
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
                        " Available Tables",
                        format_number(
                            len(available_tables)
                        )
                    )

                with col2:

                    st.metric(
                        " Total Records",
                        format_number(total_records)
                    )

                with col3:

                    st.metric(
                        " Database",
                        "PostgreSQL"
                    )

                # --------------------------------------------
                # TABLE SUMMARY
                # --------------------------------------------

                st.markdown("---")

                st.markdown(
                    "###  TABLE RECORD SUMMARY"
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
                    template="plotly_white"
                )

                fig_tables.update_layout(
                    plot_bgcolor="#FFFFFF",                    paper_bgcolor="#FFFFFF",                    font_color="#1E293B",
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
                    "###  EXPLORE DATABASE TABLE"
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
                    "###  TABLE STRUCTURE"
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
                    "###  SELECTED TABLE INFORMATION"
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
                    "###  TABLE DATA PREVIEW"
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
                    "###  COLUMN DATA TYPE DETAILS"
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
                        template="plotly_white"
                    )

                    fig_types.update_layout(
                        paper_bgcolor="#FFFFFF",                        font_color="#1E293B"
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
                    "###  POSTGRESQL INFORMATION"
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
    " ABOUT TENNIS IQ PROJECT"
):

    st.html(
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
                 TENNIS IQ
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
                 Competition Analysis<br>
                 Venue Analysis<br>
                 Player Rankings<br>
                 SQL Insights<br>
                 Data Quality<br>
                 Database Explorer
            </p>

        </div>
        """
    )


# ============================================================
# FINAL FOOTER
# ============================================================

st.html(
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
             TENNIS IQ
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
            Built with Python  Streamlit  PostgreSQL  Plotly
        </p>

        <p style="
            color:#42E8A5;
            font-size:12px;
            font-weight:bold;
        ">
            DATA  ANALYTICS  INSIGHTS
        </p>

    </div>
    """
  )


# ============================================================
# END OF TENNIS IQ APPLICATION
# ============================================================


