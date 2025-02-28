import yaml
import os
import pytest
from src.dbt_formatter import save_dbt_yaml

@pytest.fixture
def cleanup_yaml():
    """Clean up generated YAML file after test."""
    yield
    if os.path.exists("dbt_schemas/test_table.yml"):
        os.remove("dbt_schemas/test_table.yml")

def test_save_dbt_yaml(cleanup_yaml):
    """Test saving DBT YAML output."""
    column_info = {"name": "Customer Name", "age": "Customer Age"}
    save_dbt_yaml("test_table", column_info, output_dir="dbt_schemas")

    # Check if file is created
    assert os.path.exists("dbt_schemas/test_table.yml")

    # Validate YAML content
    with open("dbt_schemas/test_table.yml", "r") as file:
        yaml_content = yaml.safe_load(file)

    assert yaml_content["models"][0]["name"] == "test_table"
    assert yaml_content["models"][0]["columns"][0]["name"] == "name"
    assert yaml_content["models"][0]["columns"][0]["description"] == "Customer Name"