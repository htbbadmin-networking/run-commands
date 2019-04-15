#!/usr/bin/python3

import os
import sys
import time
import datetime
import paramiko
import getpass

host_file = "hosts"
command_file = "commands"
output_dir = "output/"

def read_file(filename):
    outlist = []
    with open(filename, 'r') as file:
        for line in file:
            outlist.append(line.strip())
    return outlist

def usage():
    usage = "python3 {} {{ssh_username}} {{ssh_password}}\n --or-- \npython3 {}".format(sys.argv[0], sys.argv[0])
    return usage

def run_commands(host, command_list, ssh_username, ssh_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, ssh_username, ssh_password, look_for_keys=False, allow_agent=False)
    client=ssh.invoke_shell()
    time.sleep(1)
    output = client.recv(65535)
    for command in command_list:
        client.send(command + '\n')
        time.sleep(1)
        output = client.recv(65535)
        time.sleep(1)
    ssh.close()
    return output

def main(host_file=host_file, command_file=command_file):
    host_list = read_file(host_file)
    command_list = read_file(command_file)
    for host in host_list:
        print("Running commands on {}".format(host))
        now = datetime.datetime.now()
        output_filename = os.path.join(output_dir, "-".join((host, str(now.year), str(now.month), str(now.day))))
        output = run_commands(host, command_list, ssh_username, ssh_password)
        decoded_output = output.decode('UTF-8')
        with open (output_filename, 'w') as outfile:
            outfile.write(decoded_output)
    return

if __name__ == '__main__':
    if len(sys.argv) == 1:
        os.system('clear')
        ssh_username = input('Enter SSH Username: ')
        ssh_password = getpass.getpass('Enter SSH Password: ')
        main()
    elif len(sys.argv) == 3:
        ssh_username = sys.argv[1]
        ssh_password = sys.argv[2]
        main()
    else:
        print(usage())
