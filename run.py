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
user_id = 'user_id'

# Queue name
# queue = 'q32'
queue = 'q32'

# Walltime (HH:MM:SS): Maximum duration to execute
# before terminating the job
# walltime = '00:15:00'
walltime = '00:15:00'

# Allowed hosts: List of nodes to run on.
only_in = [
  'hpc-n069',
  'hpc-n065',
  'hpc-n052',
  'hpc-n059',
  'hpc-n061',
  'hpc-n062',
  'hpc-n015',
  'hpc-n068',
  'hpc-n003',
  'hpc-n067',
  'hpc-n047',
  'hpc-n048',
  'hpc-n070',
  'hpc-n013',
  'hpc-n007',
  'hpc-n011',
  'hpc-n012',
  'hpc-n016',
  'hpc-n021',
  'hpc-n022',
  'hpc-n023',
  'hpc-n024',
  'hpc-n025',
  'hpc-n026',
  'hpc-n033',
  'hpc-n018'
]



# Runs the job
if __name__ == "__main__":
  pbs = build(
    cache=cache,
    lens=lens,
    server=server,
    client=client,
    workdir=workdir,
    only_in=only_in,
    cpu=cpu,
    job=job,
    user_id=user_id,
    queue=queue,
    walltime=walltime,
  )

  call('mkdir -p %s' % cache, shell=True)

  if '--output-only' not in argv:
    call('qsub %s' % pbs, shell=True)