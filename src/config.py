from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="FOR_DYNACONF",
    settings_files=["settings.yaml"],
    environments=True,
    load_dotenv=True,
)