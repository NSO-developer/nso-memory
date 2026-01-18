import subprocess
import time

# Handling Callback


# Physical Memory
# Info Level Physical Memory
def info_phy(logger,ncssmp_pid=None,overcommit_mode=None):
    logger.info("Physical Memory Usage Normal Operation log entry.")
    logger.info("Physical Memory Info Handling Done")

# Warning Level Physical Memory
def warning_phy(logger,ncssmp_pid=None,overcommit_mode=None):
    logger.info("Physical Memory over Warning Level")
    logger.info("Collecting 3 Debug Dump every second.")
    for nr in range(1, 4):
        logger.info("Collecting " +str(nr) +" Debug Dump")
        subprocess.run(['ncs', '--debug-dump','assets/debug_dump/dump'+str(nr)+'.bin'], capture_output=True).stdout.decode()
        time.sleep(1)
    logger.info("Physical Memory Warning Handling Done")

# Critical Level Physical Memory
def crit_phy(logger,ncssmp_pid=None,overcommit_mode=None):
    logger.info("Physical Memory over Critical Level.")
    logger.info(f"Terminating NSO {ncssmp_pid} with SIGUSR1 beofre SIGKILL Step in")
    subprocess.run(['kill', '-USR1',str(ncssmp_pid)], capture_output=True).stdout.decode()
    logger.info("Physical Memory Critical Handling Done")

# Allocated Memory
# Info Level Allocated Memory
def info_alloc(logger,ncssmp_pid=None,overcommit_mode=None):
    logger.info("Committed_AS Normal Operation log entry.")
    logger.info("Allocated Memory Info Handling Done")

# Warning Level Allocated Memory
def warning_alloc(logger,ncssmp_pid=None,overcommit_mode=None):
    logger.info("Committed_AS over Warning Level")
    logger.info("Collecting 3 Debug Dump every second")
    for nr in range(1, 4):
        logger.info("Collecting " +str(nr) +" Debug Dump")
        subprocess.run(['ncs', '--debug-dump','assets/debug_dump/dump'+str(nr)+'.bin'], capture_output=True).stdout.decode()
        time.sleep(1)
    logger.info("Allocated Memory Warning Handling Done")

# Crtical Level Allocated Memory
def crit_alloc(logger,ncssmp_pid=None,overcommit_mode=None):
    logger.info("Committed_AS over Critical Level. OOM Killer will step in soon")
    logger.info("Allocated Memory Critical Handling Done")
