# AIO host-side hash helper

`rebuild_reference_hashes.py` is intentionally small. It helps with the repetitive integrity metadata around an AIO package but **does not generate or edit `metainfo2.txt`**.

It uses SHA-1 because that is what the historical MHI2 SWDL metadata and `hashes.txt` files use.

## 1. Rebuild `common/tools/0/default/hashes.txt`

From the repository root:

```bash
python3 tools/rebuild_reference_hashes.py tool-dir
```

The command reads the existing `hashes.txt` first and recalculates **exactly the files already referenced by that manifest**. Placeholder or unrelated files in the directory are not added automatically. It writes fresh:

```text
FileName = "..."
FileSize = "..."
CheckSum = "..."
```

entries.

Verify without modifying anything:

```bash
python3 tools/rebuild_reference_hashes.py tool-dir --check
```

Preview the regenerated manifest:

```bash
python3 tools/rebuild_reference_hashes.py tool-dir --stdout
```

The files are hashed as **raw bytes**. Line endings therefore matter, exactly as they do to the unit. The repository pins the historical `ExceptionList.txt` checkout to CRLF because its published `695`-byte / SHA-1 reference depends on CRLF, while `finalScript.sh` is pinned to LF.

## 2. Generate a manual metainfo reference block

For any single file:

```bash
python3 tools/rebuild_reference_hashes.py file common/tools/0/default/finalScript.sh
```

Example output:

```ini
FileName = "finalScript.sh"
FileSize = "369"
CheckSum = "6d738d9ab611f314c46180b92189a2ce33a02e59"
```

This is output only. The script never opens or modifies `metainfo2.txt`.

For the final script, copy the generated SHA-1 to the appropriate `FinalScriptChecksum` field by hand.

## 3. Chunked checksums for large firmware files

Some MHI2 metainfo application sections contain:

```text
CheckSum
CheckSum1
CheckSum2
...
```

The POG11 AIO/reference comparison shows these are block-oriented: a small change to `ifs-root.ifs` changes only a subset of the numbered hashes.

The helper can generate chunk hashes when the correct chunk size is already known for the target component:

```bash
python3 tools/rebuild_reference_hashes.py file RCC/ifs-root/31/default/ifs-root.ifs --chunk-size 524288
```

That prints:

```ini
FileName = "ifs-root.ifs"
FileSize = "..."
CheckSum = "..."
CheckSum1 = "..."
...
```

plus a comment containing the whole-file SHA-1.

**Important:** `524288` (512 KiB) is a useful research/test value for known MHI2 examples, but this tool does not claim that every component or firmware family uses that chunk size. Verify the target format before copying the generated block into a metainfo.

## What this tool deliberately does not do

If you intentionally add a new secured reference file, add its `FileName`/placeholder entry to `hashes.txt` first and then run the rebuild. The helper refuses to invent the manifest scope.

It does not:

- create a complete `metainfo2.txt`;
- merge or normalize duplicate `[common]` sections;
- create or bypass signatures;
- calculate a `MetafileChecksum`;
- decide `SupportedTrains`;
- decide which peripheral firmware (BOSE, amplifiers, etc.) should be flashed;
- calculate undocumented directory-level checksums automatically;
- change any firmware image.

The operator is still responsible for building and reviewing `metainfo2.txt` manually.

## Recommended workflow

1. Start from the exact original firmware for the intended target.
2. Modify only the required files/images.
3. Run `tool-dir` after changing `ExceptionList.txt`, `finalScript.sh`, or other files in the secured tools directory.
4. Use `file` for every changed referenced payload.
5. Copy the resulting size/hash values into the hand-maintained metainfo.
6. Compare the completed metainfo against the original and review every changed section.
7. Keep target/hardware compatibility narrow. Do not replace an explicit train list with a broad wildcard without independent evidence.
8. Keep peripheral device updates such as BOSE/AMP opt-in and target-specific.
9. Keep a known recovery path and backup before testing on a unit.
