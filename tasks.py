from invoke import task

@task(aliases=['del'])
def delete(c):
    c.run("rm *mykmeanssp*.so")

@task
def run(c, k=-1, n=-1, Random=True):
    # informative massage for the user
    n_max_capacity_3d, k_max_capacity_3d = 400,20
    n_max_capacity_2d, k_max_capacity_2d = 420 , 20
    print("The max capacity for d=2 is n=" + str(n_max_capacity_2d) + " , k=" + str(
         k_max_capacity_2d))
    print("The max capacity for d=3 is n=" + str(n_max_capacity_3d) + " , k=" + str(
        k_max_capacity_3d))

    # building the so file
    c.run("python3.8.5 setup.py build_ext --inplace")


    # start the main program
    if Random:
        c.run("python3.8.5 main.py " + str(k) + " " + str(n))
    else:
        c.run("python3.8.5 main.py " + str(k) + " " + str(n) + " --no-Random")

