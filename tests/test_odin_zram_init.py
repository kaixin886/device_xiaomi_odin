#!/usr/bin/env python3
"""Static checks for the independent Scheme A odin 16 GiB ZRAM setup."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEVICE_MK = (ROOT / "device.mk").read_text()
FSTAB = (ROOT / "rootdir/etc/fstab.qcom").read_text()
INIT = (ROOT / "rootdir/etc/init.target.rc").read_text()

expected_properties = {
    "mmd.zram.enabled": "true",
    "mmd.zram.size": "17179869184",
    "mmd.zram.comp_algorithm": "lz4k",
}
for name, value in expected_properties.items():
    pattern = rf"(?m)^\s*{re.escape(name)}={re.escape(value)}(?:\s+\\)?\s*$"
    assert re.search(pattern, DEVICE_MK), f"missing {name}={value} in device.mk"

zram_entries = [
    line.split()
    for line in FSTAB.splitlines()
    if re.match(r"^\s*/dev/block/zram0\s+", line)
]
assert zram_entries == [[
    "/dev/block/zram0", "none", "swap", "defaults", "zramsize=17179869184"
]], f"unexpected ZRAM fstab entries: {zram_entries!r}"

blocks = re.split(r"(?m)(?=^on )", INIT)
matching_actions = [
    block for block in blocks if block.startswith("on property:mmd.enabled_aconfig=*")
]
assert len(matching_actions) == 1, "expected exactly one MMD AConfig property action"
assert re.search(
    r"(?m)^\s+swapon_all /vendor/etc/fstab\.qcom\s*$", matching_actions[0]
), "AConfig action must call swapon_all on the vendor fstab"

all_swapon_calls = []
for path in (ROOT / "rootdir").rglob("*.rc"):
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        if re.match(r"^\s*swapon_all\b", line):
            all_swapon_calls.append((path.relative_to(ROOT).as_posix(), line_no, line.strip()))
assert len(all_swapon_calls) == 1, f"unexpected additional swapon_all calls: {all_swapon_calls!r}"

print("odin Scheme A ZRAM init static checks passed")
