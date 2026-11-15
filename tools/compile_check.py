#!/usr/bin/env python3
"""Compile check for this mod without starting the game.

Drives Sharp Terrain's tools/compile_check.py (vanilla shader cache entry, this mod's
Code blocks applied on top, DXC) with this repository as the mod and the coat of arms
mesh effect as the main target, in both the low and the high spec permutation.

usage: compile_check.py --dxc <dxc dir> [--sharp <Sharp Terrain repo>] [-k]
"""
import argparse, importlib.util, os, sys

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF_SHARP = os.path.join(os.path.dirname(MOD), 'ck3-lowspec-terrain-fix')

ap = argparse.ArgumentParser()
ap.add_argument('--sharp', default=DEF_SHARP, help='the Sharp Terrain Without Advanced Shaders repo')
a, rest = ap.parse_known_args()

base = os.path.join(a.sharp, 'tools', 'compile_check.py')
if not os.path.exists(base):
    sys.exit(f'Sharp Terrain checker not found: {base}\nPass --sharp <repo>.')

spec = importlib.util.spec_from_file_location('sharp_compile_check', base)
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

cc.MOD = MOD
cc.TARGETS = [
    ('pdxmesh.shader', 'standard_usercolor_coa', True, 'vanilla'),
    ('pdxmesh.shader', 'standard_usercolor_coa', False, 'vanilla'),
    ('pdxmesh.shader', 'standard_usercolor', True, 'vanilla'),
    ('pdxmesh.shader', 'standard', True, 'vanilla'),
]
cc.VARIANTS = [('default', [])]

sys.argv = [base] + rest
cc.main()
