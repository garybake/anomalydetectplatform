JUPYTER_DIR := ${CURDIR}/jupyter

jupyter_build:
	docker build -t garyb/anomalydetect ${JUPYTER_DIR}

jupyter_run:
	docker run --rm -p 8080:8080 -v ${JUPYTER_DIR}:/src garyb/anomalydetect

service_run:
	cd ./service && uvicorn main:app --reload