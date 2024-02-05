/*
 * flash.c
 *
 *  Created on: Jan. 15, 2024
 *      Author: eliesaliba
 */
#include "flash.h"
#include "spidrv.h"
#include "sl_spidrv_instances.h"
#include "printf.h"

#define spi_handle sl_spidrv_exp_handle

int j;

int q;

uint8_t busy_bit = 3;

void w25q16jv_init()
{
  w25q16jv_WriteEnable();
  w25q16jv_ChipErase();
  w25q16jv_Busy();
}


sl_status_t w25q16jv_DeviceID()
{
  Ecode_t ret_code;
  uint8_t txBuffer[5];
  uint8_t rxBuffer[5];

  txBuffer[0] = 0xAB;
  txBuffer[1] = 0xFF;
  txBuffer[2] = 0xFF;
  txBuffer[3] = 0xFF;
  txBuffer[4] = 0xFF;

  ret_code = SPIDRV_MTransferB(spi_handle, txBuffer, rxBuffer, 5);

  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }


  printf("%X\n", rxBuffer[4]);

  return SL_STATUS_OK;
}

void w25q16jv_Busy()
{
  while(busy_bit == 3){
      w25q16jv_ReadStatusRegister(&busy_bit);
      //printf("Busy\n");
  }
  busy_bit = 3;
}

sl_status_t w25q16jv_WriteEnable()
{
  uint8_t txBuffer[1];
  Ecode_t ret_code;

  txBuffer[0] = 0x06;

  ret_code = SPIDRV_MTransmitB(spi_handle, txBuffer, 1);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_ReadStatusRegister(uint8_t *data)
{
  uint8_t txBuffer[2];
  uint8_t rxBuffer[2];
  Ecode_t ret_code;

  txBuffer[0] = 0x05;
  txBuffer[1] = 0xFF;

  ret_code = SPIDRV_MTransferB(spi_handle, txBuffer, rxBuffer, 2);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    *data = 0;
    return SL_STATUS_TRANSMIT;
  }

  *data = rxBuffer[1];
  //printf("%X\n", rxBuffer[1]);

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_page_program(uint8_t* txBuffer)
{
  //uint8_t txBuffer[260];
  Ecode_t ret_code;

  //txBuffer[5] = 0x55;
  w25q16jv_WriteEnable();
  ret_code = SPIDRV_MTransmitB(spi_handle, txBuffer, 260);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }

  w25q16jv_Busy();

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_byte_program(uint8_t* txBuffer)
{
  //uint8_t txBuffer[260];
  Ecode_t ret_code;

  //txBuffer[5] = 0x55;
  w25q16jv_WriteEnable();

  printf("tx %X\n", txBuffer[0]);
  printf("tx %X\n", txBuffer[1]);
  printf("tx %X\n", txBuffer[2]);
  printf("tx %X\n", txBuffer[3]);
  printf("tx %X\n", txBuffer[4]);

  ret_code = SPIDRV_MTransmitB(spi_handle, txBuffer, 5);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }

  w25q16jv_Busy();

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_Readbyte()
{
  uint8_t txBuffer[5]; //= { 0 };
  uint8_t rxBuffer[5];
  Ecode_t ret_code;

  txBuffer[0] = 0x03;
  txBuffer[1] = 0x01;
  txBuffer[2] = 0x00;
  txBuffer[3] = 0x00;
  txBuffer[4] = 0xFF;

  ret_code = SPIDRV_MTransferB(spi_handle, txBuffer, rxBuffer, 5);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }

  printf("rx %X\n", rxBuffer[4]);

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_ReadData(uint8_t *data)
{
  uint8_t txBuffer[260]; //= { 0 };
  uint8_t rxBuffer[260];
  Ecode_t ret_code;
  /*
  txBuffer[0] = 0x03;
  txBuffer[1] = 0x00;
  txBuffer[2] = 0x00;
  txBuffer[3] = 0x02;
  txBuffer[4] = 0x00;
  txBuffer[5] = 0x00;
  txBuffer[6] = 0x00;
  txBuffer[7] = 0x00;
  txBuffer[8] = 0x00;
  txBuffer[9] = 0x00;
  txBuffer[10] = 0x00;
  txBuffer[11] = 0x00;
  */
  txBuffer[0] = 0x03;
  txBuffer[1] = 0x00;
  txBuffer[2] = 0x00;
  txBuffer[3] = 0x00;

  ret_code = SPIDRV_MTransferB(spi_handle, txBuffer, rxBuffer, 260);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    *data = 0;
    return SL_STATUS_TRANSMIT;
  }

  *data = rxBuffer[4];

  for (j=4; j<260; j+=2){
      printf("%X\n", rxBuffer[j]);
  }

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_ReadData_Page(int i)
{
  //printf("Read Data Page\n");
  uint8_t txBuffer[260]; //= { 0 };
  uint8_t rxBuffer[260];
  Ecode_t ret_code;

  txBuffer[0] = 0x03;
  txBuffer[1] = 0x00;
  txBuffer[2] = 0x00;
  txBuffer[3] = 0x00;
  //int a = 0;
  for (q=0; q<i; q++){


      ret_code = SPIDRV_MTransferB(spi_handle, txBuffer, rxBuffer, 260);
      if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
        return SL_STATUS_TRANSMIT;
      }

      for (j=4; j<260; j+=2){
          printf("%X%X \n", rxBuffer[j], rxBuffer[j+1]);
          //a+=1;
      }
      if (txBuffer[2] == 0xFF){
          txBuffer[1] += 0x01;
      }
      txBuffer[2] += 0x01;

  }

  return SL_STATUS_OK;
}

