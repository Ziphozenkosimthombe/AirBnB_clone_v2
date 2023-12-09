#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers
"""

from fabric.api import local, put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ['35.153.18.76', '34.207.64.103']


def do_pack():
    """Packs the web_static folder into a .tgz archive"""
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{current_time}.tgz"
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web
    servers using the do_deploy function"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        """ Extract archive to /data/web_static/releases/
        <archive filename without extension>
        """
        archive_filename = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/{}'.format(
            archive_filename.split('.')[0])
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents of web_static folder to release folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print('New version deployed!')
        return True

    except Exception:
        return False
