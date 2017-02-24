from pyspark import SparkContext
import os
#os.system("hadoop fs -find /datalake/data/Genesis/entrevistas -name *.pdf > nombres_archivos_h.txt" )
#with open ("hdfs:///datalake/tmp/nombres_archivos_h.txt",'r') as f:
sc = SparkContext("local" , "Simple App")
print "termine"
file = sc.textFile("hdfs:///datalake/tmp/nombres_archivos_h.txt")
print file.count()
#print file
