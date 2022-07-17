from common.parameters import Environment
from common.access_db.sql_server import SqlServer

db_scource = {
    'sqlserver_investment_dev': {
        'env': Environment.Development,
        'type': SqlServer,
        'setting': {
            'hostname': r'LAPTOP-9QHQQSS8\SQLEXPRESS',
            'port': 14330,
            'database': 'Investment'
        }
    }
}
