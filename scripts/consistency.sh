#!/bin/bash

ITER=100
FILE="log_tpm_norm.csv"
TOL="1e-7"
NODES=1
TASKS=32
TIME="00:30:00"

NTASKS=$(( NODES * TASKS ))

dir_name=${PWD##*/}

TMP_DIR="$SCRATCH/$dir_name"

if [ ! -f $FILE ]; then
    echo "File $FILE not found!"
    exit 1
fi

n_samples=$(head -1 $FILE | sed 's/[^,]//g' | tr -d '\n' | wc -c)

if [ $n_samples -lt 200 ]; then
    step=5
elif [ $n_samples -lt 500 ]; then
    step=10
else
    step=20
fi

for i in  $(seq $step $step $n_samples)
do

run_script="#!/bin/bash -l
\n
\n#SBATCH -p regular
\n#SBATCH -N $NODES --ntasks-per-node=$TASKS
\n#SBATCH -t $TIME
\n#SBATCH --mail-user=avsastry@eng.ucsd.edu
\n#SBATCH --mail-type=ALL
\n#SBATCH -C haswell
\n
\nmodule load python
\n
\nsrun -n $NTASKS python ../random_restart_ica.py -f $FILE -i $ITER -t $TOL -x $TMP_DIR/$i -d $i
\nsrun -n $NTASKS python ../compute_distance.py -i $ITER -x $TMP_DIR/$i
\nsrun -n 1 -N 1 python ../cluster_components.py -i $ITER -x $TMP_DIR/$i -w $NTASKS
"

    echo "Running iteration $i"
    mkdir $i
    cp $FILE $i
    echo -en $run_script > $i/${dir_name}_$i
    cd $i
    sbatch ${dir_name}_$i
    cd ..
done
