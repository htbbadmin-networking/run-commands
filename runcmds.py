#!/usr/bin/python3

import argparse
import os
import sys
import time
import datetime
import paramiko
from getpass import getpass

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--ssh-username", help = "SSH Username")
    parser.add_argument("-c", "--command-file", help = "Command File", default = "commands")
    parser.add_argument("--hosts-file", help = "Hosts File", default = "hosts")
    parser.add_argument("-o", "--output-dir", help = "Output Directory", default = "output/")
    parser.add_argument("-r", "--retries", help = "Number of retries", default = 3)
    parser.add_argument("-t", "--timeout", help = "Absolute timeout in seconds", default = 30)
    parser.add_argument("--threads", help = "Threads", default = 2)
    args = parser.parse_args()
    args_dict = args.__dict__
    for key in args_dict.keys():
        if args_dict[key] == None:
            newvalue = input("Please specify " + key + ": ")
            setattr(args, key, newvalue)
    return args

def read_file(filename):
    outlist = []
    with open(filename, 'r') as file:
        for line in file:
            outlist.append(line.strip())
    return outlist

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

def main():
    os.system('clear')
    args = get_args()
    ssh_username = args.ssh_username
    command_file = args.command_file
    hosts_file = args.hosts_file
    output_dir = args.output_dir
    ssh_password = getpass('Enter SSH password: ')
    host_list = read_file(hosts_file)
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
    main()
