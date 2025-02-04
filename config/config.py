import logging
import os
import sys
import time
import tomllib
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler


@dataclass
class EmailConfig:
    from_address: str
    password: str
    smtp_server: str
    smtp_port: int
    to_email: [str]


@dataclass
class Host:
    url: str
    port: int


@dataclass
class Certs:
    name: str


@dataclass
class Config:
    run_hosts: bool
    run_certs: bool
    email_config: EmailConfig
    hosts: [Host]
    certs: [Certs]


def open_config(name):
    path = f"config/{name}.toml"
    try:
        with open(path, "rb") as f:
            _config = tomllib.load(f)
    except FileNotFoundError:
        error_txt = (
            f"No {name} found!\n"
            f"Please configure your config in {path} using the template file!\n"
            f"Stopping Execution!"
        )
        print(error_txt)
        sys.exit(1)
    return _config


_config = open_config("config")

_email_conf = EmailConfig(**_config["email_config"])
_host = [Host(**host) for host in _config["hosts"]]
_certs = [Certs(**cert) for cert in _config["certs"]]

config = Config(
    run_hosts=_config["run_hosts"],
    run_certs=_config["run_certs"],
    email_config=_email_conf,
    hosts=_host,
    certs=_certs,
)
