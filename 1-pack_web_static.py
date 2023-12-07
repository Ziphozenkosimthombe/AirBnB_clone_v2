#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the contents of the web_static folder the AirBnB Clone repo, using the function do_pack

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive filename (web_static_<year><month><day><hour><minute><second>.tgz)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_name = "web_static_{}.tgz".format(timestamp)

        # Create the archive using tar
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path if successful
        return "versions/{}".format(archive_name)
    except Exception as e:
        # Print an error message and return None if an exception occurs
        return None
