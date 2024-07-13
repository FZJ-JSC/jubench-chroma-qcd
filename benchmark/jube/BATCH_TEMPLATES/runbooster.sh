#!/usr/bin/bash

#####!/usr/bin/env bash
 
# QUDA specific-environment variables
 
# set the QUDA tunecache path
#export QUDA_RESOURCE_PATH=.
#env
# enable GDR support
export QUDA_ENABLE_GDR=1
 
export CUDA_DEVICE_MAX_CONNECTIONS=1
#export QUDA_MILC_HISQ_RECONSTRUCT=13               # set QUDA-MILC solver optimization
export QUDA_MILC_HISQ_RECONSTRUCT_SLOPPY=9         # set QUDA-MILC solver optimization
# this is the list of GPUs we have
GPUS=(0 1 2 3)
 
# This is the list of NICs we should use for each GPU
 
NICS=(mlx5_0:1 mlx5_1:1 mlx5_2:1 mlx5_3:1)
 
# This is the list of CPU cores we should use for each GPU
# e.g., 2x20 core CPUs split into 4 threads per process with correct NUMA assignment
#CPUS=(48-55 56-63 16-23 24-31 112-119 120-127 80-87 88-95)
CPUS=(3 1 7 5)
#
 
REORDER=(0 1 2 3)
# Number of physical CPU cores per GPU
export OMP_NUM_THREADS=6
 
# this is the order we want the GPUs to be assigned in (e.g. for NVLink connectivity)
 
# now given the REORDER array, we set CUDA_VISIBLE_DEVICES, NIC_REORDER and CPU_REORDER to for this mapping
export CUDA_VISIBLE_DEVICES="${GPUS[${REORDER[0]}]},${GPUS[${REORDER[1]}]},${GPUS[${REORDER[2]}]},${GPUS[${REORDER[3]}]}"
NIC_REORDER=(${NICS[${REORDER[0]}]} ${NICS[${REORDER[1]}]} ${NICS[${REORDER[2]}]} ${NICS[${REORDER[3]}]})
CPU_REORDER=(${CPUS[${REORDER[0]}]} ${CPUS[${REORDER[1]}]} ${CPUS[${REORDER[2]}]} ${CPUS[${REORDER[3]}]})
 
APP="$EXE $ARGS"
 
#lrank=$OMPI_COMM_WORLD_LOCAL_RANK
lrank=$SLURM_LOCALID
echo $lrank
#export UCX_NET_DEVICES=${NIC_REORDER[lrank]}
echo $lrank, $UCX_NET_DEVICES
 
export NVSHMEM_ENABLE_NIC_PE_MAPPING=1
export NVSHMEM_HCA_LIST=$UCX_NET_DEVICES
 
echo ${CPU_REORDER[$lrank]}, ${APP}
echo $EXE, $ARGS
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/pmi/lib/
export UCX_TLS=rc_x,cuda_ipc,gdr_copy,self,sm,cuda_copy
env

numactl --cpunodebind=${CPU_REORDER[$lrank]} --membind=${CPU_REORDER[$lrank]} $APP
