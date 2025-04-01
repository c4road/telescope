
Prioritized:
- docker to have reproductibility.
- code good practices (commit-hooks, Makefile, pip-compile)
- logging
- OpenApi documentation
- unittests
- script to hit the API
- BONUS: Added is_saas check based in description and industry keywords
- BONUS: Added a similar companies field based of the ones that pass the rule constraint

Room for improvement:
- Authentication, Security
- CI/CD pipeline
- Automated loading companies fixtures when running the applications instead of using import_companies.sh
- Improve packaging of no python files (MANIFEST.in)
- Improve version bumping
- Used basic API  views for flexibility we can use fancy classes from DRF for simple APIs.
- Metrics and Dashboards
- Helm templates for K8s deployment
- Health check API (It could be some endpoint that checks the connection to the DB, also it could be automatically hit on a K8s deployment)


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
