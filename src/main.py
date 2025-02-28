from snowflake_connector import SnowflakeClient
from cortex_ai import generate_column_descriptions
from dbt_formatter import save_dbt_yaml

def main():
    """Runs the end-to-end process: Snowflake metadata extraction -> Cortex AI -> DBT YAML."""
    client = SnowflakeClient()
    
    tables = client.get_table_list()
    for table in tables:
        print(f"Processing {table}...")

        metadata_df = client.get_table_metadata(table)
        sample_data = client.get_sample_data(table)

        ai_descriptions = generate_column_descriptions(sample_data)
        column_info = {col: ai_descriptions[i] for i, col in enumerate(sample_data.columns)}

        save_dbt_yaml(table, column_info)

    client.close()

if __name__ == "__main__":
    main()