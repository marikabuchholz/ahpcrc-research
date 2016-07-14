import os
import sys
import numpy
 
nproc = [1, 2, 4, 8, 16, 32]

def tddft_sbatch(np, pw_path, tddft_path): 
    string = """#!/bin/bash                                                                                      
#SBATCH --job-name=long-run-"""
    string+= str(np)
    string+="""
#SBATCH --output=cn-tddft.out                                                                   
#SBATCH --error=cn-tddft.err                                                                    
#SBATCH --time=00:10:00                                                                         
#SBATCH --qos=normal                                                                            
#SBATCH --nodes="""
    string+=str(np)
    string+="""
#SBATCH --mem=4000                                                                              
#SBATCH --ntasks-per-node=16                                                                    
##SBATCH --mpi=pmi2
                                                                             
"""
    string+=str(np)
    string+="""

rm -rf *out
mpirun -np """ 
    string+=str(np)
    string+=""" """
    string+=pw_path
    string+=""" < ~/graphene/graphene.pw-in > ~/graphene/graphene.pw-out
mpirun -np """
    string+=str(np)
    string+=""" """
    string+=tddft_path
    string+=""" < ~/graphene/graphene.tddft-in > ~/graphene/graphene.tddft-out
"""
    return string

change_path = raw_input("Change path to pw/tddft files? 1 for yes, 0 for no: ")
if change_path == "1":
    pw_path = raw_input("New pw path: ")
    tddft_path = raw_input("New tddft path: ")
else:
    pw_path = '/home/marikab/espresso-5.2.0/PW/src/pw.x'
    tddft_path = '/home/marikab/ce-tddft-master/bin/tddft.x'

#removes procdirs from previous runs
all_procs = [1, 2, 4, 8, 16, 32]
for np in all_procs:
    procdir = str(np) + 'procs'
    if os.path.exists(procdir):
        os.system('rm -r ' + procdir)

for np in nproc:        
    procdir = str(np) + 'procs'
    os.system('mkdir ' + procdir) #makes a directory for number of processors  
    os.system('cp ~/graphene/graphene.pw-in procdir') #copies pw-in file to procdir
    os.system('cd ~/' + procdir)

    os.system('cp ' + '~/graphene/graphene.pw-in ' + procdir + '/graphene.pw-in')
    os.system('cp ' + '~/graphene/graphene.tddft-in ' + procdir + '/graphene.tddft-in')

    fname = procdir + '/tddft.sbatch'
    if os.path.isfile('~/' + procdir + '/tddft.sbatch*'):
       os.system('rm -r ' + fname)
    
    f = open(fname, "w")
    f.write(tddft_sbatch(np, pw_path, tddft_path))
    os.system('chmod u+x ' + procdir + ' ~/' + fname) 
    os.system('cat /home/marikab/graphene/graphene.pw-out | grep PWSCF | awk \'/PWSCF/{i++}i==3{print $3}\'')
    f.close()

for np in nproc:
    os.system('sbatch ' + str(np) + 'procs/tddft.sbatch')














