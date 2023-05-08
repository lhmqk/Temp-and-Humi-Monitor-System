/*
 * uart_reading.h
 *
 *  Created on: Dec 22, 2022
 *      Author: acer
 */

#ifndef INC_UART_READING_H_
#define INC_UART_READING_H_

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "main.h"
#include "dht20.h"
#include "i2c-lcd.h"
#include "software_timer.h"
#include "scheduler.h"
#include "led_display.h"

#define MCU_VERSION "STM32F103RBT6"

#define FIRMWARE_VERSION "2.1"

#define INIT_UART 0

#define AUTO 1

#define isCAP 2

#define WAIT 3

#define isRST 4

#define OBLED_ON 5

#define OBLED_OFF 6

#define MOD_CYCLE 7

#define DELIM ":"

#define MAX_BUFFER_SIZE 30

#define MAX_CMD_SIZE 6

extern uint8_t buffer_byte;
extern uint8_t buffer[MAX_BUFFER_SIZE];
extern uint8_t index_buffer;
extern uint8_t buffer_flag;

void rst_buffer();

void cmd_parser_fsm();

void uart_control_fsm();

uint32_t msgCheckSum(char* msg, uint32_t msgLen);

void Scan_Addr();

void Mcu_info();



#endif /* INC_UART_READING_H_ */
