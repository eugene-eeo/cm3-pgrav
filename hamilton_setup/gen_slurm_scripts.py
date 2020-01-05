template = """#!/bin/csh
#SBATCH --job-name="ej-gs-{n}"
#SBATCH -o gustafson.{n}.%A.out
#SBATCH -e gustafson.{n}.%A.err
#SBATCH -p par7.q
#SBATCH -t 01:00:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --mail-user=njzj22@durham.ac.uk
#SBATCH --mail-type=ALL
source /etc/profile.d/modules.sh
module load intel/xe_2017.2
eeojun/gustafson.sh {n}
"""

for n in [1] + list(range(2, 64, 2)):
    script_name = 'gustafson-job-{n}'.format(n=n)
    open(script_name, 'w').write(template.format(n=n))
    print('sbatch eeojun/{script_name}'.format(script_name=script_name))
