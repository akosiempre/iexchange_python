#!usr/lib/bin python
'''
This script will run only once to initially load the topdomain table
'''
import mysql.connector
cnx = mysql.connector.connect(user='root', database='db_iexchange',charset='utf8',use_unicode=True)
cursor = cnx.cursor()	

insertquery = ("insert into topdomain (domain_name,email_count,growth_values) \
			select substring_index(addr,'@',-1) as domain ,count(*) as count,'[]' from mailing group by domain;")
try:
	cursor.execute(insertquery)
	cnx.commit()
except:
	print "Error: unable to insert data to topdomain"

cursor.close()
cnx.close()
