#!/usr/bin/env python

import paramiko
import sys

if len(sys.argv) < 5:
    print('args missing')
    sys.exit(1)

hostname = sys.argv[1]
password = sys.argv[2]
source = sys.argv[3]
dest = sys.argv[4]

username = "root"
port = 22

try:
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(source, dest)

finally:
    t.close()
