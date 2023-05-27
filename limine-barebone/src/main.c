#include <stddef.h>

#include "limine.h"
#include "serial.h"

static struct limine_bootloader_info_request bootloader_info_request = {
    .id = LIMINE_BOOTLOADER_INFO_REQUEST,
    .revision = 0
};

__attribute__((noreturn)) int _start(void)
{    
    serial_init();

    if (bootloader_info_request.response == NULL)
    {
        serial_puts("Error: Bootloader info request failed!\n");
        for (;;);
    }
    
    serial_puts("Hello, World!\nFrom: ");
    serial_puts(bootloader_info_request.response->name);
    serial_putc(' ');
    serial_puts(bootloader_info_request.response->version);
    serial_putc('\n');

    for (;;);
}