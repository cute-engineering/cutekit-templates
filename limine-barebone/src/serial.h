#pragma once

#include <stdint.h>

void serial_init(void);
void serial_putc(char c);
void serial_puts(const char *s);