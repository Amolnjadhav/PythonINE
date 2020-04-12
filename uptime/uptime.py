# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import logging
#
#logging.basicConfig(filename='demo.log',
#                    level=logging.DEBUG,
#                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')
#
#if __name__ == "__main__":
#    logging.warning("I'm a warning!")   
#    logging.info("Hello, Python!")
#    logging.debug("I'm a debug message!")

#====================
import pandas as pd
import paramiko
import time
import getpass
import re
import os
#======================
global input_file
global output_file
global date
#===============

date= time.strftime("%Y%m%d_%H%M")
path = os.getcwd()
input_file= path + r'\deviceslist\devices.csv'
output_file= path + r'\results\Result_' + date + '.csv'

#=============

def get_devices_csv():
    #location=r'C:\Users\JMA1SGP\Documents\Important\Core+\Scripts\uptime\deviceslist\devices.csv'
    os.system('cls')
    df = pd.read_csv(input_file)
    print ( "=" * 50 )
    print ("This python code will connect to following device's")
    print ( "=" * 50 )
    print (df)
    print ( "=" * 50 )
    return(df)

def connect_network_device(device,ssh_port,username,password):
    try:      
        ssh_session=paramiko.SSHClient()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_session.connect(device,ssh_port,username=username,password=password,look_for_keys=False,allow_agent=False)
        remote_conn = ssh_session.invoke_shell()        
    except paramiko.AuthenticationException:
        print ("Unable to login to: " ,device ," - issue with username or password")
        exit()
    except paramiko.ssh_exception.NoValidConnectionsError:
        print ("Unable to connect to: " , device , " - no session possible")
        exit()
        
    print ("SSH session established with",device)
    time.sleep(5)
    remote_conn.send("show version\n")
    time.sleep(15)
    device_output = remote_conn.recv(2024)
    ssh_session.close()
    return (str(device_output))

def regx_uptime(string_shw_ver):
    utime = re.search(r"([0-9]* week[s]?, [0-9]* day[s]?, [0-9]* hour[s]?, [0-9]* minute[s]?)",string_shw_ver)
    return(utime.group(1))
    
def userinput():
    print ("Enter the Username, Password:")
    print ( "=" * 50 )
    user = input ("Username: ")
    passwd = getpass.getpass()
    ssh_port = 22
    print ( "=" * 50 )
    return(user,passwd,ssh_port)
    
def main():
    row=0
    devices=get_devices_csv()
    username,password,ssh_port=userinput()
    while row <= devices.index[-1] :
        string_sh_version=connect_network_device(devices['ipaddress'][row],ssh_port,username,password)
        uptime=regx_uptime(string_sh_version)
        try:
            with open(output_file,'a') as fp:
                device_uptime="%s,%s,%s,%s" %(devices['Names'][row],devices['ipaddress'][row],uptime,'\n') 
                fp.write(str(device_uptime.replace(', ','_')))
        except IOError:
              print ("Unable create to file",output_file)
              exit()
        row += 1
        
if __name__ == '__main__':
    main()