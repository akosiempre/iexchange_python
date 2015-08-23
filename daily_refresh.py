#!usr/lib/bin python
'''
This script will run everyday to synchronize the topdomain table with the list of domain per number of email users
'''
import mysql.connector
cnx = mysql.connector.connect(user='root', database='db_iexchange',charset='utf8',use_unicode=True)
cursor = cnx.cursor()

#insert initial records added to mailing table into topdomain
try:
	insertquery = ("insert ignore into topdomain (domain_name,email_count,growth_values) \
			select substring_index(addr,'@',-1) as domain ,count(*),'[]' as count from mailing group by domain;")
	cursor.execute(insertquery)
	cnx.commit()
	cursor.close()
except:
	print "Error: initializing table top domain"

#read from mailing to get the new emails added then compare to topdomain table
cursor = cnx.cursor()
query = ("select substring_index(addr,'@',-1) as domain ,count(*) as count from mailing group by domain;")
try:
   cursor.execute(query)
   results = cursor.fetchall()
   cursor.close()
   for row in results:
      domain = row[0]
      count = row[1]
      cursor = cnx.cursor()
	  #comparing to topdomain table
      domainquery = ("select domain_name, email_count, growth_values from topdomain where domain_name = '%s';" %(domain))
      try:
        cursor.execute(domainquery)
        results = cursor.fetchall()
        cursor.close()
        for row in results:
          domain_name = row[0]
          email_count = row[1]
          growth = row[2]
          growth = eval(growth)
          daystotal = sum(growth)
          totalcount = email_count + daystotal
          countdiff = count - totalcount
          growth.append(countdiff)
          oldest_val = 0
          while True:
            daycount = len(growth)		  
            if (daycount > 30):
               oldest_val = oldest_val + growth.pop(0)		  
            else:
               break
          new_emailcount = email_count + oldest_val
          try:
            cursor = cnx.cursor()
            insertquery = ("insert into topdomain (domain_name,email_count,growth_values) values ('%s', '%s', '%s') \
                 			ON DUPLICATE KEY UPDATE email_count='%s',growth_values='%s'" \
							% (domain_name,new_emailcount,growth,new_emailcount,growth))
            cursor.execute(insertquery)
            cnx.commit()
            cursor.close()
          except:
		    print "Error: unable to insert data to topdomain"
      except:
        print "Error: unable to fetch data from topdomain"
except:
   print "Error: unable to fetch data from mailing table"
cursor.close()
cnx.close()	