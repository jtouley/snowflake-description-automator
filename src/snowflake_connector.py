import snowflake.connector
import pandas as pd
import yaml
import structlog

log = structlog.get_logger()

# Load Snowflake credentials from config
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)["snowflake"]

class SnowflakeClient:
    """Handles Snowflake connection and queries."""

    def __init__(self):
        self.conn = self.connect_to_snowflake()
        self.cursor = self.conn.cursor()
        log.info("Connected to Snowflake")

    def connect_to_snowflake(self):
        """Establish a Snowflake connection using config.yaml."""
        return snowflake.connector.connect(
            user=config["user"],
            password=config["password"],
            account=config["account"],
            warehouse=config["warehouse"],
            database=config["database"],
            schema=config["schema"]
        )

    def get_table_list(self):
        """Fetches all table names from the Snowflake schema."""
        self.cursor.execute("SHOW TABLES")
        tables = [row[0] for row in self.cursor.fetchall()]
        return tables

    def get_table_metadata(self, table_name):
        """Retrieves column metadata (including descriptions) for a given table."""
        self.cursor.execute(f"SHOW COLUMNS IN {table_name}")
        columns_df = pd.DataFrame(self.cursor.fetchall(), columns=[desc[0] for desc in self.cursor.description])
        return columns_df

    def get_sample_data(self, table_name, limit=100):
        """Retrieves a sample of table data (default: 100 rows)."""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return pd.read_sql(query, self.conn)

    def close(self):
        """Closes the Snowflake connection."""
        self.conn.close()
        log.info("Snowflake connection closed")