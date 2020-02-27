#!/bin/bash

#$ -M saguilar@nd.edu
#$ -m abe
# -cwd       		# Change to current working directory job was submitted from
#$ -pe smp 24
#$ -q debug             # Specify queue type # long or debug
#$ -N job_azr       # Specify job's name


module load /afs/crc.nd.edu/user/n/nsl/nuclear/startup/nsl
module load gcc
module load gsl
module load Minuit2
module load qt/5.8.0
#module load azure-upog
module load azure
export OMP_NUM_THREADS=$NSLOTS
#echo $PWD
cd rMatrix/27Al_p
#echo $PWD
azure2 --no-long-wavelength --no-gui --use-brune --ignore-externals --gsl-coul --no-readline /afs/crc.nd.edu/group/nsl/activetarget/users/saguilar/rMatrix/27Al_p/temp.azr <<EOF
2


EOF

