# Space-VT-Task
Hello people!
This is the task required by Space@VT for being eligible to participate in GSOC 2018, working for Space@VT. I have taken up the 'Analyzing the Disturbance storm time (Dst) index' project's task of writing the dst indices to a database.

The task has been divided into 3 scripts, that scrape the 3 kinds of dst index provided on the given link, namely Provisional DST (2014-2015), Realtime DST (2016-2018(january)) and Final DST (1957-2013). Each file is well documented and most of the code is common across all three of them.

The following libraries have been used in this task:-
  1. urllib - To request each webpage where DST data is written.
  2. BeautifulSoup - To parse the webpage and extract the data (contained in a pre element) from the obtained page.
  3. sqlite3 - To write the data to the database.
  
Any database browsing tool, like 'DB browser for SQLITE', can be used to access the data stored in 'dst.db' database.
The database has a column for 'Year', 'Month', 'Day', and twenty four other columns, each corresponding to one hour of the day and containing the DST data for that hour.

To build the database locally on your system:-
  1. Download the three python scripts.
  2. Make sure BeautifulSoup4 is installed on your system.
  3. Run 'dst_real_time.py' first as it creates the database file and fills it up with the data of 2016-2018 years.
  4. Run the two other files, 'dst_provisional.py' and 'dst_final.py' to get data for the years 1957-2015.
