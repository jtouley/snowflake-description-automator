# Snowflake Description Automator

## What This Project Does
	•	Extracts metadata (tables, columns, existing descriptions) from Snowflake
	•	Fetches sample data for each table
	•	Uses Snowflake Cortex AI to generate column descriptions
	•	Outputs results in DBT-compatible YAML

Why? Because writing and maintaining column descriptions manually sucks.

## How to Use It

### 1️⃣ Install Dependencies
```sh
bash config/setup.sh
source venv/bin/activate
```

### 2️⃣ Configure Snowflake & Cortex AI

Update config/config.yaml and remove .example:
```yaml
snowflake:
  user: "your_user"
  password: "your_password"
  account: "your_account"
  warehouse: "your_warehouse"
  database: "your_database"
  schema: "your_schema"

cortex_ai:
  model: "snowflake-arctic"
```
### 3️⃣ Run the Script
```sh
python src/main.py
```
This will:
✅ Pull metadata from Snowflake
✅ Retrieve sample data
✅ Use Cortex AI to generate descriptions
✅ Write YAML files to dbt_schemas/

## How This Works (Code Structure)

snowflake-description-automator/
│── config/
│   ├── config.yaml              # Snowflake & Cortex AI credentials
│── src/
│   ├── main.py                  # Orchestrates everything
│   ├── snowflake_connector.py    # Queries Snowflake for metadata & sample data
│   ├── cortex_ai.py              # Calls Snowflake Cortex AI to generate descriptions
│   ├── dbt_formatter.py          # Converts metadata into DBT YAML
│── tests/
│   ├── test_snowflake.py         # Tests Snowflake connection & queries
│   ├── test_cortex_ai.py         # Tests AI-generated descriptions
│   ├── test_dbt_formatter.py     # Tests DBT YAML output
│── dbt_schemas/                  # Where YAML files get saved
│── requirements.txt              # Dependencies
│── README.md                     # This file

## How to Contribute

### 1️⃣ Clone & Create a Branch
```sh
git clone https://github.com/jtouley/snowflake-description-automator.git
cd snowflake-description-automator
git checkout -b feature/new-improvement
```
### 2️⃣ Make Your Changes
	•	If you’re fixing Snowflake queries, edit snowflake_connector.py
	•	If you’re improving AI descriptions, edit cortex_ai.py
	•	If you’re enhancing YAML formatting, edit dbt_formatter.py

### 3️⃣ Run Tests
```sh
pytest tests/
```
### 4️⃣ Format & Lint
```sh
pre-commit run --all-files
```
### 5️⃣ Commit & Push
```sh
git add .
git commit -m "Added feature XYZ"
git push origin feature/new-improvement
```
Then, open a Pull Request (PR) on GitHub.

## Common Issues & Fixes

**Problem**: ModuleNotFoundError: No module named 'src'
✔ **Fix**: Run export PYTHONPATH=$(pwd)/src before running tests

**Problem**: Cortex AI isn’t generating descriptions
✔ **Fix**: Check if Snowflake Cortex AI is enabled for your account

**Problem**: YAML output is missing descriptions
✔ **Fix**: Make sure sample data exists & AI is returning results

What’s Next

🔹 Parallel processing for large schemas
🔹 Improve AI-generated descriptions
🔹 Better error handling for Snowflake & Cortex AI failures

🔥 Questions? Open an issue or PR. Otherwise, start coding. 🚀