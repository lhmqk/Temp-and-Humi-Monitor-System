/*
 * led_display.c
 *
 *  Created on: Mar 24, 2023
 *      Author: acer
 */

#include "led_display.h"

void turnLedOn(){
	HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, RESET);
}

void turnLedOff(){
	HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, SET);
}

void toggleLed(){
	HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}

void turnOBLedOn(){
	HAL_GPIO_WritePin(OB_LED_GPIO_Port, OB_LED_Pin, SET);
}

void turnOBLedOff(){
	HAL_GPIO_WritePin(OB_LED_GPIO_Port, OB_LED_Pin, RESET);
}

void toggleOBLed(){
	HAL_GPIO_TogglePin(OB_LED_GPIO_Port, OB_LED_Pin);
}
