import os
import logging
from osdk import args, builder, const, cmds, shell

logger = logging.getLogger(__name__)

def kvmAvailable() -> bool:
    if os.path.exists("/dev/kvm") and os.access("/dev/kvm", os.R_OK):
        return True
    return False


def installLimineEfi(efiBootDir: str) -> None:
    limine = shell.wget(
        "https://raw.githubusercontent.com/limine-bootloader/limine/v4.x-branch-binary/BOOTX64.EFI"
    )

    shell.cp(limine, os.path.join(efiBootDir, "BOOTX64.EFI"))


def installLimineLegacy(bootDir: str) -> None:
    XORRISO = [
        "xorriso", "-as", "mkisofs", "-b", "limine-cd.bin", "-no-emul-boot",
        "-boot-load-size", "4", "-boot-info-table", bootDir, "-o", os.path.join(const.CACHE_DIR, "barebones.iso")
    ]

    files = [
        "limine.sys",
        "limine-cd.bin",
        "limine-deploy.c",
        "limine-hdd.h"
    ]

    for file in files:
        limine = shell.wget(
            f"https://raw.githubusercontent.com/limine-bootloader/limine/v4.x-branch-binary/{file}"
        )

        if file not in ["limine-deploy.c", "limine-hdd.h"]:
            shell.cp(limine, os.path.join(bootDir, file))
        else:
            shell.cp(limine, os.path.join(const.CACHE_DIR, file))

    shell.exec(*XORRISO)
    shell.exec(*["cc", "-o", os.path.join(const.CACHE_DIR, "limine-deploy"), os.path.join(const.CACHE_DIR, "limine-deploy.c")])
    shell.exec(*[os.path.join(const.CACHE_DIR, "limine-deploy"), os.path.join(const.CACHE_DIR, "barebones.iso")])

def bootCmd(args: args.Args) -> None:
    legacy = "legacy" in args.opts

    imageDir = shell.mkdir(".osdk/images/barebones")
    bootDir = shell.mkdir(os.path.join(imageDir, "boot"))

    kernel = builder.build('kernel', 'kernel-x86_64')

    shell.cp(kernel.outfile(), os.path.join(bootDir, "kernel.elf"))
    shell.cp(os.path.join(const.META_DIR, "config", "limine.cfg"), bootDir)

    qemu = [
        "qemu-system-x86_64",
        '-no-reboot',
        '-no-shutdown',
        "-m", "4G",
        "-smp", "4",
        "-serial", "mon:stdio"
    ]

    if not legacy:
        logger.info("Using UEFI")
        efiBootDir = shell.mkdir(os.path.join(imageDir, "EFI", "BOOT"))
        ovmf = shell.wget("https://retrage.github.io/edk2-nightly/bin/RELEASEX64_OVMF.fd")

        installLimineEfi(efiBootDir)

        qemu += [
            "-bios", ovmf,
            "-drive", f"file=fat:rw:{imageDir},media=disk,format=raw",
        ]

    else:
        logger.info("Using legacy BIOS")
        installLimineLegacy(imageDir)
        qemu += [ 
            "-cdrom", os.path.join(const.CACHE_DIR, "barebones.iso")
        ]

    if kvmAvailable():
        qemu += ["-enable-kvm", "-cpu", "host"]

    shell.exec(*qemu)

cmds.append(cmds.Cmd('B', 'boot', 'Boot the kernel', bootCmd))