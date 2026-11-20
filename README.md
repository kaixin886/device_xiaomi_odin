Copyright &copy; 2021 The LineageOS Project

Device configuration for Xiaomi MIX 4
=========================================

The Xiaomi MIX 4 (codenamed _"odin"_) is a high-end smartphone from Xiaomi.

It was released in August 2021.

## Device specifications

Basic   | Spec Sheet
-------:|:-------------------------
CPU     | Octa-core (1x2.99 GHz Kryo 680 & 3x2.42 GHz Kryo 680 & 4x1.80 GHz Kryo 680)
Chipset | Qualcomm SM8350 Snapdragon 888+
GPU     | Adreno 660
Memory  | 8/12 GB RAM
Shipped Android Version | 11.0
Storage | 128/256/512 GB (UFS 3.1)
Battery | Non-removable Li-Po 4500 mAh
Display | 2400 x 1080 pixels, 6.67 inches (~395 ppi pixel density)
Camera  | 108MP(Primary), 13MP(Ultrawide), 8MP(Telephoto), dual LED flash, 20MP(Selfie)

## Device picture


![Xiaomi MIX 4](https://fdn2.gsmarena.com/vv/pics/xiaomi/mix-4-1.jpg "Xiaomi MIX 4")

## Scheme A: 16 GiB ZRAM through ROM init

This is the standalone ROM/device-tree option on the `integration/odin-zram-16g` branch, based on Inkypen's LineageOS 24.0 odin tree. It configures `mmd.zram.enabled=true`, `mmd.zram.size=17179869184` (bytes), and `mmd.zram.comp_algorithm=lz4k`.

The device init waits for Android 17 MMD to publish `mmd.enabled_aconfig`, then runs `swapon_all` against the vendor fstab. If the MMD AConfig flag is enabled, AOSP fs_mgr skips its fstab ZRAM setup and MMD uses the properties above. If that flag is disabled, fs_mgr applies the fstab `zramsize=17179869184` fallback. In the fallback path, LZ4K depends on the paired kernel's default compressor. See the [Android MMD configuration](https://source.android.com/docs/core/perf/mmd) and the [AOSP fs_mgr MMD integration](https://android.googlesource.com/platform/system/core.git/+/1d4dc2f4bcfc1045d0114d0d3fce278f601d208).

Disable Scene's ZRAM management before using this ROM configuration so only one component initializes ZRAM. This device-tree change is separate from the kernel-only Scheme C branch, where Scene remains responsible for the 16 GiB capacity. Scheme A requires building and flashing a ROM containing this branch; it has not yet been tested on the MIX 4, and no performance or power benefit is claimed.
