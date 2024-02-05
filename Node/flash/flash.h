/*
 * flash.h
 *
 *  Created on: Jan. 15, 2024
 *      Author: eliesaliba
 */

#ifndef FLASH_H_
#define FLASH_H_

#include "sl_status.h"

void w25q16jv_init();

void w25q16jv_Busy();

sl_status_t w25q16jv_DeviceID();

sl_status_t w25q16jv_WriteEnable();

sl_status_t w25q16jv_byte_program(uint8_t *txBuffer);

sl_status_t w25q16jv_Readbyte();

sl_status_t w25q16jv_ReadStatusRegister(uint8_t *data);

sl_status_t w25q16jv_page_program();

sl_status_t w25q16jv_ReadData(uint8_t *data);

sl_status_t w25q16jv_ReadData_Page(int i);

sl_status_t w2516jv_ReadBLEData(int i, uint8_t *buf, uint8_t connection);

sl_status_t w25q16jv_SectorErase();

sl_status_t w25q16jv_ChipErase();

#endif /* FLASH_H_ */
