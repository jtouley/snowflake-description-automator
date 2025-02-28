import snowflake.connector
import pandas as pd
import yaml
import structlog

log = structlog.get_logger()

# Load credentials from config.yaml
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

SNOWFLAKE_CONFIG = config["snowflake"]
CORTEX_MODEL = config["cortex_ai"]["model"]

# Establish Snowflake connection
def connect_to_snowflake():
    """Create and return a Snowflake connection."""
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG["user"],
        password=SNOWFLAKE_CONFIG["password"],
        account=SNOWFLAKE_CONFIG["account"],
        warehouse=SNOWFLAKE_CONFIG["warehouse"],
        database=SNOWFLAKE_CONFIG["database"],
        schema=SNOWFLAKE_CONFIG["schema"]
    )

def generate_column_descriptions(df):
    """Generates AI-powered descriptions for Snowflake table columns using Cortex AI."""
    conn = connect_to_snowflake()
    cursor = conn.cursor()

    # Prepare input data
    column_metadata = df.head(5).to_string(index=False)

    query = f"""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        '{{
            "model": "{CORTEX_MODEL}",
            "messages": [
                {{"role": "system", "content": "You are an AI assistant helping generate concise column descriptions."}},
                {{"role": "user", "content": "Generate concise descriptions for these columns: {column_metadata}"}}
            ]
        }}'
    )
    """

    try:
        cursor.execute(query)
        response = cursor.fetchone()
        return response[0] if response else "No response from Cortex AI"
    except Exception as e:
        log.error(f"Error calling Cortex AI: {e}")
        return "Error generating descriptions"
    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
    print(generate_column_descriptions(df))