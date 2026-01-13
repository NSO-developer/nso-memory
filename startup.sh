INSTALLATION_PATH=$1

trap "cleanup" SIGKILL 

cleanup () {
    PID_MONITOR=$(pgrep -f plot.sh)
    kill -INT $PID_MONITOR
    PID_MIDDLE=$(pgrep -f lib/middleware/main.py)
    kill -INT $PID_MIDDLE
}

# montior engine
cd $INSTALLATION_PATH/lib/memory_utilization_tool/ ;bash plot.sh -v -m NaN &> $INSTALLATION_PATH/logs/monitor.log &
# middleware action engine
python lib/middleware/main.py $INSTALLATION_PATH/logs/monitor.log &> $INSTALLATION_PATH/logs/action.log &


PID_NCS=$(pgrep -f ncs.smp)
# startup NSO
if  [ -z "$PID_NCS" ]; then
    ncs
fi

while true
do
  PID_NCS=$(pgrep -f ncs.smp)
  if  [ -z "$PID_NCS" ]; then
    cleanup 
    break
    fi
done

wait
