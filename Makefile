INSTALLATION_PATH="~/git/nso_memory/lib/middleware"

build:
	git clone git@github.com:NSO-developer/nso-memory-utilization-tool.git lib/memory_utilization_tool
	sudo apt-get install gnuplot

start_backend:
	bash main.sh

start_frontend:
	bash startup.sh $(PWD)
