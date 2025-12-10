from pathlib import Path
from dynaconf import Dynaconf
from dynaconf import Validator

BASE_DIR = Path(__file__).resolve().parent

settings = Dynaconf(
    envvar_prefix="SIMBORA",
    settings_files=[
        BASE_DIR / 'settings.toml',
        BASE_DIR / '.secrets.toml',
    ],
    environments=True,
    default_env='development',
    env_switcher='SIMBORA_ENV',
    load_dotenv=True,
    dotenv_path=BASE_DIR / '.env',
    # Validações automáticas
    validators=[
        Validator(
            'secret_key',
            must_exist=True,
            env=['development', 'production', 'testing'],
        ),
        Validator(
            'field_encryption_key',
            must_exist=True,
            env=['development', 'production', 'testing'],
        ),
        Validator(
            'allowed_hosts',
            must_exist=True,
            len_min=1,
            env=['production'],
        ),
        Validator(
            'simbora_password',
            len_min=1,
            env=['development', 'production'],
            # Não obrigatório em testing pois pode usar console backend
        ),
    ],
)

