#define HANDOVER_INCLUDE_MACROS
#define HANDOVER_INCLUDE_UTILITES

#include <stddef.h>
#include <handover-spec/handover.h>

HANDOVER();

#include "serial.h"

__attribute__((noreturn)) int _start(void)
{    
    serial_init();

    serial_puts("Hello, World!\n");

    for (;;);
}