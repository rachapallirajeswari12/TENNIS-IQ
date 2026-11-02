\# 🎾 TENNIS IQ – Sports Analytics Platform



\## Game Analytics: Unlocking Tennis Data with Sportradar API



\### 📌 Project Overview

TENNIS IQ is a sports analytics platform developed to explore and analyze tennis-related data using Python, PostgreSQL, SQL, and Streamlit.



The project focuses on competition analysis, venue analysis, and doubles competitor rankings. It transforms structured JSON data into relational database tables and presents meaningful insights through an interactive dashboard.



\### 🎯 Project Objectives

\- Analyze tennis competitions and categories.

\- Explore venues, cities, countries, and complexes.

\- Analyze doubles competitor rankings and ranking points.

\- Store and manage structured data using PostgreSQL.

\- Generate analytical insights using SQL.

\- Present data through interactive visualizations.



\### 🛠️ Technologies Used

\- Python

\- Streamlit

\- Pandas

\- PostgreSQL

\- SQL

\- Psycopg2

\- Sportradar API JSON data



\### 📂 Project Files



| File | Description |

|---|---|

| `app.py` | Streamlit dashboard application |

| `competitions.json` | Competition dataset |

| `complexes.json` | Complexes and venues dataset |

| `double\_competitors\_rankings.json` | Doubles competitor rankings dataset |

| `tennis\_analytics.sql` | Database schema and SQL queries |

| `requirements.txt` | Required Python libraries |



\### 🗄️ Database Overview



The PostgreSQL database contains six tables:



| Table Name | Records |

|---|---:|

| Categories | 18 |

| Competitions | 6,699 |

| Complexes | 780 |

| Venues | 4,139 |

| Competitor | 1,000 |

| Competitor Rankings | 1,000 |



\### 📊 Dashboard Features



1\. \*\*Overview\*\* – Key project statistics and summary metrics.

2\. \*\*Competition Analysis\*\* – Competition details and category-based analysis.

3\. \*\*Venue Analysis\*\* – Venue, city, country, and timezone insights.

4\. \*\*Doubles Player Rankings\*\* – Doubles player leaderboard and ranking points.

5\. \*\*SQL Insights\*\* – Analytical SQL queries and results.

6\. \*\*Data Quality\*\* – Data validation and quality checks.

7\. \*\*Database Explorer\*\* – Explore database tables and records.



\### ⚙️ Installation and Setup



\*\*1. Clone the repository\*\*



```bash

git clone https://github.com/rachapallirajeswari12/TENNIS-IQ.git

```



\*\*2. Navigate to the project folder\*\*



```bash

cd TENNIS-IQ

```



\*\*3. Install dependencies\*\*



```bash

pip install -r requirements.txt

```



\*\*4. Configure PostgreSQL\*\*



Create a PostgreSQL database named:



`tennis\_analytics`



Execute the SQL script `tennis\_analytics.sql` only when setting up a new database. Do not recreate tables in an existing populated database.



\*\*5. Run the Streamlit application\*\*



```bash

streamlit run app.py

```



Enter your PostgreSQL connection details in the application sidebar.



\### 📈 Key Project Outcomes



\- 6,699 competitions analyzed.

\- 4,139 venues explored.

\- 1,000 doubles competitors analyzed.

\- 74 player countries represented.

\- Interactive dashboard with seven analytical sections.



\### 👥 Project Type

Major Team Project



\### 🔗 Data Source

Sportradar Tennis API documentation:  

https://developer.sportradar.com/tennis/reference/competitions



https://developer.sportradar.com/tennis/reference/complexes



https://developer.sportradar.com/tennis/reference/doubles-competitor-rankings



\### 🚀 Conclusion

TENNIS IQ demonstrates how sports data can be collected, structured, stored, analyzed, and presented through an interactive analytics platform using Python, PostgreSQL, SQL, and Streamlit.

