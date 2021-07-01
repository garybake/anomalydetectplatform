JUPYTER_DIR := ${CURDIR}/jupyter
SERVICE_DIR := ${CURDIR}/service

jupyter_build:
	docker build -t garyb/anomalydetect ${JUPYTER_DIR}

jupyter_run:
	docker run --rm -p 8080:8080 -v ${JUPYTER_DIR}:/src garyb/anomalydetect

service_build:
	docker build -t garyb/lp-service ${SERVICE_DIR}

service_run:
	docker run --rm -p 8000:8000 -v ${SERVICE_DIR}:/src garyb/lp-service

service_run_local:
	cd ./service && uvicorn main:app --reload