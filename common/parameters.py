from enum import Enum


class Environment(Enum):
    Development = 'dev'
    Integration = 'int'
    Staging = 'stg'
    Production = 'prd'
