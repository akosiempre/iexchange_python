#!usr/lib/bin python
'''
This script will show the top 50 domains by count sorted by the percentage of growth of the last 30 days compared to the total.
'''
import os
import mysql.connector
from operator import itemgetter

cnx = mysql.connector.connect(user='root', database='db_iexchange',charset='utf8',use_unicode=True)
cursor = cnx.cursor()	
domainquery = ("select domain_name, email_count, growth_values from topdomain order by email_count desc limit 0, 50")

#create initial report
try:
  os.remove("email_domain_growth.txt")
except OSError:
  pass
fout = open("email_domain_growth.txt", 'a')

try:
   cursor.execute(domainquery)
   results = cursor.fetchall()
   for row in results:
     domain_name = row[0]
     email_count = row[1]
     growth = row[2]
     growth = eval(growth)
     daystotal = sum(growth)
     growthperc = (daystotal / float(email_count))*100
     total_count = email_count + daystotal
     fout.write("%40s, \t%d, \t%6.2f %%\n" % (domain_name, total_count, growthperc))
except:
   print "Error: unable to get data from topdomain"
fout.close()
cursor.close()
cnx.close()

#creating the final report
with open('email_domain_growth.txt') as fin:
   lines = [line.split() for line in fin]

lines.sort(key=itemgetter(2),reverse=True)

with open('email_domain_growth.txt', 'w') as fout:
   fout.write("        DOMAIN NAME,   COUNT,  GROWTH\n")
   for el in lines:
	  fout.write("%20s %8s %7s\n" % (el[0],el[1],el[2]))

fout.close()