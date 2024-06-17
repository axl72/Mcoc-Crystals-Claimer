from environs import Env
from dotenv import load_dotenv

load_dotenv()

env = Env()


class Envs:
    EMAIL = env.str("EMAIL")
    DRIVER_PATH = env.str("DRIVER_PATH")
    PASSWORD = env.str("PASSWORD")
    URL = env.str("URL")
