# cs5293sp23-project0
Name: Zachary Knepp

#  Project Description
The purpose of this program is to go to the Norman Police Website (https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports), process the Daily Incident Summary PDFs, store the data in a sql database, and print out the frequency of nature of incident in descending order. 


# How to install
pipenv install

#  How to run
pipenv run … video

# Functions
project0.py \
create_table() - This function makes a database called normanpolice.db, and returns the connection to the database

get_pdf(url) - This function takes a url parameter to a pdf, retrieves the pdf, splits the pdf by line, stores the lines in a list, and returns the list of lines.

store_data_from_pdf(pdf, con) - This function takes the list of lines from get_pdf(url) and database connection as parameters, uses regular expression to extract the text data from the lines, and inserts the data into the database using the add_to_table(datetime, incident_num, location, nature, ori, con) function.

add_to_table(datetime, incident_num, location, nature, ori, con) - Takes datetime, incident_num, location, nature, ori, and database connection as parameters. Stores datetime, incident_num, location, nature, and ori in the database, and reports how many successes/failures.

clear_table(con) - Takes the database connection and clears the table.

print_table(con) - Takes the database connection and prints the table.

status(con) - Takes the database connection, counts the frequency of the nature column, and orders the nature column in descending order of by frequency.

# Database Development


# Bugs and Assumptions



