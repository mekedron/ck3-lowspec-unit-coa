# Unit Coats of Arms Without Advanced Shaders (CK3)

Keeps the coats of arms on the shields of army units and on the sails of ships when the
graphics option **Advanced Shaders** is off. Vanilla drops them with that setting: the
shields and sails show only the plain realm colours.

## Cause

Unit and ship models use the mesh effect `standard_usercolor_coa` from
`game/gfx/FX/pdxmesh.shader`. Its pixel shader reads the owner's coat of arms from the
flag atlas and blends it into the parts of the texture masked for heraldry - but that read
is behind one preprocessor guard:

    #if defined( COA ) && !defined( LOW_SPEC_SHADERS )
        float4 CoAAtlasSlot = GetUserData( Input.InstanceIndex, USER_DATA_ATLAS_SLOT );
        float2 FlagCoords = CoAAtlasSlot.xy + ( MirrorOutsideUV( Input.UV1 ) * CoAAtlasSlot.zw );
        UserColor = lerp( UserColor, PdxTex2D( FlagTexture, FlagCoords ).rgb, Properties.r );
    #endif

`LOW_SPEC_SHADERS` is defined for every shader when Advanced Shaders is off, so the
coat of arms is compiled out and only the `USER_COLOR` tint above it is left.

## Fix

`gfx/FX/pdxmesh.shader` is the vanilla file with that guard lifted: the coat of arms is
read under low spec too. The rest of the low spec path (vertex normals, cheap lighting,
no shadows) stays as it is.

The cost is one texture read per pixel, and only on meshes drawn with the
`standard_usercolor_coa` effect - unit and ship models, a small part of the screen. Every
other mesh compiles to exactly the vanilla code.

The change sits behind `#define UNITCOA_LOWSPEC` at the top of the file's shared
`PixelShader` code block; comment it out to get the vanilla behaviour back.

## Compatibility

* Overrides the whole of `gfx/FX/pdxmesh.shader`, so it conflicts with any other mod that
  ships that file - among them *A Game of Thrones*, which carries its own `pdxmesh.shader`.
  Whichever mod is lower in the load order wins.
* Works alongside Sharp Terrain, Real Snow, Better Water and Visible Epidemics: none of
  them touches `pdxmesh.shader`.
* Built on CK3 1.20.1.2. After a game patch that changes `pdxmesh.shader`, the file has to
  be rebuilt from the new vanilla copy.
* Does nothing with Advanced Shaders on - vanilla already draws the coats of arms there.

## Installing

    ./install.sh

copies the mod into the CK3 mod folder inside the Proton prefix, then enable **Unit Coats
of Arms Without Advanced Shaders** in the launcher playset. On Windows, copy `gfx/` and
`descriptor.mod` into `Documents\Paradox Interactive\Crusader Kings III\mod\lowspec_unit_coa`
and add a `lowspec_unit_coa.mod` next to it with a `path="mod/lowspec_unit_coa"` line.

## Checking it

    tools/compile_check.py --dxc <dir with bin/dxc and lib/libdxcompiler.so>

compiles the coat of arms effect (low and high spec) and two neighbouring mesh effects
from the game's shader cache with this mod's code applied. It needs the
[Sharp Terrain](https://github.com/mekedron/ck3-lowspec-terrain-fix) repository next to
this one for the shared checker.

    tools/check_log.sh

after a game start shows whether the mod was mounted and whether any shader failed to
compile.
