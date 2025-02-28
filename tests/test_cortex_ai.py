import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.cortex_ai import generate_column_descriptions

@pytest.fixture
def mock_snowflake_connection():
    """Mock Snowflake connection."""
    with patch("snowflake.connector.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

def test_generate_column_descriptions(mock_snowflake_connection):
    """Test Cortex AI column description generation."""
    mock_cursor = mock_snowflake_connection.cursor.return_value
    mock_cursor.fetchone.return_value = ("Generated AI descriptions",)
    
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
    descriptions = generate_column_descriptions(df)
    
    assert descriptions == "Generated AI descriptions"
    mock_cursor.execute.assert_called()