from pathlib import Path
import yaml


class Config:
    _config = None

    @classmethod
    def load(cls, path=None):

        if cls._config is not None:
            return cls._config

        if path is None:
            path = Path(__file__).parent / "config_master.yaml"

        try:
            with open(path, "r", encoding="utf-8") as f:
                cls._config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise RuntimeError(f"Config file not found: {path}")

        return cls._config

    @classmethod
    def get(cls, key_path, default=None):

        value = cls.load()

        for key in key_path.split("."):

            if not isinstance(value, dict):
                return default

            if key not in value:
                return default

            value = value[key]

        return value

    @classmethod
    def reload(cls):
        cls._config = None
        
