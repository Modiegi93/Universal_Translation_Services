#!/usr/bin/python3
from fabric.api import env, run, put
from os.path import exists
env.hosts = ['52.87.222.61', '52.86.63.6']

def do_deploy(archive_path):

    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]

        # Upload archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/{}'.format(archive_name))

        # Uncompress the archive to /data/web_static/releases/<archive filename without extension> on the web server
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(archive_name, archive_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_name))

        # Move the uncompressed files to the proper location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(archive_no_ext, archive_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_no_ext))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version of your code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_no_ext))

        print("New version deployed!")
        return True

    except:
        return False

    """if not exists(archive_path):
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
        return False"""
