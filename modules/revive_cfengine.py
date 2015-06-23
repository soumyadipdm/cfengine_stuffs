#!/usr/bin/python

'''This script attempts to revive cfengine, once it detects the following:
   1. cf-agent hasn't run for more than 30 minutes (configurable)
   2. cf-execd process is not found, even though cfengine is installed
'''
import os
import sys
import re
import time
import subprocess
import psutil
import syslog
import argparse

def run_cfe_agent():
    cfe_agent = "/var/cfengine/bin/cf-agent"
    error = False

    'first do a fresh failsafe file transfer from master policy server'
    try:
        with open(os.devnull, "wb") as dev_null:
            proc = subprocess.Popen(["/usr/bin/nohup", cfe_agent, "-K", "-f failsafe.cf"],
                    stdout=dev_null,
                    stderr=dev_null,
                    preexec_fn=os.setpgrp
                    )

    except OSError as e:
        syslog.syslog(syslog.LOG_ERR, str(e))
        error = True

    'now run cf-agent'
    try:
        with open(os.devnull, "wb") as dev_null:
            proc = subprocess.Popen(["/usr/bin/nohup", cfe_agent, "-K"],
                    stdout=dev_null,
                    stderr=dev_null,
                    preexec_fn=os.setpgrp
                    )

    except OSError as e:
        syslog.syslog(syslog.LOG_ERR, str(e))
        error = True

    return error

def bootstrap_cfe(policy_server_ip):
    cfe_agent = "/var/cfengine/bin/cf-agent"
    error = False

    try:
        with open(os.devnull, "wb") as dev_null:
            proc = subprocess.Popen(["/usr/bin/nohup", cfe_agent, "--bootstrap", "policy_server_ip"],
                    stdout=dev_null,
                    stderr=dev_null,
                    preexec_fn=os.setpgrp
                    )
    
    except OSError as e:
        syslog.syslog(syslog.LOG_ERR, str(e))
        error = True

def cure_me(policy_server_ip):
    error = run_cfe_agent()
    if error:
        berr = bootstrap_cfe(policy_server_ip)
        if berr:
            syslog.syslog(syslog.LOG_ERR, "unable to bootstrap CFEngine")
            sys.exit(1)

def check_cf_agent_last_run(max_cf_agent_run_delay, policy_server_ip):
    '''Check if cf-agent ran within max_cf_agent_run_delay, if not,
       1) do a failsafe transfer, run cf-agent
       2) if step 1 is unsuccesful, bootstrap CFEngine
    '''
    cfe_promise_summary_log = "/var/cfengine/promise_summary.log"

    try:
        with open(cfe_promise_summary_log, "r") as cfe_promise_summary_log_file:
            for line in cfe_promise_summary_log_file:
                pass
            
            'get the last line'
            last_line = line

    except IOError as e:
        syslog.syslog(syslog.LOG_ERR, str(e))
        sys.exit(1)

    last_time_regex = re.compile(r'^\d+,(\d+):.*?$')
    match = last_time_regex.search(last_line)

    if match:
        last_time = int(match.group(1))
    else:
        syslog.syslog(syslog.LOG_WARNING, "cf-agent run last time could not be obtained")
        sys.exit(1)

    delay = int(time.time()) - last_time

    if delay > max_cf_agent_run_delay:
        syslog.syslog(syslog.LOG_CRIT, "cf-agent has not run for {0} min".format(delay/60))
        syslog.syslog(syslog.LOG_INFO, "forking cf-agent")
        cure_me(policy_server_ip)

def check_cf_execd(policy_server_ip):
    '''Check if cf-execd is in the process table, if not
       1) do a failsafe, run cf-agent
       2) if step 1 fails, do a bootstrap
    '''
    pid = None 
    'grab pid from cf-execd.pid'
    try:
        with open("/var/cfengine/cf-execd.pid", "r") as pid_file:
            pid = int(pid_file.read().strip())

    except IOError as e:
        syslog.syslog(syslog.LOG_WARNING, str(e))

    cf_execd_exists = psutil.pid_exists(pid)

    if not cf_execd_exists:
        syslog.syslog(syslog.LOG_CRIT, "cf-execd is not running")
        syslog.syslog(syslog.LOG_INFO, "forking cf-agent")
        cure_me(policy_server_ip) 

def main():
    parser = argparse.ArgumentParser(description="A script to attempt to recover CFEngine")
    parser.add_argument("--max_delay", "-d", type=int, default=30, help="max. num minutes from last cf-agent run, default 30 mins")
    parser.add_argument("policy_server_ip", help="IP of the policy server")

    args = parser.parse_args()
    
    if args.max_delay not in range(61):
        sys.exit("number of minutes  should be within 0 to 60")

    max_cf_agent_run_delay = args.max_delay*60*60 # seconds
    
    'run the checks now'
    check_cf_agent_last_run(max_cf_agent_run_delay, args.policy_server_ip)
    check_cf_execd(args.policy_server_ip)

    syslog.syslog(syslog.LOG_INFO, "revive_cfengine was run and everything came out fine")

if __name__ == '__main__':
    main()
