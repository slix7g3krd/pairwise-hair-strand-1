"""第 60 批：角色转身时发梢边缘一圈发黑，换成短 groom 后发根直接穿出头..."""

# Without MSAA the alpha test has to keep wispy tips, so it cuts low.
# With MSAA the partial-coverage fringe is resolved by the samples, so the
# cut-off is raised to the coverage midpoint; leaving it low is what turns
# every strand edge into a hard stair-step.
HARD_ALPHA_CUTOFF = 0.25
MSAA_ALPHA_CUTOFF = 0.5


def root_bone(root, offset):
    """发根跟随骨骼。

    发根位置必须在骨骼空间里做完整平移，而不是只对发梢用固定切线。
    ``root``/``offset`` 是 (x, y) 二元组，逐分量相加后返回新的二元组。
    """
    return (root[0] + offset[0], root[1] + offset[1])


def prepass_alpha(alpha, cutoff):
    """深度预pass Alpha。

    透明发丝只在预pass 里写入超过阈值的片元，阈值刚好相等时也要写，
    否则边界处会出现只写深度不写颜色的空洞。
    """
    return bool(alpha >= cutoff)


def dual_highlight(light_a, light_b):
    """双光高光。

    Kajiya 高光必须按参与光照的两束光的最大贡献取，而不是把第二盏灯
    的强度也乘到主光方向上——否则第二盏灯会把发丝照成塑料。
    """
    return max(light_a, light_b)


def alpha_threshold(alpha, msaa):
    """MSAA 下 Alpha 阈值。

    MSAA 打开时把裁切阈值抬到覆盖中点，让采样点负责边缘渐变；
    未开 MSAA 时保持较低的裁切值以保留细发梢。
    """
    cutoff = MSAA_ALPHA_CUTOFF if msaa else HARD_ALPHA_CUTOFF
    return bool(alpha >= cutoff)


def lod_map(lod, max_lod):
    """groom LOD 映射。

    groom 切换时层级可能高于目标资产提供的最大 LOD，必须夹取，
    否则发根和发梢会按不同层级采样而错位。
    """
    max_lod = max(0, int(max_lod))
    return max(0, min(int(lod), max_lod))


def wind_substep(wind, dt, substeps):
    """风场子步。

    风力积分必须按帧时间均分到每个子步，不能每步都用整帧 dt，
    否则低帧率下发丝会被放大抖动直到抖散。
    """
    count = max(1, int(substeps))
    return wind * dt / count


def backlight_shadow(shadow, backlight):
    """背光发根阴影。

    发丝阴影要同时投到主光和背光，只要有任一盏灯参与就不能跳过，
    否则背光一侧的发根会浮空。
    """
    return bool(shadow or backlight)


def density_uv(u, scale):
    """毛发密度 UV。

    密度图必须和发丝用同一套 UV（u 乘缩放），不能另算一套，
    否则发缝处会采到错误的密度而出现黑块。
    """
    return u * scale


def depth_offset(depth, offset):
    """发丝深度偏移。

    相机拉近后发丝几何被放大、深度精度下降，需要按片元深度施加
    偏移把发丝推到头皮之前，避免自遮挡。
    """
    return depth + offset


def sort_isolation(character_id, buffer_id):
    """发丝排序隔离键。

    每个角色的发丝排序缓冲相互独立，键里带上角色 id 才能防止
    多角色共用一张缓冲时切换角色串发。
    """
    return f"{character_id}:{buffer_id}"


def hat_collision(distance, radius):
    """帽子碰撞。

    帽檐不是球体，但到帽檐的最近距离小于碰撞半径即视为穿透，
    返回是否发生碰撞。
    """
    return distance < radius


def bone_lag(current, previous, max_lag):
    """异步骨骼滞后。

    异步模拟拿到的骨骼可能比上一帧跳变超出预算（快速转头、重绑定）。
    差值在 ``max_lag`` 以内时采用当前帧；超出则视为过期/瞬移样本，
    回退到上一帧的稳定姿态，避免发根被瞬移拉飞。
    """
    if abs(current - previous) > max_lag:
        return previous
    return current


def hdr_highlight(value, max_value):
    """HDR 高光夹取。

    Kajiya 高光在 HDR 下会远超材质上限，需要在写入前夹到 [0, max_value]，
    否则边缘会被烧白。
    """
    return min(max(value, 0.0), max_value)
