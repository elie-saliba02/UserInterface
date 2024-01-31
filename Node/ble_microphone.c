/*
 * ble_microphone.c
 *
 *  Created on: Jan. 17, 2024
 *      Author: eliesaliba
 */


#include "sl_bluetooth.h"
#include "em_pdm.h"
#include "ustimer.h"
#include "printf.h"

uint16_t data_;

int i_;

int i__;

int q_;

void mic_collect(uint8_t connection){
  uint8_t buf[244];
  sl_status_t sc;

  for (q_=0; q_<102; q_++){ //102

  for (i_ = 0 ; i_<244 ; i_+=2){
        data_ = PDM->RXDATA;
        printf("%X\n", data_);
        buf[i_]= (uint8_t) (data_ >> 8);
        buf[i_+1]= (uint8_t) (data_ & 0x00FF);
        USTIMER_Delay(18);
  }


  sc = sl_bt_gatt_server_send_notification(
    connection,
    30,
    sizeof(buf),
    buf);

    if (sc) {
      printf("Failed to send temperature measurement indication\n");
    }
  }
}
