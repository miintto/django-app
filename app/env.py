import os

from dotenv import find_dotenv, load_dotenv


def load_dotenv_file(base_url):
    if "SECRET_KEY" in os.environ.keys():
        return

    dotenv_path = find_dotenv(
        f"{base_url}/.env", raise_error_if_not_found=True
    )
    load_dotenv(dotenv_path=dotenv_path)
