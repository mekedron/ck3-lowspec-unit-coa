# Unit Coats of Arms Without Advanced Shaders (CK3)

Сохраняет гербы на щитах армейских юнитов и на парусах кораблей при выключенной настройке
**«Дополнительные эффекты шейдеров»**. Ваниль с этой настройкой их убирает: на щитах и
парусах остаются только цвета державы.

## Причина

Модели юнитов и кораблей рисуются эффектом `standard_usercolor_coa` из
`game/gfx/FX/pdxmesh.shader`. Его пиксельный шейдер берёт герб владельца из атласа флагов
и смешивает его с участками текстуры, отмеченными под геральдику, — но это чтение стоит за
одной директивой препроцессора:

    #if defined( COA ) && !defined( LOW_SPEC_SHADERS )
        float4 CoAAtlasSlot = GetUserData( Input.InstanceIndex, USER_DATA_ATLAS_SLOT );
        float2 FlagCoords = CoAAtlasSlot.xy + ( MirrorOutsideUV( Input.UV1 ) * CoAAtlasSlot.zw );
        UserColor = lerp( UserColor, PdxTex2D( FlagTexture, FlagCoords ).rgb, Properties.r );
    #endif

`LOW_SPEC_SHADERS` определяется для всех шейдеров, когда дополнительные эффекты выключены,
поэтому герб вырезается при компиляции и остаётся только тонировка `USER_COLOR` над ним.

## Исправление

`gfx/FX/pdxmesh.shader` — ванильный файл, в котором это условие снято: герб читается и в
low spec. Остальной low spec путь (вершинные нормали, дешёвое освещение, без теней) не
тронут.

Цена — одно чтение текстуры на пиксель и только у мешей с эффектом
`standard_usercolor_coa`, то есть у моделей юнитов и кораблей, а это малая часть экрана.
Все остальные меши компилируются ровно в ванильный код.

Изменение стоит за `#define UNITCOA_LOWSPEC` в начале общего блока кода `PixelShader`;
закомментируйте его, чтобы вернуть ванильное поведение.

## Совместимость

* Заменяет `gfx/FX/pdxmesh.shader` целиком, поэтому конфликтует с любым модом, который
  несёт этот файл, — в том числе с *A Game of Thrones*, у которого свой `pdxmesh.shader`.
  Побеждает мод, стоящий ниже в порядке загрузки.
* Совместим с Sharp Terrain, Real Snow, Better Water и Visible Epidemics: ни один из них
  `pdxmesh.shader` не трогает.
* [All-in-One Map Pack Without Advanced Shaders](https://github.com/mekedron/ck3-lowspec-all-in-one)
  уже содержит этот мод: ставьте либо его, либо этот, но не оба.
* Собран на CK3 1.21.0. После патча игры, меняющего `pdxmesh.shader`, файл нужно
  пересобрать из новой ванильной копии.
* С включёнными дополнительными эффектами ничего не делает — ваниль там гербы и так рисует.

## Установка

    ./install.sh

копирует мод в папку модов CK3 внутри Proton-префикса; затем включите **Unit Coats of Arms
Without Advanced Shaders** в плейсете лаунчера. На Windows скопируйте `gfx/` и
`descriptor.mod` в `Documents\Paradox Interactive\Crusader Kings III\mod\lowspec_unit_coa`
и положите рядом `lowspec_unit_coa.mod` со строкой `path="mod/lowspec_unit_coa"`.

## Проверка

    tools/compile_check.py --dxc <папка с bin/dxc и lib/libdxcompiler.so>

компилирует эффект герба (low и high spec) и два соседних эффекта мешей из шейдерного кэша
игры с кодом этого мода. Нужен репозиторий
[Sharp Terrain](https://github.com/mekedron/ck3-lowspec-terrain-fix) рядом с этим — там
общий проверяльщик.

    tools/check_log.sh

после запуска игры показывает, смонтирован ли мод и не упал ли какой-нибудь шейдер.
