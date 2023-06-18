#!/usr/bin/python3
from fabric.api import env, run, put
from os.path import exists
env.hosts = ['52.87.222.61', '52.86.63.6']

def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')
        
        # Extract the archive to the /data/web_static/releases/ directory
        filename = archive_path.split('/')[-1]
        folder_name = '/data/web_static/releases/' + filename.split('.')[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))
        
        # Delete the archive from the web servers
        run('rm /tmp/{}'.format(filename))
        
        # Move the files from the extracted folder to its final destination
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))
        
        # Delete the existing symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(folder_name))
        
        print('New version deployed!')
        return True
    except Exception as e:
        print('Deployment failed:', str(e))
        return False
