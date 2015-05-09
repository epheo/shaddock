import docker

def docker_check(self, app_args, param):

    docker_host = app_args.docker_host
    docker_version = app_args.docker_version
    docker_api = docker.Client(base_url=docker_host,
                               version=docker_version,
                               timeout=10)

    try:
        status = [c['Status'][:2].lower()
                  for c in docker_api.containers()
                  if (c['Names'][0][1:] == param['name'])][0]
    except IndexError:
        status = 'down'
    if param['status'] in ['running', 'up']:
        if status == 'up':
            ret = True
        else:
            ret = False
    elif param['status'] in ['stopped', 'down']:
        if status == 'up':
            ret = False
        else:
            ret = True
    return ret