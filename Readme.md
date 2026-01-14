# NSO Proactive Memory Handling Toolset
This repository present a external toolset that startup a rescue script and operate beside NSO to take care of the NSO during Out of Memory scenario. The design of the toolset is shown as the diagram below. We create the Rescue Script as shown in the red box. Inside the rescue script we monitor the memory utilization with [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool)
  than proceed with the action in the middleware.  
![image](image/image.png)

## Action Proceed
The tool will monitor two logs from the [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool) and proceed with different action. 
* Warning - Collect 3 debug dump with 1 second apart
* Critical - Kill NSO with SIGUSR1 instead of SIGKILL from OOM Killer. 

If you want to create your own customized action, you can modify the log_inspection function in lib/middleware/main.py.


## Usage
The method below shows how to startup the toolset. The toolset only can be startup under the root path of the toolset(not in any of the subfolder). 
### Prequisition
Run the following command to build the relevant dependency
```
make build
```

### Manual Method
1. Make sure NSO is up. If NSO is down, the tool will terminate automatically
2. Startup [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool) in one terminal with the following command
```
cd $PWD/lib/memory_utilization_tool/ ;bash plot.sh -v -m NaN &> $PWD/logs/monitor.log
```
3. Startup middleware from another terminal with the following command
```
    python $PWD/lib/middleware/main.py $PWD/logs/monitor.log $PWD/logs/action.log
```
4. The middleware will now monitor the output of the [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool). Incase the WARNING or CRIT is printed for allocated or used memory, the middleware will proceed with the action. 


### Automatic Method
* Start up the rescue script in the backend with main.sh
```
make start_backend
```

* Or the rescue script in the front end
```
make start_frontend
```

