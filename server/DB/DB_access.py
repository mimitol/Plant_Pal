import json
import pyodbc
from exceptions import DBConnectionError, QueryExecutionError,InvalidInputError

connection = None


async def connect():
    global connection
    if not connection:
        with open(r'C:\Users\user\PycharmProjects\pythonProject3\Configuration\configuration.json', 'r') as config_file:
            config_data = json.load(config_file)
        conn_str = config_data["conn_str"]
        # server_name = 'C503\SQLEXPRESS01'
        # database_name = 'GardenApp'
        # # Windows authentication
        # conn_str = 'DRIVER={SQL Server};SERVER=' + server_name + ';DATABASE=' + database_name + ';Trusted_Connection=yes;'
        try:
            # Establishing the connection
            conn = pyodbc.connect(conn_str)
            connection = conn

        except pyodbc.Error as ex:
            raise DBConnectionError
    return connection


async def execute_query(sql_query, args=None):
    result = None
    try:
        db_connection = await connect()
        cursor = db_connection.cursor()
        if args is None:
            result = cursor.execute(sql_query)
        else:
            cursor.execute(sql_query, args)
        if sql_query.strip().lower().startswith('select'):
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        db_connection.commit()
        return result
    except pyodbc.ProgrammingError as pe_ex:
        raise InvalidInputError
    except pyodbc.Error as ex:
        raise QueryExecutionError



def close_connection(cursor):
    # Close the cursor and connection
    global connection
    connection.close()
    cursor.close()