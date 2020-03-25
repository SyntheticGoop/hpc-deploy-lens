source $lensdir/Examples/rand10x40.in
loadExamples $lensdir/Examples/rand10x40.ex

setObject batchSize 1500

# `trainParallel` Triggers the job to be distributed across the clients.
trainParallel 5000 -n -r 100