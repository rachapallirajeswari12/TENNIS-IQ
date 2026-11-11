# 🎾 TENNIS IQ – Sports Analytics Platform

## Game Analytics: Unlocking Tennis Data with Sportradar API

### Project Overview

TENNIS IQ is a tennis sports analytics platform developed using Python, PostgreSQL, SQL, and Streamlit.

The project transforms structured Sportradar JSON data into relational database tables and presents meaningful insights through an interactive dashboard.

### Project Objectives

- Analyze tennis competitions and categories.
- Explore venues, cities, countries, and complexes.
- Analyze competitor rankings and ranking points.
- Store and manage data using PostgreSQL.
- Generate analytical insights using SQL queries.
- Present results through interactive visualizations.

### Technologies Used

- Python
- Streamlit
- Pandas
- PostgreSQL
- SQL
- Psycopg2
- Plotly
- Sportradar JSON data

### Live Dashboard

**[🚀 Open TENNIS IQ Live Dashboard](https://rachapallirajeswari12-tennis-iq-app-049wyo.streamlit.app/)**

### Dashboard Features

1. **Overview** – Key project statistics and summary metrics.
2. **Competition Analysis** – Competition and category analysis.
3. **Venue Analysis** – Venue, city, country, and complex analysis.
4. **Player Rankings** – Competitor rankings and ranking points.
5. **SQL Insights** – SQL queries and analytical results.
6. **Data Quality** – Data validation and quality checks.
7. **Database Explorer** – Explore database tables and records.

### Database Overview

The PostgreSQL database contains six tables:

| Table | Records |
|---|---:|
| Categories | 18 |
| Competitions | 6,699 |
| Complexes | 780 |
| Venues | 4,139 |
| Competitor | 1,000 |
| Competitor Rankings | 1,000 |

**Total Records: 13,636**

### Main Project Files

| File / Folder | Description |
|---|---|
| `app.py` | Main Streamlit dashboard |
| `queries.py` | SQL query library used by the dashboard |
| `queries.sql` | SQL analysis queries |
| `insights.txt` | Key analytical findings |
| `requirements.txt` | Python dependencies |
| `.streamlit/` | Streamlit configuration |
| `assets/` | Dashboard visual assets |

### Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/rachapallirajeswari12/TENNIS-IQ.git
```

**2. Navigate to the project folder**

```bash
cd TENNIS-IQ
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure the database**

Configure your PostgreSQL or Supabase database connection using the application's supported configuration.

Ensure the six project tables are available and populated before running the dashboard.

**5. Run the application**

```bash
streamlit run app.py
```

### Key Project Outcomes

- 6,699 competitions analyzed.
- 4,139 venues explored.
- 1,000 competitor records processed.
- 1,000 competitor ranking records analyzed.
- 13,636 total database records.
- Interactive dashboard with seven analytical sections.

### Project Type

Major Team Project – 4 Members

### Data Source

Sportradar Tennis API:

- Competitions
- Complexes
- Doubles Competitor Rankings

https://developer.sportradar.com/tennis/reference/competitions

### Conclusion

TENNIS IQ demonstrates how tennis data can be collected, transformed, stored, analyzed, and presented through an interactive analytics platform using Python, PostgreSQL, SQL, and Streamlit.