from dotenv import load_dotenv


def load_environments():
    env_path_workspace = '.one.workspace'
    load_dotenv(dotenv_path=env_path_workspace)


def create_credential(credential, path):
    file = ''
    for key, value in credential.items():
        file += '%s=%s\n' % (key, value)

    with open(path, 'w+') as f:
        f.write(file)
        f.close()
