#!/usr/bin/env python3
"""
AD collection with https://github.com/fox-it/BloodHound.py/
Wrapper to get password from file and not through cli

% bloodhound-python -d DOMAIN -c Default -u USER -v
"""
import datetime
import os
import time
from pathlib import Path
import yaml
import logging
import bloodhound
from bloodhound import BloodHound
from bloodhound.ad.domain import AD
from bloodhound.ad.authentication import ADAuthentication

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    # Retrieve configuration from file
    HOME = str(Path.home())
    secrets_file = os.path.join(HOME, ".adcollection.conf")
    with open(secrets_file, "r", encoding="utf-8") as secrets_fd:
        credentials = yaml.safe_load(secrets_fd)

    # Collection
    auth = ADAuthentication(
        username=credentials["username"],
        password=credentials["password"],
        domain=credentials["domain"],
    )
    ad = AD(
        auth=auth, domain=credentials["domain"], nameserver=credentials["nameserver"]
    )
    if 'domain_controller' in credentials:
        ad.override_dc(credentials['domain_controller'])
    collect = ["group", "localadmin", "session", "trusts"]
    ad.dns_resolve(domain=credentials["domain"])
    timestamp = (
        datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S") + "_"
    )
    bloodhound = BloodHound(ad)
    bloodhound.connect()
    bloodhound.run(
        collect=collect,
    )
