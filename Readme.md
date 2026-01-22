# NSO Proactive Memory Handling Toolset
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/NSO-developer/nso-memory)


This repository present a external toolset that startup a rescue script and operate beside NSO to take care of the Out of Memory scenario during NSO operation. The repository shows the application usage of the latest NSO Memory Best Practices by create a Rescue Script works beside the NSO as shown in the red box. The rescue script will incharge of the monitor the memory utilization of the NSO and proceed with the action described in the Action Proceed chapter below. At the same time, generate diagram of how memory utilization looks like with the help of the [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool)  
![image](image/theory.png)  

The architecture of the toolset is shown as the diagram below. Inside the rescue script we monitor the memory utilization with [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool). The middle script will inspect the logs of [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool) than proceed with the action that defined in the callback function.  
![image](image/arch.png)

## Action Proceed
The tool will monitor two logs from the [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool) and proceed with different action. 
* Warning - Collect 3 debug dump with 1 second apart
* Critical - Kill NSO with SIGUSR1 instead of SIGKILL from OOM Killer. In this case, crash dump can be generated when vm.overcommit_memory=0 before the OOM Killer step in.

Diagram wll be generated from [NSO Memory Utilization Measurement Tool](https://github.com/NSO-developer/nso-memory-utilization-tool) as usual for troubleshooting. Combine the logs with the diagram generated together with the extra information captured above will make troubleshooting much easier. At the same time, handle the critical scenario in a much graceful way. 

### Create your own Action
If you want to create your own customized action at different alarm level, modify the following callback function in lib/middleware/callbacks.py.

#### Physical Memory Handling
* Define handling action when physical memory is at normal range
```
info_phy(logger,ncssmp_pid=None,overcommit_mode=None)
```
* Define handling action when physical memory is over Warning Level but did not reach the Critical Level
```
warning_phy(logger,ncssmp_pid=None,overcommit_mode=None)
```
* Define handling action when physical memory is over Critical Level
```
crit_phy(logger,ncssmp_pid=None,overcommit_mode=None)
```

#### Allocated Memory Handling
* Define handling action when allocated memory is at normal range
```
info_alloc(logger,ncssmp_pid=None,overcommit_mode=None)
```
* Define handling action when allocated memory is over Warning Level but did not reach the Critical Level
```
warning_alloc(logger,ncssmp_pid=None,overcommit_mode=None
```
* Define handling action when allocated memory is over Critical Level
```
crit_alloc(logger,ncssmp_pid=None,overcommit_mode=None)
```

## Usage
The method below shows how to startup the toolset. The toolset only can be startup under the root path of the toolset(not in any of the subfolder). 
### Prequisition
Run the following command to build the relevant dependency
```
make build
```

### Automatic Method
* Start up the rescue script in the backend with main.sh
```
make start_backend
```

* Or the rescue script in the front end
```
make start_frontend
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




## Copyright and License Notice
```
Copyright (c) 2026 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
```

