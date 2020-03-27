from os import getcwd
from lib.modules.build import from_folder, build
from subprocess import call
from sys import argv

# Absolute location of the folder to work from.
# Defaults to the current working directory (getcwd()).
# here = from_folder(getcwd())
here = from_folder(getcwd())

# Cache folder for temporary files.
# cache = here('.cache')
cache = here('.cache')

# Lens directory. Do not modify if lens is not moved.
lens = here('Lens')

# Server script: The script to be run by the server.
# server = './server.tcl'
server = here('server.tcl')

# Client script: The script to be run by the clients.
# client = './client.tcl'
client = here('client.tcl')

# Output directory: Where to output the results to.
# output = './session/'
workdir = here('session')

# CPUs: Number of CPUs to use for processing.
# No fewer than 2 are allowed. If less than 2 is set,
# the job will default to 2.
# cpu = 2
cpu = 12

# Job name
# job = 'LENS'
job = 'LENS'

# Project Funding Code Eg. eee_userid
# user_id = 'user_id'
user_id = 'hpc_admin'

# Queue name
# queue = 'q32'
queue = 'q32_76'

# Walltime (HH:MM:SS): Maximum duration to execute
# before terminating the job
# walltime = '00:15:00'
walltime = '00:15:00'



# Runs the job
if __name__ == "__main__":
  call('mkdir -p %s' % cache, shell=True)

  pbs = build(
    cache=cache,
    lens=lens,
    server=server,
    client=client,
    workdir=workdir,
    cpu=cpu,
    job=job,
    user_id=user_id,
    queue=queue,
    walltime=walltime,
  )

  if '--output-only' not in argv:
    call('qsub %s' % pbs, shell=True)