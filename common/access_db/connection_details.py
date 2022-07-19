from common.parameters import Environment

db_source = {
    'sqlserver_investment_dev': {
        'env': Environment.Development,
        'setting': {
            'hostname': r'LAPTOP-9QHQQSS8\SQLEXPRESS',
            'port': 14330,
            'database': 'Investment'
        }
    }
}
