import subprocess
import asyncio
from sys import argv
import re
import time
import os, shutil


def log_inspection():
    filePath = argv[1]
    #print(filePath)
    lastLine = None
    with open(filePath,'r') as f:
        info_trigger=False
        warning_trigger=False
        crit_trigger=False
        while True:
            line = f.readline()
            overcommit_mode = int(subprocess.run(['cat', '/proc/sys/vm/overcommit_memory'], capture_output=True).stdout.decode().strip())
            ncssmp_pid=subprocess.run(['pgrep','-f', '\.smp.*-ncs true'], capture_output=True).stdout.decode().strip()
            #print(ncssmp_pid)

            if len(line)>0:
                if re.search(r'\[MONITOR\] \[WARNING\] Physical Memory Usage.*exceeded.*MemTotal', line):
                    if not warning_trigger:
                        print("Physical Memory over Warning Level")
                        print("Collecting 3 Debug Dump every second.")
                        for nr in range(1, 4):
                            print("Collecting " +str(nr) +" Debug Dump")
                            subprocess.run(['ncs', '--debug-dump','assets/debug_dump/dump'+str(nr)+'.bin'], capture_output=True).stdout.decode()
                            time.sleep(1)
                        warning_trigger=True
                        crit_trigger=False
                        info_trigger=False
                        print("Done")  
                elif re.search(r'\[MONITOR\] \[CRIT\] Physical Memory Usage.*exceeded.*MemTotal', line):
                    if not crit_trigger:
                        print("Physical Memory over Critical Level.")
                        print(f"Terminating NSO {ncssmp_pid} with SIGUSR1 beofre SIGKILL Step in")
                        subprocess.run(['kill', '-USR1',str(ncssmp_pid)], capture_output=True).stdout.decode()
                        crit_trigger=True
                        warning_trigger=True
                        info_trigger=False
                    #print("Try to restart NSO")
                    #subprocess.run(['ncs'], capture_output=True).stdout.decode()
                elif re.search(r'\[MONITOR VERBOSE\] \[INFO\] Physical Memory Usage.*is within.*MemTotal', line):
                    if not info_trigger:
                        print("Physical Memory Usage Normal Operation log entry.")
                        warning_trigger=False
                        crit_trigger=False

                elif re.search(r'\[MONITOR\] \[WARNING\] Committed_AS.*exceeded.*CommitLimit', line) and overcommit_mode != 0:
                    if not warning_trigger:
                        print("Committed_AS over Warning Level")
                        print("Collecting 3 Debug Dump every second")
                        for nr in range(1, 4):
                            print("Collecting " +str(nr) +" Debug Dump")
                            subprocess.run(['ncs', '--debug-dump','assets/debug_dump/dump'+str(nr)+'.bin'], capture_output=True).stdout.decode()
                            time.sleep(1)
                        warning_trigger=True
                        crit_trigger=False
                        info_trigger=False
                        print("Done")
                elif re.search(r'\[MONITOR\] \[CRIT\] Committed_AS.*exceeded.*CommitLimit', line) and overcommit_mode != 0:
                    if not crit_trigger:
                        print("Committed_AS over Critical Level. OOM Killer will step in soon")
                        crit_trigger=True
                        warning_trigger=True
                        info_trigger=False
                elif re.search(r'\[MONITOR VERBOSE\] \[INFO\] Committed_AS.*is within.*CommitLimit', line) and overcommit_mode != 0:
                    if not info_trigger:
                        print("Committed_AS Normal Operation log entry.")
                        warning_trigger=False
                        crit_trigger=False
                        info_trigger=False
    return 1


def prepare():
    for filename in os.listdir("assets/debug_dump/"):
        if filename.startswith("dump") and filename.endswith(".bin"):
            file_path = os.path.join("assets/debug_dump/", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def main():
    prepare()
    log_inspection()




if __name__=="__main__":
    main()
