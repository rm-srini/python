from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql.types import *

# spark = SparkSession.builder.appName("DataFrame").getOrCreate()
spark = SparkSession.builder.appName("pandas to spark").getOrCreate()

df = pd.read_excel(r"C:\Srini\Finance\Transaction.xlsx")

df_spark = spark.createDataFrame(df)

print(df_spark)