"""角色移动预测：积分、回滚与滑墙。

约定：
- 所有向量为同维序列（测试使用三维），函数不会修改入参。
- 位置/速度类返回值为新分配的列表。
- None、空序列等空输入按零向量处理，避免批量预测时个别坏数据中断整批。
"""


def _dim(*vectors):
    """取第一个非空向量的维度，全部为空时退回三维。"""
    for vector in vectors:
        if vector:
            return len(vector)
    return 3


def _as_vec(value, size):
    """把输入规整为定长数值列表；空输入补零，短向量尾部补零。"""
    if not value:
        return [0.0] * size
    vec = [float(component) for component in value]
    if len(vec) < size:
        vec.extend([0.0] * (size - len(vec)))
    return vec


def integrate(position, velocity, accel, dt):
    """积分位置与速度。

    采用恒定加速度解析积分：
        position' = position + velocity * dt + 0.5 * accel * dt ** 2
        velocity' = velocity + accel * dt
    加速度半项保证带加速度时位置不丢位移；dt 为 0/None 时原样返回。
    返回 ``[新位置, 新速度]``。
    """
    size = _dim(position, velocity, accel)
    pos = _as_vec(position, size)
    vel = _as_vec(velocity, size)
    acc = _as_vec(accel, size)
    dt = float(dt) if dt else 0.0

    new_position = [
        pos[i] + vel[i] * dt + 0.5 * acc[i] * dt * dt
        for i in range(size)
    ]
    new_velocity = [vel[i] + acc[i] * dt for i in range(size)]
    return [new_position, new_velocity]


def dead_reckon(position, velocity, latency):
    """航位推演：按网络延迟用当前速度线性外推位置。"""
    size = _dim(position, velocity)
    pos = _as_vec(position, size)
    vel = _as_vec(velocity, size)
    latency = float(latency) if latency else 0.0
    return [pos[i] + vel[i] * latency for i in range(size)]


def reconcile(predicted, authoritative, alpha):
    """回滚和解：在预测位置与权威位置之间按 alpha 线性插值。

    alpha=0 完全保留预测值，alpha=1 完全采用权威值，中间值平滑校正，
    避免联机角色在两个位置之间来回跳。
    """
    size = _dim(predicted, authoritative)
    pred = _as_vec(predicted, size)
    auth = _as_vec(authoritative, size)
    alpha = float(alpha) if alpha else 0.0
    return [pred[i] + alpha * (auth[i] - pred[i]) for i in range(size)]


def slide(velocity, normal):
    """沿墙滑动：去掉速度在法线方向的分量，保留切向分量。

    使用通用投影公式 ``v - (v·n)/(n·n) * n``，法线无需预先单位化；
    法线为零向量（空输入）时无法定义碰撞面，直接返回原速度。
    """
    size = _dim(velocity, normal)
    vel = _as_vec(velocity, size)
    nrm = _as_vec(normal, size)

    norm_sq = sum(component * component for component in nrm)
    if norm_sq <= 0.0:
        return vel

    projection = sum(vel[i] * nrm[i] for i in range(size)) / norm_sq
    return [vel[i] - projection * nrm[i] for i in range(size)]


def jump_height(initial_velocity, gravity):
    """跳跃高度：竖直上抛最大高度 ``v² / (2g)``。

    gravity 缺失或非正时物理上没有有限的抛物顶点，按 0.0 兜底，避免除零。
    """
    if initial_velocity is None or gravity is None or gravity <= 0:
        return 0.0
    return (float(initial_velocity) ** 2) / (2.0 * float(gravity))
