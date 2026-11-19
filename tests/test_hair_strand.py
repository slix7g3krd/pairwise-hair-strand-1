import pytest
from render import hair_strand as mod

CASES = [
    ("root", 'm.root_bone((1.0, 2.0), (0.5, 0.5)) == approx((1.5, 2.5))'),
    ("root_zero", 'm.root_bone((0.0, 0.0), (0.0, 0.0)) == approx((0.0, 0.0))'),
    ("prepass", 'm.prepass_alpha(0.5, 0.5) is True'),
    ("dual", 'm.dual_highlight(1.0, 2.0) == approx(2.0)'),
    ("alpha_no_msaa", 'm.alpha_threshold(0.4, False) is True'),
    ("alpha_msaa", 'm.alpha_threshold(0.4, True) is False'),
    ("lod", 'm.lod_map(5, 3) == 3'),
    ("wind", 'm.wind_substep(2.0, 1.0, 2) == approx(1.0)'),
    ("backlight", 'm.backlight_shadow(False, True) is True'),
    ("density", 'm.density_uv(0.5, 2.0) == approx(1.0)'),
    ("depth", 'm.depth_offset(1.0, 0.2) == approx(1.2)'),
    ("sort", 'm.sort_isolation("a", "b") == "a:b"'),
    ("hat", 'm.hat_collision(0.5, 1.0) is True'),
    ("async", 'm.bone_lag(10.0, 8.0, 1.0) == approx(8.0)'),
    ("hdr", 'm.hdr_highlight(2.0, 1.0) == approx(1.0)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
