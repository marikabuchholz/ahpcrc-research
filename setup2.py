import os
import sys
import numpy

import input_files

#removes procdirs from previous runs
def removeDirs(nproc):
    for np in nproc:
        procdir = 'np%02d'% np
        if os.path.exists(procdir):
            os.system('rm -r ' + procdir)

def createDirs(prefix, pwdir, tddir, nproc, methods):
    for np in nproc:
        # Create directory
        npdir = 'np%02d'% np
        os.system('mkdir ' + npdir)

        # Create .sbatch file
        sbstr = input_files.getsbatch(np, pwdir, tddir)
        f = open(npdir + '/tddft.sbatch', 'w')
        f.write(sbstr)
        f.close()
        os.system('chmod u+rwx ' + npdir + '/tddft.sbatch')

        # Create .tddft-in file
        #      For now define dt, nstep conv_threshold right here
        dt = 0.5
        nstep = 10
        conv_threshold = 1e-10
        tdstr = input_files.gettdfile(prefix, dt, nstep, conv_threshold)

        f = open(npdir + '/' + prefix + '.tddft-in', 'w')
        f.write(tdstr)
        f.close()

        # Create .pw-in file
        pwstr = input_files.getpw16at(pseudodir)
        f = open(npdir + '/' + prefix + '.pw-in', 'w')
        f.write(pwstr)
        f.close()
        
    return 0

def runparallel(prefix, pwdir, tddir, nproc, methods):
    for np in nproc:
        npdir = 'np%02d'% np
        for method in methods:
            fname ='tddft.sbatch'
            os.system('cd ' + npdir + ' && sbatch ' + fname)

if __name__ == '__main__':
    prefix = 'graphene'
    pwdir = '/home/marikab/espresso/bin'
    tddir = '/home/marikab/espresso/ce-tddft/src'
    pseudodir = '/home/marikab/espresso/pseudo'

    methods = ['cn']
    nproc = [1, 2, 4, 8, 16, 32]

    if len(sys.argv) > 1:
        if sys.argv[1] == 'default':
            removeDirs(nproc)
            createDirs(prefix, pwdir, tddir, nproc, methods)
        if sys.argv[1] == 'parallel':
            runparallel(prefix, pwdir, tddir, nproc, methods)
    else:
        print("Usage:\n\tpython setup.py <option>")
        print("\t\t<option> = default, parallel")

