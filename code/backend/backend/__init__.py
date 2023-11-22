import uvicorn
import logging

from backend.config import Config

def start():
    config = Config()

    logging.getLogger("main").info("Loaded configuration...")
    logging.getLogger('main').info(f'start at {config["host"]}:{config["port"]}')

    uvicorn.run("backend.routes:app", host=config['host'], port=int(config['port']), ssl_keyfile=config['ssl_keyfile'], ssl_certfile=config['ssl_certfile'], reload=True)

if __name__ == '__main__':
    start()


