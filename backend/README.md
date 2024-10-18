# Backend API (FastAPI app)

## Development
### Installation
#### Install python3.12 virtual environment and activate it
```commandline
python3.12 -m venv .venv
source .venv/bin/activate
```
#### Install Poetry in the previously created virtual environment
```commandline
pip install poetry
```
#### Install project using poetry
```commandline
poetry config virtualenvs.create false
poetry install --with dev
```

### Testing
#### Run lint checks
```commandline
poetry run task lint
```

#### Run tests locally
```commandline
poetry run task test
```
