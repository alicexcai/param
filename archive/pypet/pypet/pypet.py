from pypet import Environment

def multiply(traj):
    z = traj.x + traj.y
    traj.f_add_result('z', z)
    

env = Environment()
traj = env.traj
traj.f_add_parameter('x', 0, comment='1st dim')
traj.f_add_parameter('y', 0, comment='2nd dim')
traj.f_explore(dict(x=[1,2,3,4], y=[5,6,7,8]))
env.run(multiply)
