from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as f
import requests

def process(row):
  print(30*'*')
  print('procesando...')
  datos={'hashtag':row['hashtag'],'count':row['count']}
  requests.post('http://127.0.0.1:5000/',data=datos)
  print(row)
  print(30*'*')
  
spark = SparkSession.builder.appName('twitter-processing').getOrCreate()

lines = spark.readStream.format('socket').option('host','localhost').option('port',9898).load()

# Se obtienen los Hashtag
col1=lines.value.alias('hashtag')
# Se cuentan los HashTag
data = lines.select(col1).groupBy('hashtag').count()

query = data.writeStream.foreach(process).outputMode('complete').start()

query.awaitTermination()








