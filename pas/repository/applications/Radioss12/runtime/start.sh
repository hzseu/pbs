#!/bin/bash
export HW12_HOME=/data/apps/hw12.0/altair/
export ALTAIR_LICENSE_PATH=6200@192.168.40.66

###########plmpi##################
export MPI_ROOT=/data/apps/plmpi
export PATH=${HW12_HOME}/hwsolvers/radioss/bin/linux64:$MPI_ROOT/bin:$PATH
export LD_LIBRARY_PATH=${HW12_HOME}/hm/bin/linux64:${HW12_HOME}/hwsolvers/common/bin/linux64:$MPI_ROOT/lib/linux_amd64:$LD_LIBRARY_PATH

cp ${HW12_HOME}/hwsolvers/common/bin/linux64/radflex_12_linux64 ./

ulimit -s unlimited
ulimit -l unlimited
unset OMP_NUM_THREADS
unset NCPUS
export OMP_NUM_THREADS=1

NP=`cat ${PBS_NODEFILE} | wc -l`
#####################STARTER_CMD###########
/data/apps/hw12.0/altair/hwsolvers/radioss/bin/linux64/s_12.0.210_linux64 -np ${NP} -input $STARTERFILE

#########COPY FILE##############
#for i in `uniq ${PBS_NODEFILE}|sed '1d'`
#do
#scp -r ${PBS_JOBDIR}/*  ${i}:${PBS_JOBDIR}/
#done
#/bin/sleep 60s
##############

bhosts=`uniq -c $PBS_NODEFILE|awk '{print $2":"$1}'|tr '\n' ','`
#bhosts=`uniq -c $PBS_NODEFILE`
echo ${bhosts} > hostlist
#############ENGIN_CMD#################

cmd="${MPI_ROOT}/bin/mpirun -e MPI_REMSH=/usr/bin/ssh -stdio=i0 -np ${NP} -hostlist ${bhosts} ${PAS_EXECUTABLE} -i $ENGINEFILES "
echo $cmd
${cmd}
