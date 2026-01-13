import subprocess
import asyncio
from sys import argv
import re
import time
import os, shutil


def log_inspection():
    filePath = argv[1]
    print(filePath)
    lastLine = None
    with open(filePath,'r') as f:
        while True:
            line = f.readline()
            overcommit_mode = int(subprocess.run(['cat', '/proc/sys/vm/overcommit_memory'], capture_output=True).stdout.decode().strip())
            ncssmp_pid=subprocess.run(['pgrep','-f', '\.smp.*-ncs true'], capture_output=True).stdout.decode().strip()
            print(ncssmp_pid)

            if len(line)>0:
                if re.search(r'\[MONITOR\] \[WARNING\] Physical Memory Usage.*exceeded.*MemTotal', line):
                    print("Physical Memory over Warning Level")
                    print("Collecting 3 Debug Dump every second.")
                    for nr in range(1, 4):
                        print("Collecting " +str(nr) +" Debug Dump")
                        subprocess.run(['ncs', '--debug-dump','assets/debug_dump/dump'+str(nr)+'.bin'], capture_output=True).stdout.decode()
                        time.sleep(1)
                    print("Done")
                elif re.search(r'\[MONITOR\] \[CRIT\] Physical Memory Usage.*exceeded.*MemTotal', line):
                    print("Out of Physical Memory over Critical Level.")
                    print(f"Terminating NSO {ncssmp_pid} with SIGUSR1 beofre SIGKILL Step in")
                    subprocess.run(['kill', '-USR1',str(ncssmp_pid)], capture_output=True).stdout.decode()
                    #print("Try to restart NSO")
                    #subprocess.run(['ncs'], capture_output=True).stdout.decode()
                elif re.search(r'\[MONITOR VERBOSE\] \[INFO\] Physical Memory Usage.*is within.*MemTotal', line):
                    print("Physical Memory Usage Normal Operation log entry.")

                elif re.search(r'\[MONITOR\] \[WARNING\] Committed_AS.*exceeded.*CommitLimit', line) and overcommit_mode != 0:
                    print("Committed_AS over Warning Level")
                    print("Collecting 3 Debug Dump every second")
                    for nr in range(1, 4):
                        print("Collecting " +str(nr) +" Debug Dump")
                        subprocess.run(['ncs', '--debug-dump','assets/debug_dump/dump'+str(nr)+'.bin'], capture_output=True).stdout.decode()
                        time.sleep(1)
                    print("Done")
                elif re.search(r'\[MONITOR\] \[CRIT\] Committed_AS.*exceeded.*CommitLimit', line) and overcommit_mode != 0:
                    print("Committed_AS over Critical Level. OOM Killer will step in soon")
                elif re.search(r'\[MONITOR VERBOSE\] \[INFO\] Committed_AS.*is within.*CommitLimit', line) and overcommit_mode != 0:
                    print("Committed_AS Normal Operation log entry.")
            #if not line:
            #    break
            # action
            #print(line)
            #lastLine = line
        return 1


def main():
    log_inspection()




if __name__=="__main__":
    main()
