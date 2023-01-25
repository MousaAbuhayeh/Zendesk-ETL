# Introduction 
This script will periodicly transfer Zendesk's data into and SQL database using python with a period of 100 thousend seconds. 
Zendesk's data consists of the following main parts to biuld your data model.
- Tickets
- Ticket metrics
- Custom fields
- Users
- Groups
- Ticket fields
Making sure the data transferred is sufficient enough to produce useful insights

# Getting Started
1.	Installation process
- Setting up credintials for your zendesk domain and SQL database as system variables on your machine. naming them as stated in Config.ini file
- Setting up a mail host and port for the SMTP handler to send report emails
- Building tables in your database's schema for the data you wish to transfer
- Listing in Static.py file all fields you wish to transfer from zendesk (both keys in the JSON data and column names in the tables)
2.	Software dependencies
Windows or linux machine.
3.	API references
https://developer.zendesk.com/api-reference/

# Build and Test
- First test the code on a short period of time to test for errors or any missplaced data and data types
- remove time limit to export all data available for the first run
- set up this script as a service on your machine so it would produce your data daily

