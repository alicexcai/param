from pypet import Environment
import h5py

h5py.Dataset.__doc__ = ''

def multiply(traj):
    z = traj.x + traj.y
    traj.f_add_result('z', z)
    

env_new = Environment()
traj_new = env_new.traj
traj_new.f_add_parameter('x', 0, comment='1st dim')
traj_new.f_add_parameter('y', 0, comment='2nd dim')
traj_new.f_explore(dict(x=[1,2,3,4], y=[5,6,7,8]))
env_new.run(multiply)