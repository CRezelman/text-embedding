# Text Embedding

This repo serves as an investigation into running a locally run Text Embedding model

## Virtual Environment

### Create

```bash
python -m venv .venv
```

### Activate

```bash
source .venv/Scripts/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Update Dependencies

```bash
pip freeze > requirements.txt
```

## Docker

### Build and Start

```bash
docker compose up --build
```

### Run Detached

```bash
docker compose up --build -d
```

### Watch Logs

```bash
docker compose logs -f
```
