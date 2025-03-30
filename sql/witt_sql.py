import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Token, Where
from sqlparse.tokens import Keyword, DML, Name


def extract_columns_from_select(parsed):
    columns = set()
    found_select = False  # Initialize found_select

    for stmt in parsed.tokens:
        if stmt.ttype is DML and stmt.value.upper() == 'SELECT':
            found_select = True
        elif found_select and isinstance(stmt, IdentifierList):
            for identifier in stmt.get_identifiers():
                columns.add(identifier.get_real_name())
        elif found_select and isinstance(stmt, Identifier):
            columns.add(stmt.get_real_name())
    return columns


def extract_columns_from_conditions(parsed):
    conditions = set()
    for stmt in parsed.tokens:
        if isinstance(stmt, Where) or (isinstance(stmt, IdentifierList) or isinstance(stmt, Identifier)):
            for token in stmt.tokens:
                if isinstance(token, Identifier):
                    conditions.add(token.get_real_name())
                elif token.ttype is Name:
                    conditions.add(token.value)
        elif stmt.ttype is Name:
            conditions.add(stmt.value)
    return conditions


def parse_sql(query):
    parsed = sqlparse.parse(query)[0]
    select_columns = extract_columns_from_select(parsed)
    condition_columns = extract_columns_from_conditions(parsed)
    return select_columns, condition_columns


query = """
SELECT
    name,
    salary,
    deprtment_name
from
    (
    select
        name,
        salary,
        dept_id
    from
        perm_emp pe
    union all
    select
        name,
        salary,
        dept_id
    from
        cnt_emp ce
    where type = 'F'
    ) emp
join
    dept on dept.dept_id = emp.dept_id
where
    dept_name = 'Data'
    depttpye = ''
"""

select_columns, condition_columns = parse_sql(query)
print("Columns in SELECT:", select_columns)
print("Columns in WHERE/JOIN:", condition_columns)
