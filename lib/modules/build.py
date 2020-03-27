from os.path import abspath
from functools import reduce
from .linewriter import linewriter
from ..bash_snippets.wait_for_file import wait_for_file

def read(file):
  """Loads a file as a string."""
  data = ''
  with open(file, 'r') as read_file:
    data = read_file.read()
  return data

def with_file(file):
  """Select a file to write."""
  def write(data):
    """Write this data to the file."""
    with open(file, 'w+') as write_file:
      write_file.write(data)
  return write

def concat(joiner):
  """String to concatenate a list of strings with."""
  def join(*paths):
    """Joins a list of strings to concatenate."""
    return reduce(lambda a, c: '%s%s%s' % (a, joiner, c), paths)
  return join

def from_folder(root):
  """Joins a list of paths relative to a root folder."""
  def here(*paths):
    """Concatenates a set of paths against the predefined root folder."""
    return concat("/")(root, *paths)
  return here


def build(cache, lens, server, client, workdir, cpu, job, user_id, queue, walltime):
  jobdir = from_folder(workdir)('$PBS_JOBID')
  cachedir = from_folder(jobdir)('.cache')
  logs = from_folder(jobdir)('logs')
  client_script = from_folder(cache)('client.tcl')
  server_script = from_folder(cache)('server.tcl')
  final_script = from_folder(cache)('job.pbs')

  clients = max(cpu - 1, 1)

  setup = linewriter()
  for d in (jobdir, cachedir, logs):
    setup.add('mkdir -p %s' % (d))

  pbs = linewriter()
  pbs.add('#PBS -N %s' % (job))
  pbs.add('#PBS -P %s' % (user_id))
  pbs.add('#PBS -q %s' % (queue))
  pbs.add('#PBS -o %s/pbs.log' % (logs))
  pbs.add('#PBS -e %s/pbs.err' % (logs))
  pbs.add('#PBS -l walltime=%s' % (walltime))
  pbs.add('#PBS -l select=%s:ncpus=1' % (cpu))


  tcl_cfg = linewriter()
  tcl_cfg.add('set __portfile__ "%s/port"' % (from_folder(workdir)('$env(PBS_JOBID)', '.cache')))
  tcl_cfg.add('set __hostname__ "%s/hostname"' % (from_folder(workdir)('$env(PBS_JOBID)', '.cache')))
  tcl_cfg.add('set lensdir "%s"' % (lens))
  tcl_cfg.add('set workdir "%s"' % (from_folder(workdir)('$env(PBS_JOBID)', 'output')))


  server_tcl = linewriter()
  server_tcl.add(tcl_cfg.str())
  server_tcl.add('set __port__ [startServer]')
  server_tcl.add('echo $__port__ > $__portfile__')
  server_tcl.add('echo $env(HOSTNAME) > $__hostname__')
  server_tcl.add('waitForClients %s' % (clients))
  server_tcl.add(read(server))
  server_tcl.add('exit')


  client_tcl = linewriter()
  client_tcl.add(tcl_cfg.str())
  client_tcl.add(read(client))
  client_tcl.add('startClient [exec cat $__hostname__] [exec cat $__portfile__]')
  client_tcl.add('wait')
  client_tcl.add('exit')


  with_file(server_script)(server_tcl.str())
  with_file(client_script)(client_tcl.str())

  batch = linewriter()
  batch.add('%s/run.sh %s 2> %s/server.err 1> %s/server.log &' % (lens, server_script, logs, logs))
  batch.add('server=$!')
  batch.add(wait_for_file('%s/hostname' % (cache), 10))
  for i in range(clients):
    batch.add('%s/run.sh %s 2> %s/client-%s.err 1> %s/client-%s.log &' % (lens, client_script, logs, i, logs, i))
  batch.add('wait $server')


  final = linewriter()
  final.add(pbs.str())
  final.add(setup.str())
  final.add(batch.str())

  with_file(final_script)(final.str())

  return final_script