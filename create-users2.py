#!/usr/bin/python3
# INET4031
# Mahad Osman
# Date Created: March 28, 2026
# Date Last Modified: March 28, 2026
# This script automates the creation of Linux user accounts and group
# assignments. It includes an interactive dry-run mode that allows the
# user to test the script without making any changes to the system.

# os module - used to run Linux system commands like adduser and passwd
import os
# re module - used for regular expressions to detect comment/skip lines
import re
# sys module - used to read input line by line from stdin
import sys

def main():
    # Prompt the user to choose between dry-run mode or normal execution
    dry_run_input = input("Would you like to run in dry-run mode? (Y/N): ")
    # Determine if dry-run mode is enabled based on user input
    dry_run = dry_run_input.strip().upper() == 'Y'

    if dry_run:
        print("==> Running in DRY-RUN mode. No changes will be made to the system.")
    else:
        print("==> Running in NORMAL mode. Users will be created.")

    # Read the input file line by line from stdin
    for line in sys.stdin:
        # Check if the line starts with '#' which marks it as a comment/skip line
        match = re.match("^#", line)
        # Remove leading/trailing whitespace and split into fields by ':'
        fields = line.strip().split(':')
        # Skip lines that are comments or don't have exactly 5 fields
        if match or len(fields) != 5:
            if dry_run:
                if match:
                    print("==> Skipping line marked to skip: %s" % line.strip())
                else:
                    print("==> ERROR: Line does not have enough fields, skipping: %s" % line.strip())
            continue

        # Extract user data from the parsed fields
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        # Split the groups field by comma to handle multiple group assignments
        groups = fields[4].split(',')

        # Notify that account creation is starting for this user
        print("==> Creating account for %s..." % (username))
        # Build the adduser command
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        if dry_run:
            # In dry-run mode just print the command, don't execute it
            print(cmd)
        else:
            # In normal mode execute the command
            os.system(cmd)

        # Notify that the password is being set for this user
        print("==> Setting the password for %s..." % (username))
        # Build the passwd command
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        if dry_run:
            print(cmd)
        else:
            os.system(cmd)

        # Loop through each group and assign the user if group is not '-'
        for group in groups:
            # '-' indicates no group assignment - skip it
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                if dry_run:
                    print(cmd)
                else:
                    os.system(cmd)

if __name__ == '__main__':
    main()
