from services.envs import Envs
from core.claimer import Claimer

if __name__ == "__main__":
    claimer = Claimer(
        driver_path=Envs.DRIVER_PATH,
        email=Envs.EMAIL,
        password=Envs.PASSWORD,
        url=Envs.URL,
    )

    claimer.claim_crystals()
