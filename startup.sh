#!/bin/bash


INSTALLATION_PATH=$1

trap "cleanup" SIGINT 
trap "cleanup" SIGKILL


cleanup () {
    echo "Cleaning up monitoring processes..."
    PID_MONITOR=$(pgrep -f plot.sh)
    echo "Terminating Memory Monitor PID $PID_MONITOR"
    pkill -f plot.sh
    pkill -f monitor.sh
    pkill -f collect.sh
    PID_MIDDLE=$(pgrep -f lib/middleware/main.py)
    echo "Terminating Middleware PID $PID_MIDDLE"
    pkill -f lib/middleware/main.py
    #kill -9 $PID_MIDDLE
    exit 0
}


start_monitoring_daemon () {
    # montior engine
    cd $INSTALLATION_PATH/lib/memory_utilization_tool/ ;bash plot.sh -v -m NaN &> $INSTALLATION_PATH/logs/monitor.log &
    PID_MONITOR=$(pgrep -f plot.sh)
    echo "NSO Memory Utilization Tool started in Monitor mode with PID - $PID_MONITOR"
    cd $INSTALLATION_PATH
    # middleware action engine
    python $INSTALLATION_PATH/lib/middleware/main.py $INSTALLATION_PATH/logs/monitor.log $INSTALLATION_PATH/logs/action.log &
    PID_MIDDLE=$(pgrep -f lib/middleware/main.py)
    echo "Middleware started to monitor logs of NSO Memory Utilization Tool with PID - $PID_MIDDLE"
}


start_monitoring_daemon

# PID_NCS=$(pgrep -f "\.smp.*-ncs true")
# # startup NSO
# if  [ -z "$PID_NCS" ]; then
#     ncs
# fi

# if NSO is terminated, stop all monitoring processes
while true
do
  PID_NCS=$(pgrep -f "\.smp.*-ncs true")
  if  [ -z "$PID_NCS" ]; then
    cleanup 
    wait
    break
    fi
done