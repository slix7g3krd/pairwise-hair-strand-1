"""第 60 批：角色转身时发梢边缘一圈发黑，换成短 groom 后发根直接穿出头..."""

def root_bone(root, offset):
    """发根跟随骨骼。"""
    raise NotImplementedError("TODO: root_bone")

def prepass_alpha(alpha, cutoff):
    """深度预pass Alpha。"""
    raise NotImplementedError("TODO: prepass_alpha")

def dual_highlight(light_a, light_b):
    """双光高光。"""
    raise NotImplementedError("TODO: dual_highlight")

def alpha_threshold(alpha, msaa):
    """MSAA 下 Alpha 阈值。"""
    raise NotImplementedError("TODO: alpha_threshold")

def lod_map(lod, max_lod):
    """groom LOD 映射。"""
    raise NotImplementedError("TODO: lod_map")

def wind_substep(wind, dt, substeps):
    """风场子步。"""
    raise NotImplementedError("TODO: wind_substep")

def backlight_shadow(shadow, backlight):
    """背光发根阴影。"""
    raise NotImplementedError("TODO: backlight_shadow")

def density_uv(u, scale):
    """毛发密度 UV。"""
    raise NotImplementedError("TODO: density_uv")

def depth_offset(depth, offset):
    """发丝深度偏移。"""
    raise NotImplementedError("TODO: depth_offset")

def sort_isolation(character_id, buffer_id):
    """发丝排序隔离键。"""
    raise NotImplementedError("TODO: sort_isolation")

def hat_collision(distance, radius):
    """帽子碰撞。"""
    raise NotImplementedError("TODO: hat_collision")

def bone_lag(current, previous, max_lag):
    """异步骨骼滞后。"""
    raise NotImplementedError("TODO: bone_lag")

def hdr_highlight(value, max_value):
    """HDR 高光夹取。"""
    raise NotImplementedError("TODO: hdr_highlight")
