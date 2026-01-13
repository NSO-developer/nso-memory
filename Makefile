INSTALLATION_PATH="~/git/nso_memory/lib/middleware"

build:
	git clone git@github.com:NSO-developer/nso-memory-utilization-tool.git lib/memory_utilization_tool


start:
	bash main.sh $(INSTALLATION_PATH)
