# scouts-wwdb-api

This is the django api repository for the scouts werkwinkels project.

## Lokale installatie

De dependencies staan in `pyproject.toml` (sectie `[project]`), de vastgezette versies in `uv.lock`.
Installeer [uv](https://docs.astral.sh/uv/). uv installeert zelf Python 3.11, de versie van de server.

```bash
# installeer de dependencies uit uv.lock in .venv
uv sync --python 3.11

# na een wijziging aan dependencies in pyproject.toml: werk uv.lock bij en commit beide
uv lock

# draai een commando in de omgeving
uv run python src/manage.py runserver
```

De taken `just install` en `just uv-lock` in de `justfile` gebruiken dezelfde commando's.
