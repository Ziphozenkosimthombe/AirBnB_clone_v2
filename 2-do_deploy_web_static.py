#!/usr/bin/python3
<<<<<<< HEAD
"""script that generates a .tgz archive from the contents of the web_static"""

from fabric.api import local, task, env, run, settings, put
import os
from datetime import datetime


@task
def do_pack():
    """archive web_static"""
    try:
        f_current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'web_static_{f_current_time}.tgz web_static'
        local("mkdir -p versions")
        local(f"tar -cvzf versions/{file_name}")
        return "versions/"
    except Exception as e:
        return None
=======
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
>>>>>>> f1218a491e0c006e8e88ad30d219c27d0a2fcb66

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

<<<<<<< HEAD
@task
def do_deploy(archive_path):
    """deploy web_static to servers"""
    env.hosts = ['35.153.18.76', '34.207.64.103']
    if not os.path.exists(archive_path):
        return False
    try:
        for host in env.hosts:
            env.host_string = host
            filename = archive_path.split('/')[-1]
            filename = filename.split('.')[0]
            put(archive_path, '/tmp/')
            run(f'mkdir -p /data/web_static/releases/{filename}/')
            run(f'tar -xzf /tmp/{filename}.tgz -C \
                /data/web_static/releases/{filename}/')
            run(f'rm /tmp/{filename}.tgz')
            run(f'mv /data/web_static/releases/{filename}/web_static/* \
                /data/web_static/releases/{filename}/')
            run(
                f'rm -rf /data/web_static/releases/{filename}/web_static')
            run(f'rm -rf /data/web_static/current')
            run(f'ln -s /data/web_static/releases/{filename}/ \
                /data/web_static/current')
            print('New version deployed!')

        return True
    except Exception as e:
=======
        # Move contents of web_static folder to release folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print('New version deployed!')
        return True

    except Exception:
>>>>>>> f1218a491e0c006e8e88ad30d219c27d0a2fcb66
        return False
