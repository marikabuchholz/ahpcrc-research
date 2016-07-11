import os
import sys
import numpy
 
nproc = [1, 2, 4, 8, 16, 32]
dt = 0.5
nsteps = 1000
pseudodir = '/home/marikab/qe-tddft/pseudo'
fname = '16atoms_results.txt'

def getshellscript(method, nk, dt, prefix, timehours):
    string = """#!/bin/bash 

#SBATCH --job-name="""
    string += method + '-k'+str(nk) + '-dt' + str(dt) + "\n"
    string += """#SBATCH --output=cn-tddft.out
#SBATCH --error=cn-tddft.err
#SBATCH --time="""
    string += str(int(timehours)) + """:00:00
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --mem=4000
#SBATCH --ntasks-per-node=16

#now run normal batch commands
module load openmpi/1.6.5/intel13sp1up1

"""
    string += "PREFIX=" + prefix
    string +="""

rm -rf *out
/home/rehnd/qe-tddft/bin/pw.x < $PREFIX.pw-in > $PREFIX.pw-out
/home/rehnd/qe-tddft/multi-k-tddft/bin/tddft.x < $PREFIX.tddft-in > $PREFIX.tddft-out
"""
    return string

def tddft_sbatch(nproc): 
    string = """#!/bin/bash                                                                                      
#SBATCH --job-name=long-run-"""
    string+= str(nproc)
    string+="""
#SBATCH --output=cn-tddft.out                                                                   
#SBATCH --error=cn-tddft.err                                                                    
#SBATCH --time=00:10:00                                                                         
#SBATCH --qos=normal                                                                            
#SBATCH --nodes=8                                                                               
#SBATCH --mem=4000                                                                              
#SBATCH --ntasks-per-node=16                                                                    
##SBATCH --mpi=pmi2
                                                                             
PREFIX=graphene

rm -rf *out
mpirun -np 8 /home/marikab/espresso-5.2.0/PW/src/pw.x < $PREFIX.pw-in > $PREFIX.pw-out
mpirun -np 8 /home/marikab/ce-tddft-master/bin/tddft.x < $PREFIX.tddft-in > $PREFIX.tddft-out
"""
    return string

for np in nproc:
    procdir = str(np) + 'procs'
    if not os.path.exists(procdir):
        os.system('mkdir ' + procdir) #makes a directory for number of processors - only make it if it doesn't a\
lready exist                                                                                                     
    os.system('cp ./graphene/graphene.pw-in procdir') #copies pw-in file to procdir                              
    f = open(str(np) + 'procs' + fname, "w")
    f.write(tddft_sbatch(np))

    tps = 0.25 #time per solve                                                                                   
    timehours = min(48, int(numpy.ceil(tps*nsteps/3600.)))

    method = '16atoms' + str(np) + 'proc'
    f.write(getshellscript(method, 1, dt, 'graphene', str(timehours)))
    f.close()
    os.system('chmod u+x ' + procdir + ' /home/marikab/graphene/tddft.sbatch*')
    os.system('cat /home/marikab/graphene/graphene.tddft-out | grep -A 4 PW | awk \'{print $4}\'')
    os.system('cat /home/marikab/graphene/graphene.tddft-out | grep -A 4 PW | awk \'{print $7}\'')
