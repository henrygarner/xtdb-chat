install:
	pip3 install -r requirements.txt
run:
	PYTHONPATH=xtdb_chat python3 -m main
test:
	PYTHONPATH=xtdb_chat python3 -m evals
docker:
	docker build -t xtdb_chat .
	docker run -e OPENAI_API_KEY --name xtdb_chat xtdb_chat:latest
drun:
	docker exec -it xtdb_chat /bin/bash -c "export DBHOST=host.docker.internal" && make run

