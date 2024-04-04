#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run, execute

env.hosts = ["104.196.168.90", "35.196.46.172"]
def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False

    commands = [
        "rm -rf /data/web_static/releases/{}/".format(name),
        "mkdir -p /data/web_static/releases/{}/".format(name),
        "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name),
        "rm /tmp/{}".format(file_name),
        "mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name),
        "rm -rf /data/web_static/releases/{}/web_static".format(name),
        "rm -rf /data/web_static/current",
        "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)
    ]

    # Execute commands in parallel on all hosts
    results = execute(run_commands, commands, hosts=env.hosts, parallel=True)

    # Check if any command failed
    if any(result.failed for result in results.values()):
        return False

    return True


def run_commands(commands):
    """Run multiple commands on a host."""
    for command in commands:
        if run(command).failed:
            return False
    return True#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run, execute

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False

    commands = [
        "rm -rf /data/web_static/releases/{}/".format(name),
        "mkdir -p /data/web_static/releases/{}/".format(name),
        "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name),
        "rm /tmp/{}".format(file_name),
        "mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name),
        "rm -rf /data/web_static/releases/{}/web_static".format(name),
        "rm -rf /data/web_static/current",
        "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)
    ]

    # Execute commands in parallel on all hosts
    results = execute(run_commands, commands, hosts=env.hosts, parallel=True)

    # Check if any command failed
    if any(result.failed for result in results.values()):
        return False

    return True


def run_commands(commands):
    """Run multiple commands on a host."""
    for command in commands:
        if run(command).failed:
            return False
    return True
