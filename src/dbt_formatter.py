import yaml
import os

def save_dbt_yaml(table_name, column_info, output_dir="dbt_schemas"):
    """Formats column metadata into DBT-compatible YAML."""
    os.makedirs(output_dir, exist_ok=True)

    dbt_yaml = {
        "version": 2,
        "models": [
            {
                "name": table_name,
                "description": f"Auto-generated DBT model description for {table_name}",
                "columns": [
                    {"name": col, "description": desc}
                    for col, desc in column_info.items()
                ]
            }
        ]
    }

    with open(f"{output_dir}/{table_name}.yml", "w") as file:
        yaml.dump(dbt_yaml, file, default_flow_style=False)