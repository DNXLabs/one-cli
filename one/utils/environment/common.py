from dotenv import load_dotenv


def load_environments():
    env_path_workspace = '.one.workspace'
    load_dotenv(dotenv_path=env_path_workspace)
