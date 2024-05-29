SERVICES=all

# Target to initialize the environment
init:
	@echo "Initializing the environment..."
	bash init.sh

build:
	bash build.sh

install:
	bash install.sh

start:
	bash start.sh

test:
	bash test.sh

run-frontend:
	bash service-frontend.sh

run-backend:
	bash service-backend.sh

run-container:
	bash run-container.sh

deploy:
	bash deploy.sh

deploy-frontend:
	bash deploy-frontend.sh

deploy-backend:
	bash deploy-backend.sh