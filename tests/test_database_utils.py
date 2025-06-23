from src.utils.database_utils import transaction


def test_transaction_commit_on_success(mock_connection, mock_cursor):
    mock_connection.cursor.return_value = mock_cursor

    @transaction(mock_connection)
    def dummy_func(cursor=None) -> None:
        cursor.execute("some sql")

    # function call
    dummy_func()

    mock_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call("BEGIN TRANSACTION")
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_transaction_rollback_on_failure(mock_connection, mock_cursor):
    mock_connection.cursor.return_value = mock_cursor

    @transaction(mock_connection)
    def dummy_func(cursor=None) -> None:
        cursor.execute("some sql")
        raise RuntimeError("Something went wrong")

    dummy_func()

    mock_connection.cursor.assert_called_once()
    mock_connection.commit.assert_not_called()
    mock_connection.rollback.assert_called_once()
    mock_cursor.close.assert_called_once()
