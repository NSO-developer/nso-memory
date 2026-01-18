import subprocess
import asyncio
from sys import argv
import re
import time
import os, shutil
import logging
from callbacks import warning_phy,warning_alloc,crit_alloc,crit_phy,info_phy,info_alloc



logger = logging.getLogger('middleware')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(argv[2])
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

#Parse the Log and proceed with Action
def log_inspection():
    filePath = argv[1]
    #logger.info(filePath)
    with open(filePath,'r') as f:
        info_trigger=False
        warning_trigger=False
        crit_trigger=False
        while True:
            line = f.readline()
            overcommit_mode = int(subprocess.run(['cat', '/proc/sys/vm/overcommit_memory'], capture_output=True).stdout.decode().strip())
            ncssmp_pid=subprocess.run(['pgrep','-f', '\.smp.*-ncs true'], capture_output=True).stdout.decode().strip()
            #Handling Infrastructure base on Logs from Monitor
            if len(line)>0:
                #Physical Memory Handling
                if re.search(r'\[MONITOR\] \[WARNING\] Physical Memory Usage.*exceeded.*MemTotal', line):
                    if not warning_trigger:
                        warning_phy(logger)
                        warning_trigger=True
                        crit_trigger=False
                        info_trigger=False
                elif re.search(r'\[MONITOR\] \[CRIT\] Physical Memory Usage.*exceeded.*MemTotal', line):
                    if not crit_trigger:
                        crit_phy(logger,ncssmp_pid)
                        crit_trigger=True
                        warning_trigger=True
                        info_trigger=False
                elif re.search(r'\[MONITOR VERBOSE\] \[INFO\] Physical Memory Usage.*is within.*MemTotal', line):
                    if not info_trigger:
                        info_phy(logger)
                        warning_trigger=False
                        crit_trigger=False

                #Allocated Memory Handling
                elif re.search(r'\[MONITOR\] \[WARNING\] Committed_AS.*exceeded.*CommitLimit', line) and overcommit_mode != 0:
                    if not warning_trigger:
                        warning_alloc(logger)
                        warning_trigger=True
                        crit_trigger=False
                        info_trigger=False
                elif re.search(r'\[MONITOR\] \[CRIT\] Committed_AS.*exceeded.*CommitLimit', line) and overcommit_mode != 0:
                    if not crit_trigger:
                        crit_alloc(logger)
                        crit_trigger=True
                        warning_trigger=True
                        info_trigger=False
                elif re.search(r'\[MONITOR VERBOSE\] \[INFO\] Committed_AS.*is within.*CommitLimit', line) and overcommit_mode != 0:
                    if not info_trigger:
                        info_alloc(logger)
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
                logger.info('Failed to delete %s. Reason: %s' % (file_path, e))


def main():
    logger.info("Starting Memory Inspection Middleware")
    prepare()
    log_inspection()




if __name__=="__main__":
    main()
