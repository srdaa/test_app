DC = docker-compose
LOGS = docker logs
DEV_FILE = ./dev.yaml
CONTAINER_NAME = django-app


.PHONY: dev
dev:
	${DC} -f ${DEV_FILE} up --build 

.PHONY: dev-logs
dev-logs:
	${LOGS} ${CONTAINER_NAME} -f

.PHONY: dev-down
dev-down:
	${DC} -f ${DEV_FILE} down