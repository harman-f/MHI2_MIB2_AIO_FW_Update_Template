#!/usr/bin/env python3
"""
Rebuild and verify the simple SHA-1 reference hashes used by the MHI2 AIO
template without generating or modifying metainfo2.txt.

Commands:

  tool-dir
      Rebuild/check an existing hashes.txt from the files referenced by it.
      The manifest controls scope; unrelated/placeholder files are not added.

  file
      Print FileName/FileSize/CheckSum lines for one reference file.
      With --chunk-size, emit CheckSum, CheckSum1, ... for manual metainfo
      editing.

This tool deliberately never edits metainfo2.txt.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
from typing import Iterable


HEADER = """###########################################################################
#
# This is the hash file to secure the tooling of the common section
#
###########################################################################
"""

ENTRY_RE = re.compile(
    r'FileName\s*=\s*"(?P<name>[^"]+)"\s*'
    r'FileSize\s*=\s*"(?P<size>\d+)"\s*'
    r'CheckSum\s*=\s*"(?P<sha1>[0-9A-Fa-f]{40})"',
    re.MULTILINE,
)


def sha1_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def sha1_file(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def iter_chunks(path: Path, chunk_size: int) -> Iterable[bytes]:
    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk_size)
            if not block:
                break
            yield block


def quote_name(name: str) -> str:
    return name.replace("\\", "\\\\").replace('"', '\\"')


def parse_tool_hashes(text: str) -> list[tuple[str, int, str]]:
    result: list[tuple[str, int, str]] = []
    for match in ENTRY_RE.finditer(text):
        result.append(
            (
                match.group("name"),
                int(match.group("size")),
                match.group("sha1").lower(),
            )
        )
    return result


def current_reference_entries(
    directory: Path, manifest_text: str
) -> list[tuple[str, int, str]]:
    declared = parse_tool_hashes(manifest_text)
    if not declared:
        raise ValueError(
            "manifest contains no FileName/FileSize/CheckSum entries; "
            "refusing to invent manifest scope"
        )

    rebuilt: list[tuple[str, int, str]] = []
    for name, _old_size, _old_hash in declared:
        path = directory / name
        if not path.is_file():
            raise ValueError(f"referenced file is missing: {path}")
        rebuilt.append((name, path.stat().st_size, sha1_file(path)))
    return rebuilt


def render_tool_hashes(entries: list[tuple[str, int, str]]) -> str:
    lines = [HEADER.rstrip(), ""]
    for name, size, digest in entries:
        lines.extend(
            [
                f'FileName = "{quote_name(name)}"',
                f'FileSize = "{size}"',
                f'CheckSum = "{digest}"',
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def entry_map(
    entries: list[tuple[str, int, str]]
) -> dict[str, tuple[int, str]]:
    return {name: (size, digest) for name, size, digest in entries}


def command_tool_dir(args: argparse.Namespace) -> int:
    directory = Path(args.directory).resolve()
    output = directory / args.output

    if not directory.is_dir():
        print(f"ERROR: not a directory: {directory}", file=sys.stderr)
        return 2
    if not output.is_file():
        print(
            f"ERROR: manifest not found: {output}; "
            "create the intended entries manually first",
            file=sys.stderr,
        )
        return 2

    manifest_text = output.read_text(encoding="utf-8")

    try:
        declared = parse_tool_hashes(manifest_text)
        rebuilt = current_reference_entries(directory, manifest_text)
        rendered = render_tool_hashes(rebuilt)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.check:
        old = entry_map(declared)
        new = entry_map(rebuilt)

        if old == new:
            print(
                f"OK: {output} matches {len(rebuilt)} referenced file(s)"
            )
            return 0

        print(f"STALE: {output}", file=sys.stderr)
        for name, _size, _digest in rebuilt:
            if old.get(name) != new.get(name):
                print(
                    f"  {name}: {old.get(name)} -> {new.get(name)}",
                    file=sys.stderr,
                )
        return 1

    if args.stdout:
        sys.stdout.write(rendered)
        return 0

    output.write_bytes(rendered.encode("utf-8"))
    print(f"WROTE: {output}")
    for name, size, digest in rebuilt:
        print(f"  {name}: size={size} sha1={digest}")
    return 0


def command_file(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()

    if not path.is_file():
        print(f"ERROR: not a file: {path}", file=sys.stderr)
        return 2

    display_name = args.file_name or path.name

    print(f'FileName = "{quote_name(display_name)}"')
    print(f'FileSize = "{path.stat().st_size}"')

    if args.chunk_size is None:
        print(f'CheckSum = "{sha1_file(path)}"')
        return 0

    if args.chunk_size <= 0:
        print("ERROR: --chunk-size must be > 0", file=sys.stderr)
        return 2

    count = 0
    for index, block in enumerate(iter_chunks(path, args.chunk_size)):
        key = "CheckSum" if index == 0 else f"CheckSum{index}"
        print(f'{key} = "{sha1_bytes(block)}"')
        count += 1

    if count == 0:
        print(f'CheckSum = "{sha1_file(path)}"')

    print(
        f"# chunk_size={args.chunk_size} bytes; chunks={count}; "
        f"whole_file_sha1={sha1_file(path)}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild/verify AIO reference hashes and print manual metainfo "
            "hash snippets. This tool never edits metainfo2.txt."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    tool_dir = sub.add_parser(
        "tool-dir",
        help=(
            "rebuild or verify an existing hashes.txt from exactly the "
            "files referenced by that manifest"
        ),
    )
    tool_dir.add_argument(
        "directory",
        nargs="?",
        default="common/tools/0/default",
        help="reference directory (default: common/tools/0/default)",
    )
    tool_dir.add_argument(
        "--output",
        default="hashes.txt",
        help="manifest filename in the directory (default: hashes.txt)",
    )
    mode = tool_dir.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="verify the existing manifest without writing",
    )
    mode.add_argument(
        "--stdout",
        action="store_true",
        help="print the regenerated manifest instead of writing it",
    )
    tool_dir.set_defaults(func=command_tool_dir)

    file_cmd = sub.add_parser(
        "file",
        help="print FileSize/CheckSum lines for manual metainfo editing",
    )
    file_cmd.add_argument("path", help="reference file to hash")
    file_cmd.add_argument(
        "--file-name",
        help="override the FileName value printed in the snippet",
    )
    file_cmd.add_argument(
        "--chunk-size",
        type=int,
        help=(
            "emit CheckSum, CheckSum1, ... per chunk. For example 524288 "
            "means 512 KiB. Only use a chunk size verified for the target "
            "firmware/component."
        ),
    )
    file_cmd.set_defaults(func=command_file)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
