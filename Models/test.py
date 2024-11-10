from pyspark.sql import SparkSession
from pyspark.pandas import Series as spkSeries
from propylean.properties import Length, Time
from propylean.series import Series as pplSeries
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
r = [1, 2]
a = spkSeries(r,copy=False)

pps = pplSeries(a,prop=Length)

print("++++++++++++++")
# print(pps)
# print("describe: ", pps.describe())
print("____________")
pps2=pps
print(a + 2)
print("____________")

print("++++++++++++")

# Import data from source as Pandas DataFrame.
import pandas as pd
df = pd.read_csv("/home/abhishekr/Propylean/Models/LPG_bullet_data.csv", sep=";")
pps = pplSeries(df["time(s)"],prop=Time)

print("++++++++++++++")
# print(pps)
# print("describe: ", pps.describe())
print("____________")
pps2=pps
print(df["time(s)"] + 2)
print("____________")
print("++++++++++++")


