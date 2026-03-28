# inet_4031_adduser_script

## Description
This Python script automates the creation of Linux user accounts and group
assignments on an Ubuntu server. Instead of manually running adduser commands
for each user, this script reads from a structured input file and processes
each user automatically. This is useful when setting up multiple servers that
need the same set of user accounts.

## Files
- **create-users.py** - The main Python script that creates users and assigns groups
- **create-users.input** - The input file containing the list of users to create

## Input File Format
The input file is a colon-delimited text file. Each line represents one user:
```
username:password:lastname:firstname:group(s)
```

- Lines starting with `#` are skipped (comments)
- Use `-` in the groups field to indicate no group assignment
- Lines with fewer than 5 fields are skipped automatically
- Multiple groups are comma-separated: `group01,group02`

## How to Run

**Step 1 - Make the script executable:**
```
chmod +x create-users.py
```

**Step 2 - Dry run (no users actually created):**

Comment out the `os.system(cmd)` and `print(cmd)` lines in the script,
then run:
```
./create-users.py < create-users.input
```

**Step 3 - Run for real:**
```
sudo ./create-users.py < create-users.input
```