sl_status_t w2516jv_ReadBLEData(int i, uint8_t *buf, uint8_t connection) //221 for 210 regular pages
{
  uint8_t txBuffer[248]; //= { 0 }; //244 bytes
  uint8_t rxBuffer[248];
  uint32_t address = 0x00;
  Ecode_t ret_code;

  txBuffer[0] = 0x03;

  txBuffer[1] = 0x00;
  txBuffer[2] = 0x00;
  txBuffer[3] = 0x00;

  //int a = 0;

  for (q=0; q<i; q++){

      ret_code = SPIDRV_MTransferB(spi_handle, txBuffer, rxBuffer, 248);
      if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
        return SL_STATUS_TRANSMIT;
      }
      //collects data then save it to the buffer array.

      for (j=4; j<248; j +=1 ){
          buf[j-4] = rxBuffer[j];
          //printf("buf[j-4] %X\n", buf[j-4]);
      }

      mic_notify(buf, connection);

/*
      for (j=4; j<248; j+=2){
          printf("%X%X \n", rxBuffer[j], rxBuffer[j+1]);
          //a+=1;
      }

      printf("BREAK\n");
*/
      address += 0xF4;

      txBuffer[1] = (uint8_t) (address >> 16);
      txBuffer[2] = (uint8_t) (address >> 8 & 0x0000FF);
      txBuffer[3] = (uint8_t) (address & 0x0000FF);

  }

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_SectorErase()
{
  uint8_t txBuffer[4];
  Ecode_t ret_code;

  txBuffer[0] = 0x20;
  txBuffer[1] = 0x00;
  txBuffer[2] = 0x00;
  txBuffer[3] = 0x00;

  ret_code = SPIDRV_MTransmitB(spi_handle, txBuffer, 4);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }

  return SL_STATUS_OK;
}

sl_status_t w25q16jv_ChipErase()
{
  uint8_t txBuffer[1];
  Ecode_t ret_code;

  txBuffer[0] = 0x60;

  ret_code = SPIDRV_MTransmitB(spi_handle, txBuffer, 1);
  if (ret_code != ECODE_EMDRV_SPIDRV_OK) {
    return SL_STATUS_TRANSMIT;
  }

  return SL_STATUS_OK;
}


