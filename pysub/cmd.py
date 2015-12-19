import os
import subprocess


def run_cmd(cmd, silent=None, **kwargs):
    params = {
        'shell': True
    }

    if silent:
        FNULL = open(os.devnull, 'w')
        params['stdout'] = FNULL
        params['stderr'] = subprocess.STDOUT

        # retcode = subprocess.call(['echo', 'foo'], stdout=FNULL, stderr=subprocess.STDOUT)
    params.update(kwargs)

    subprocess.call(cmd, **params)
