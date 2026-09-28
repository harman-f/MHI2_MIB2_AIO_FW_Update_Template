# MHI2_MIB2_AIO_FW_Update_Template

This repository contains building blocks for custom **A**ll **I**n **O**ne MHI2 firmware updates.

> [!WARNING]
> **This repository is NOT a ready-to-flash firmware update.**
>
> It is a template/research collection. Firmware train, MU, hardware generation and peripheral-device compatibility must be checked before building or applying an AIO package.

## Wiki / background

The [Wiki](https://github.com/harman-f/MHI2_MIB2_AIO_FW_Update_Template/wiki) documents the historical AIO workflow and examples.

## Known historical AIO examples

### VW

- MHI2_ER_VWG11_K3342_1_AIO_MU1427
- MHI2_ER_VWG13_K4525_1_AIO_MU1367 — can also be used as the basis for the documented G11 -> G13 conversion workflow

### Skoda

- MHI2_ER_SKG11_K3343_1_AIO_MU1433
- MHI2_ER_SKG13_P4526_1_AIO_MU1440 — can also be used as the basis for the documented G11 -> G13 conversion workflow

### SEAT

- MHI2_ER_SEG11_P4709_1_AIO_MU1447

### Porsche

- MHI2_ER_POG11_K5126_1_AIO_MU1394
- MHI2_ER_POG24_K5137_1_AIO_MU1417
- MHI2_US_POG11_K5186_1_AIO_MU1476
- MHI2_US_POG24_K5136_1_AIO_MU1416

### Audi

- MHI2_ER_AU57x_K3663_1_MU1425_AIO — not based directly on this template, but follows a related approach

These are historical examples, **not a claim that every later unit in the same train family is compatible**. In particular, reports from newer Porsche P5250/P5251-era units show that broad train wildcards are not a safe compatibility rule.

## Features represented by the template

- Automatic firmware-update start after inserting the prepared SD card
- Patched IFS-root support
- FEC container extension through `common/tools/addFecs.txt`
- CarPlay / Android Auto coding
- Developer Mode / GEM coding
- WLAN coding
- M.I.B. launcher integration
- Optional navigation activation / target-specific actions
- Basic backup before post-install changes
- Installation logging to SD
- Separate generic and firmware-specific post-install script layers

## New: host-side reference hash helper

The repository now includes:

```text
tools/rebuild_reference_hashes.py
```

It intentionally **does not build or edit `metainfo2.txt`**. It handles the repetitive reference hashes so the metainfo can still be assembled and reviewed manually.

Rebuild `common/tools/0/default/hashes.txt` from the actual files below it:

```bash
python3 tools/rebuild_reference_hashes.py tool-dir
```

Check the existing manifest without changing it:

```bash
python3 tools/rebuild_reference_hashes.py tool-dir --check
```

Generate `FileName`, `FileSize` and SHA-1 for manual metainfo entry:

```bash
python3 tools/rebuild_reference_hashes.py file common/tools/0/default/finalScript.sh
```

Generate numbered chunk hashes for a large referenced image when the target component's chunk size is known:

```bash
python3 tools/rebuild_reference_hashes.py file RCC/ifs-root/31/default/ifs-root.ifs --chunk-size 524288
```

See [tools/README.md](tools/README.md) for the exact scope and limitations.

> [!IMPORTANT]
> The helper hashes the **raw file bytes**. Line endings therefore matter.
>
> The `--chunk-size` value must be verified for the target firmware/component. 512 KiB is useful for known research examples, but is not declared universal by this repository.

## Important lessons from field reports

### Keep compatibility narrow

Do not automatically turn a source firmware's explicit `SupportedTrains` list into a broad wildcard. Firmware families with similar names can still differ in hardware, updater behavior or component layout.

### Keep peripheral firmware opt-in

BOSE/amplifier and other external-device updates should remain separate and target-specific. Historical Porsche AIO packages deliberately excluded BOSE from the normal update path and kept a separate BOSE variant.

### Rebuild every integrity value touched by a modification

Historical AIO examples show that changing an image can require:

- `FileSize`
- `CheckSum`
- numbered `CheckSumN` block hashes
- tool/reference hashes
- `FinalScriptChecksum`
- other component-specific metadata

Do not assume that changing a few bytes only requires changing one top-level checksum.

### Do not ignore RCC/hash errors

Legacy issue reports include RCC/hash failures and recovery by restoring the original RCC payload. Treat an integrity mismatch as a build/package problem to resolve before retrying, not as an error to skip.

### CarPlay / Android Auto can also depend on vehicle USB coding/hardware

Older VW cases were resolved by correcting the 5F USB configuration; CarPlay can additionally require the appropriate USB hub/port hardware. A successful AIO install therefore does not by itself prove that the vehicle-side USB configuration is suitable.

## AIO execution structure

The template intentionally separates the SWDL-facing entry point from the editable post-install sequence:

```text
metainfo2
  -> common/tools/0/default/finalScript.sh
       -> common/tools/finalScriptSequence.sh
            -> backup
            -> generic actions
            -> optional target-specific actions
            -> FEC / coding / other post-install work
```

`finalScript.sh` is the small referenced entry point. `finalScriptSequence.sh` contains the high-level orchestration.

The generic script also disables `Swdlautorun.txt` after use by renaming it to `_Swdlautorun.txt`, preventing an accidental immediate update loop.

## Building a package

A safe development workflow is:

1. Start from the exact original firmware for the intended target.
2. Preserve a pristine copy and a recovery path.
3. Add/replace only the required payloads.
4. Rebuild `common/tools/0/default/hashes.txt` with the helper.
5. Generate size/hash snippets for every changed referenced file/image.
6. Build and review `metainfo2.txt` manually.
7. Compare every metainfo change against the original firmware.
8. Keep `SupportedTrains`, peripheral updates and target-specific coding conservative.
9. Test on known hardware before claiming wider compatibility.

The template deliberately does **not** automate the final metainfo/signature/compatibility decisions.
