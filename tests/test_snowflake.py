import pytest
from unittest.mock import patch, MagicMock
from src.snowflake_connector import SnowflakeClient

@pytest.fixture
def mock_snowflake_connection():
    """Mock Snowflake connection."""
    with patch("snowflake.connector.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        yield mock_conn

def test_get_table_list(mock_snowflake_connection):
    """Test fetching tables from Snowflake."""
    mock_cursor = mock_snowflake_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("TABLE1",), ("TABLE2",)]  
    
    client = SnowflakeClient()
    tables = client.get_table_list()
    
    assert tables == ["TABLE1", "TABLE2"]
    mock_cursor.execute.assert_called_with("SHOW TABLES")