/*
 * i2c-lcd.h
 *
 *  Created on: Dec 22, 2022
 *      Author: acer
 */
#ifndef INC_LCD_H_
#define INC_LCD_H_

#include "stm32f1xx_hal.h"
#include "dht20.h"

void lcd_init ();   // initialize lcd

void lcd_send_cmd (char cmd);  // send command to the lcd

void lcd_send_data (char data);  // send data to the lcd

void lcd_send_string (char *str);  // send string to the lcd

void lcd_clear_display ();	//clear display lcd

void lcd_goto_XY (int row, int col); //set proper location on screen

void lcd_greeting ();

void lcd_show_value();
#endif /* INC_DHT20_H_ */
