import urllib
import urllib.request
from urllib.parse import urlparse
import os
import requests
import re
import sqlite3
import io
import PyPDF2
import numpy as np

# This function creates the sql table to store the data in
def create_table():
  con = sqlite3.connect("normanpolice.db", timeout=60)
  cur = con.cursor()
  try:
    cur.execute("CREATE TABLE incidents(datetime, incident_num, location, nature, ori)")
  except:
    print("Table already exists")
  return con





# This function adds to the sql table
def add_to_table(datetime, incident_num, location, nature, ori, con):
  #con = sqlite3.connect("normanpolice.db")
  cur = con.cursor()
  cur.execute("INSERT INTO incidents (datetime, incident_num, location, nature, ori) values (?, ?, ?, ?, ?)", (datetime, incident_num, location, nature, ori))
  con.commit()



#This functiopn clears the sql table
def clear_table(con):
  # delete all rows from table
  cur = con.cursor()
  cur.execute('DELETE FROM incidents;',);
  print('We have deleted', cur.rowcount, 'records from the table.')
  #commit the changes to db			
  con.commit()





#This function follows the url to the pdf, retrieves the pdf, and returns a list of rows in the pdf
def get_pdf(url):
  req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
  remote_file = urllib.request.urlopen(req).read()
  remote_file_bytes = io.BytesIO(remote_file)
  pdfdoc = PyPDF2.PdfReader(remote_file_bytes)

  lines = []
  for page in pdfdoc.pages:
    # Extracting text from page
    # And splitting it into chunks of lines
    text = page.extract_text().split("\n")
    lines.append(text)

  lines_separated =[]
  count = 0
  for line in lines:
    for l in line:
      lines_separated.append(l)
      count = count + 1
  return lines_separated







#This function takes a list of lines from the pdf, searches the lines for data using regular expressions and stores in sql database
def store_data_from_pdf(pdf, con):
  regex_datetime = r"((\d{1})\/(\d{1})\/(\d{4}) ([0-9]+):(\d{2}))|((\d{1})\/(\d{2})\/(\d{4}) ([0-9]+):(\d{2}))"
  regex_incident_num = r"(\d{4})-(\d{8})"
  regex_location = r"( \d{1,5}. ([A-Z]|[1-9])+ [A-Z]+ (([A-Z]+)\b)?)|( [A-Z]+ [A-Z]+ [A-Z]+ \/ [A-Z]+ [A-Z]+ [A-Z]+)|( [A-Z]+ [A-Z]+ \/ [A-Z]+ [A-Z]+)|([A-Z] [A-Z]+ [A-Z]+ \/ \d+[A-Z]+ [A-Z]+ [A-Z]+)|([1-9]+[A-Z]+ [A-Z]+ [A-Z]+ \/ [A-Z]+ \d)|(\d\d\d\d [A-Z]+ \d+\w+ \w+)|([A-Z] [A-Z]+ [A-Z]+ \d [A-Z]+ \/ [A-Z] [A-Z]+ [A-Z]+)|([A-Z]+ [A-Z]+ \/ \d+[A-Z]+ [A-Z]+ [A-Z]+)|(\d{4} \d{3}[A-Z]+ [A-Z]+ [A-Z]+)|(\d+ [A-Z] [A-Z]\d\d)"
  regex_nature = r"([A-Z][a-z]+ [A-Z][a-z]+\/[A-Z][a-z]+)|([A-Z][a-z]+ \/ [A-Z][a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+ [a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+ [a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+\/[A-Z][a-z]+ [A-Z][a-z]+\/[A-Z][a-z]+)|([A-Z][a-z]+\/[A-Z][a-z]+)|([A-Z][a-z]+ [A-Z][a-z]+\/[A-Z][a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)|((MVA) [A-Z][a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+ [A-Z][a-z]+)|([A-Z][a-z]+)"
  regex_ori = r"(EMSSTAT)|([A-Z][A-Z]\d\d\d\d\d\d\d)|(14005)"

  count = 0
  s = 0
  f = 0
  for i in pdf:
    try:
      dt = re.search(regex_datetime, i)
      inc = re.search(regex_incident_num, i)
      loc = re.search(regex_location, i)
      nat = re.search(regex_nature, i)
      o = re.search(regex_ori, i)
      ######################################
      if(dt == None):
        datetime = "Null"
      else:
        datetime = dt.group()
      ######################################
      if(inc == None):
        incident_num = "Null"
      else:
        incident_num = inc.group()
      ######################################
      if(loc == None):
        location = "Null"
      else:
        location = loc.group()
      ######################################
      if(nat == None):
        nature = "Null"
      else:
        nature = nat.group()
      ######################################
      if(o == None):
        ori = "Null"
      else:
        ori = o.group()

      
      add_to_table(datetime, incident_num, location, nature, ori, con)
      #print("Added to table: ", i)
      s = s + 1
    except:
      print("An exeption occured with: ", i)
      f = f + 1

    count = count + 1

  print(s, " Successes occurred")
  print(f, " Failures occurred")







#This function prints the contents in the sql database
def print_table(con):
  cur = con.cursor()
  res = cur.execute("SELECT * FROM incidents")
  rows = res.fetchall()
  k = len(rows)
  
  for i in range(0,k):
    print(rows[i][0], "|", rows[i][1], "|", rows[i][2], "|", rows[i][3], "|", rows[i][4])



#This function prints out the frequencies of nature
def status(con):
  cur = con.cursor()
  res = cur.execute("SELECT nature, count(*) as frequency FROM incidents GROUP BY nature ORDER BY count(*) desc")
  rows = res.fetchall()
  k = len(rows)
  
  for i in range(0,k):
    print(rows[i][0], "|", rows[i][1])



