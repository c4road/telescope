What came first:
- Docker, docker-compose
- logs

## Setup
```
pyenv virtualenv 3.10.14 telescope
pyenv local telescope
pyenv activate
pip install -r requirements.txt
pip install -r dev_requirements.txt
pre-commit install
```

## Development
```
make build
make run
make makemigrations
make migrate
```


## Test
```
make import_companies
make get_companies
make process_companies
make run_tests
```

## Build Wheel
```
make build_package VERSION=0.0.1
```
🚢
