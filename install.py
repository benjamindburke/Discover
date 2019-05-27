import subprocess

modules = ['requests']

for module in modules:
    subprocess.run('python -m pip install --user {0}'.format(module))
