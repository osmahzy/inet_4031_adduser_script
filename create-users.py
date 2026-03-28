#!/usr/bin/python3
# INET4031
# Mahad Osman
# Date Created: March 28, 2026
# Date Last Modified: March 28, 2026
# This script automates the creation of Linux user accounts and group
# assignments by reading from a colon-delimited input file via stdin.
# Each line in the input file represents one user with fields:
# username:password:lastname:firstname:group(s)

# os module - used to run Linux system commands like adduser and passwd
import os
# re module - used for regular expressions to detect comment/skip lines
import re
# sys module - used to read input line by line from stdin
import sys

def main():
    # Read the input file line by line from stdin
    for line in sys.stdin:
        # Check if the line starts with '#' which marks it as a comment
        # Lines starting with '#' should be skipped entirely
        match = re.match("^#",line)
        # Remove leading/trailing whitespace and split the line into
        # fields using ':' as the delimiter
        fields = line.strip().split(':')
        # Skip the line if it is a comment (starts with #) OR if it does
        # not have exactly 5 fields - this handles malformed/incomplete lines
        # in the input file without crashing the script
        if match or len(fields) != 5:
            continue
        # Extract user data from the parsed fields
        # username - the Linux login name
        # password - the user's password
        # gecos - full name field stored in /etc/passwd (firstname lastname)
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])
        # Split the groups field by comma to handle multiple group assignments
        # A '-' in this field means no group assignment for this user
        groups = fields[4].split(',')
        # Notify that account creation is starting for this user
        print("==> Creating account for %s..." % (username))
        # Build the adduser command using the gecos info and username
        # --disabled-password skips interactive password prompt
        # --gecos sets the full name field in /etc/passwd
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)
        print(cmd)
        os.system(cmd)
        # Notify that the password is being set for this user
        print("==> Setting the password for %s..." % (username))
        # Build the passwd command using echo to pipe the password twice
        # (once for new password, once for confirmation)
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
        print(cmd)
        os.system(cmd)
        # Loop through each group and assign the user if group is not '-'
        for group in groups:
            # '-' indicates no group assignment - skip it
            # Otherwise assign the user to the specified group
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
