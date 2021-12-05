from pypet import Environment, cartesian_product

def multiply(traj):
    """Example of a sophisticated simulation that involves multiplying two values.

    :param traj:

        Trajectory containing the parameters in a particular combination,
        it also serves as a container for results.

    """
    z=traj.x * traj.y
    traj.f_add_result('z',z, comment='I am the product of two values!')

# Create an environment that handles running our simulation
env = Environment(trajectory='Multiplication',filename='./HDF/example_01.hdf5',
                    file_title='Example_01',
                    comment = 'I am the first example!')

# Get the trajectory from the environment
traj = env.trajectory

# Add both parameters
traj.f_add_parameter('x', 1.0, comment='Im the first dimension!')
traj.f_add_parameter('y', 1.0, comment='Im the second dimension!')

# Explore the parameters with a cartesian product
traj.f_explore(cartesian_product({'x':[1.0,2.0,3.0,4.0], 'y':[6.0,7.0,8.0]}))

# Run the simulation with all parameter combinations
env.run(multiply)
