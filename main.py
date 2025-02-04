from config.config import config
from tools import validity, certsh

if config.run_hosts:
    validity.runner()

if config.run_certs:
    certsh.check_certsh()
