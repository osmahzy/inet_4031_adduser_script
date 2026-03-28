#!/usr/bin/python3
# INET4031
# Mahad Osman
# Date Created: March 28, 2026
# Date Last Modified: March 28, 2026
# This script automates the creation of user accounts and group assignments
# on a Linux system by reading from an input file.

import os       # Used to run operating system commands like adduser and passwd
import re       # Used for regular expressions to detect comment/skip lines
import sys      # Used to read input from stdin (the input file)

def main():
    for line in sys.stdin:
        # Check if the line starts with '#' which marks it as a comment/skip line
        match = re.match("^#",line)
        # Strip whitespace and split the line into fields using ':' as delimiter
        fields = line.strip().split(':')
        # Skip the line if it is marked as a comment OR if it doesn't have
        # exactly 5 fields - this handles bad/incomplete lines in the input file
        if match or len(fields) != 5:
            continue
        # Extract username, password, and GECOS field (full name) from the fields
        # GECOS format matches what is stored in /etc/passwd
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])
        # Split the groups field by comma to get individual group names
        groups = fields[4].split(',')
        # Notify that the account creation process is starting for this user
        print("==> Creating account for %s..." % (username))
        # Build the adduser command with GECOS info and username
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)
        # Uncomment the lines below to actually run the command
        #print(cmd)
        #os.system(cmd)
        # Notify that the password is being set for this user
        print("==> Setting the password for %s..." % (username))
        # Build the passwd command to set the user's password
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
        # Uncomment the lines below to actually run the command
        #print(cmd)
        #os.system(cmd)
        for group in groups:
            # If group is not '-' (empty indicator), assign the user to that group
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                #print(cmd)
                #os.system(cmd)

if __name__ == '__main__':
    main()
