import json
from json import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError

from backend.src.pydantic_models.config import Config

try:
    with open(Path(__file__).parent.parent.parent / 'config.json', 'r') as f:
        try:
            config: Config = Config(**json.load(f))
        except ValidationError as e:
            print(f'Failed to validate: {e}')
        except JSONDecodeError as e:
            print(f'Failed to load config: {e}')
except FileNotFoundError as e:
    print(f'Failed to find config file: {e}')
