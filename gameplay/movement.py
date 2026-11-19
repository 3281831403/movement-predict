"""角色移动预测：积分、回滚与滑墙：待实现的核心模块。"""


def integrate(position, velocity, accel, dt):
    """积分位置与速度。"""
    raise NotImplementedError

def dead_reckon(position, velocity, latency):
    """航位推演。"""
    raise NotImplementedError

def reconcile(predicted, authoritative, alpha):
    """回滚和解。"""
    raise NotImplementedError

def slide(velocity, normal):
    """沿墙滑动。"""
    raise NotImplementedError

def jump_height(initial_velocity, gravity):
    """跳跃高度。"""
    raise NotImplementedError
