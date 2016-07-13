import os
import sys
import numpy
 
nproc = [1, 2, 4, 8, 16, 32]
dt = 0.5
nsteps = 1000
prefix = 'graphene'

def tddft_sbatch(np): 
    string = """#!/bin/bash                                                                                      
#SBATCH --job-name=long-run-"""
    string+= str(np)
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
mpirun -np $NP $PW_PATHpw.x < $PREFIX.pw-in > $PREFIX.pw-out
mpirun -np $NP $TDDFT_PATHtddft.x < $PREFIX.tddft-in > $PREFIX.tddft-out
"""
    return string

change_path = raw_input("Change path to pw/tddft files? 1 for yes, 0 for no: ")
if change_path == "1":
    pw_path = raw_input("New pw path: ")
    tddft_path = raw_input("New tddft path: ")
else:
    pw_path = '/home/marikab/espresso-5.2.0/PW/src/'
    tddft_path = '/home/marikab/ce-tddft-master/bin/'

for np in nproc:        
    procdir = str(np) + 'procs'
    if not os.path.exists(procdir):
        os.system('mkdir ' + procdir) #makes a directory for number of processors 
    else:
        os.system('rm -r ' + procdir)
        print "removed"
        os.system('mkdir ' + procdir) 
    os.system('cp ./graphene/graphene.pw-in procdir') #copies pw-in file to procdir
    os.system('cd ~/' + procdir)
    method = '16atoms' + str(np) + 'proc'
    f = open(method + '.txt', "w") 
    f.write(tddft_sbatch(np))

    os.system('mv ' + method + '.txt' + ' ' + '~/' + procdir)
    f.close()
    tps = 0.25 #time per solve
    timehours = min(48, int(numpy.ceil(tps*nsteps/3600.)))

    fname = procdir + '/tddft.sbatch'
    os.system('cp /home/marikab/graphene/tddft.sbatch ~/' + fname)
    os.system('chmod u+x ' + procdir + ' ~/' + fname) 
    os.system('cat /home/marikab/graphene/graphene.pw-out | grep PWSCF | awk \'/PWSCF/{i++}i==3{print $3}\'')















