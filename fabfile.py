#!/usr/bin/python -u

from fabric.api import (
    env,
    execute,
    settings,
    sudo,
    task,
)

from fabric.contrib.project import rsync_project, upload_project

env.use_ssh_config = True
env.colors = True
        
@task
def deploy_lxc_webpanel():
    install = 'wget https://gist.githubusercontent.com/H2so4/971ee995bbdfe1bf8785/raw/42bfc57a4af0d18a7f3ca83af4304a3d9480ca8c/lxc_web_panel_install.sh -O - | bash'
    with settings(sudo_user='root'):
        sudo(install)

@task
def deploy_lxc():
    with settings(sudo_user='root', warn_only=True):
        sudo('''
            add-apt-repository -y ppa:ubuntu-lxc/daily
            apt-get update
            apt-get -y install wget lxc libcgmanager-dev

            lxc-create -t centos -n centos
            [[ $(grep -ir 'lxc.start.auto=1' /var/lib/lxc/centos/config|wc -l) -eq 0 ]] && echo lxc.start.auto=1 >> /var/lib/lxc/centos/config

            lxc-create -t ubuntu -n ubuntu
            [[ $(grep -ir 'lxc.start.auto=1' /var/lib/lxc/ubuntu/config|wc -l) -eq 0 ]] && echo lxc.start.auto=1 >> /var/lib/lxc/ubuntu/config
            ''')


@task
def lxc_host():
    execute(deploy_lxc)
    execute(deploy_lxc_webpanel)

    print(
'''
    Important: 
    If you don't have internet access from your containers after install, reboot the host VM/Server.

    By default you won't be able to ssh in to your container, you must install openssh-server and set a password for the ubuntu sudo_user
    or create a new user with a password.

    The following commands will install openssh-server. at the prompt enter the password for the ubuntu user:
    apt-get update;apt-get install -y openssh-server;passwd ubuntu
'''
        )
