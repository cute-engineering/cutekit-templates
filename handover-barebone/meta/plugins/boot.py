import os

from cutekit import args, builder, const, cmds, shell


def kvmAvailable() -> bool:
    if os.path.exists("/dev/kvm") and os.access("/dev/kvm", os.R_OK):
        return True
    return False


def bootCmd(args: args.Args) -> None:
    imageDir = shell.mkdir(os.path.join(const.PROJECT_CK_DIR, "images", "barebone"))
    bootDir = os.path.join(imageDir, "boot")
    efiBootDir = shell.mkdir(os.path.join(imageDir, "EFI", "BOOT"))
    ovmf = shell.wget("https://retrage.github.io/edk2-nightly/bin/RELEASEX64_OVMF.fd")

    loader = builder.build('loader', 'efi-x86_64')
    kernel = builder.build('kernel', 'kernel-x86_64')

    shell.cpTree(os.path.join(const.META_DIR, "boot"), bootDir)
    shell.cp(kernel.outfile(), os.path.join(bootDir, "kernel.elf"))
    shell.cp(loader.outfile(), os.path.join(efiBootDir, "BOOTX64.EFI"))

    qemu = [
        "qemu-system-x86_64",
        '-no-reboot',
        '-no-shutdown',
        "-m", "256M",
        "-smp", "4",
        "-serial", "mon:stdio",
        "-bios", ovmf,
        "-drive", f"file=fat:rw:{imageDir},media=disk,format=raw",
    ]

    if kvmAvailable():
        qemu += ["-enable-kvm", "-cpu", "host"]


    shell.exec(*qemu)


cmds.append(cmds.Cmd('B', 'boot', 'Boot the kernel', bootCmd))