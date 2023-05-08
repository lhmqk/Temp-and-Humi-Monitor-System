/*
 * dht20.h
 *
 *  Created on: Dec 22, 2022
 *      Author: acer
 */

#ifndef INC_DHT20_H_
#define INC_DHT20_H_

#include <stdio.h>
#include <string.h>
#include "main.h"
#include "i2c-lcd.h"
#include "uart_reading.h"
#include "software_timer.h"

extern uint16_t value_x10[2];
extern char temp[20],humid[20];

void dht20_init();

void dht20_reset(uint8_t);

void dht20_read(uint16_t*);

void dht20_start();

void dht20_output();

#endif /* INC_DHT20_H_ */
