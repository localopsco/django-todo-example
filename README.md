### To create venv (Python Virtual Environment):
Run
```shell
python3 -m venv ~/venv/django_todo
```

### To enter into venv:
Run
```shell
source ~/venv/django_todo/bin/activate
```

### To exit from venv:
Run
```shell
deactivate
```

### To run app inside `venv`:
1. Enter into venv. (Refer above commands to enter into venv)
2. Run
```shell
pip install -r requirements.txt
```
3. Run
```shell
make run
```

### To run tests:
Run
```shell
make test
```

### To run using `docket-compose.yml`:
1. Run
```shell
chmod +x entrypoint.sh
```

2. Run
```shell
docker-compose up
```

OR to rebuild,

Run
```shell
docker-compose up --build be
```

### To push docker image

```shell
make be-docker-push v=0.0.1
```

### To helm install in local

```shell
helm install todo ./helm
```

### To push new helm version

Note: Make sure to run `helm dependency update` inside helm directory before building the helm chart.

```shell
make deploy-helm v=0.0.1
```
