import sqlite3

# Open db file
fd = open('createDB.sql', 'r')

# Read data from file
sqlFile = fd.read()

# Close db file
fd.close()

# Split all SQL commands
sqlCommands = sqlFile.split(';')

# Create connection
con = sqlite3.connect("gymDB.db")
cur = con.cursor()

# Execute every command from the input file
for command in sqlCommands:
    con.execute(command)
    con.commit()
