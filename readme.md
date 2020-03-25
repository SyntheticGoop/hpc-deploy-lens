## hpc-deploy-lens
Light Efficient Network Simulator (LENS) is an efficent, yet flexible, neural network simulator.

This application was copied from [here](https://ni.cmu.edu/~plaut/Lens/Manual/introduction.html).

The purpose of this repository is to setup this application to be usable on Nanyang Technological University's HPC cluster running on CentOS 7.

## Deploying the package
The entire package is archived into a tar in the dist folder.
1. Clone this repo.
   - `$repo` is this git repository.
   - `$repo_dir` is the location to clone this to.
   ```bash
   git clone $repo $repo_dir
   ```
1. Edit the run file.
   Within the `server.tcl` and `client.tcl` file, you will have access to the `lensdir` and `workdir` variables. The `lensdir` variable is where the Lens installation is placed and `workdir` is the output working directory set in `run.py`.

   - `run.py`
     Configure the number of concurrent clients and working directories.
   
   - `server.tcl`
     Setup the server execution code.
     The code for starting up and waiting for clients will be automatically injected at runtime.

   - `client.tcl`
     Setup the client execution code.
     The code for connecting the clients and waiting for the server will be automatically injected at runtime.
     Note that you need to have the same model loaded in the client as the server or else lens will crash.

2. Queue the job.
   ```bash
   job=$(python run.py)
   ```

   You can view your running job, run:
   ```bash
   qstat -t $job
   ```

   If you want to double check what files will executed, run:
   ```bash
   python run.py --output-only
   cd .cache
   ```
   This will show you all the automatically generated files.

3. Your output files will be written to the directories specified in `run.py`.
   By default it will be in `session/$PBS_JOBID/` where $PBS_JOBID is the id of the job.

## Debugging
- All runs will produce logs in the `session/$PBS_JOBID/logs` folder.
   1. STDERR is written to `server.err` or `client-$number.err`
   2. STDOUT is written to `server.log` or `client-$number.log`
- You may occasionally need to `ssh` into the execution node to debug your job. To do so you must first check which node you're running on.
   1. To get the node
      ```bash
      qstat -f $job | grep vnode
      ```
      the output will look something like
      `exec_vnode = (hpc-r001:ncpus=1:mem=262144kb:ngpus=1)`
      You will want to ssh the `hpc-r001` portion like so.
      ```bash
      ssh hpc-r001
      ```
      You will now be in the node.
- You may also need to run the job interactively. You can do so by calling the following command.
   ```bash
   qsub -I -l select=1:ncpus=32:mpiprocs=32 -l walltime=04:00:00 -P $my_projectid 
   ```
   Replace `$my_projectid` with your project id.
   Note that you can this will create a job and you can ssh into it multiple times.

If you need to refresh and discard all changes in this repo, you can run:
```bash
git reset --hard
git clean -df
```
Note that this command will delete and reset everything in the folder, including output files.