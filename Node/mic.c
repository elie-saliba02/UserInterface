/*
 * mic.c
 *
 *  Created on: Jan. 17, 2024
 *      Author: eliesaliba
 */
#include "em_gpio.h"
#include "em_pdm.h"
#include "em_cmu.h"
#include <math.h>

#define MIC_SAMPLE_RATE            40000

void mic_init(void)
{
  PDM_Init_TypeDef pdmInit = PDM_INIT_DEFAULT;

  // Set up clocks
  CMU_ClockEnable(cmuClock_GPIO, true);
  CMU_ClockEnable(cmuClock_PDM, true);
  CMU_ClockSelectSet(cmuClock_PDMREF, cmuSelect_HFRCODPLL); // 19 MHz

  // Config GPIO and pin routing
  GPIO_PinModeSet(gpioPortA, 0, gpioModePushPull, 1);    // MIC_EN
  GPIO_PinModeSet(gpioPortD, 2, gpioModePushPull, 0);    // PDM_CLK
  GPIO_PinModeSet(gpioPortD, 3, gpioModeInput, 0);       // PDM_DATA

  GPIO_SlewrateSet(gpioPortC, 7, 7);

  GPIO->PDMROUTE.ROUTEEN = GPIO_PDM_ROUTEEN_CLKPEN;
  GPIO->PDMROUTE.CLKROUTE = (gpioPortD << _GPIO_PDM_CLKROUTE_PORT_SHIFT)
                            | (2 << _GPIO_PDM_CLKROUTE_PIN_SHIFT);
  GPIO->PDMROUTE.DAT0ROUTE = (gpioPortD << _GPIO_PDM_DAT0ROUTE_PORT_SHIFT)
                            | (3 << _GPIO_PDM_DAT0ROUTE_PIN_SHIFT);
  GPIO->PDMROUTE.DAT1ROUTE = (gpioPortC << _GPIO_PDM_DAT1ROUTE_PORT_SHIFT)
                            | (7 << _GPIO_PDM_DAT1ROUTE_PIN_SHIFT);

  // Initialize PDM registers with reset values

  PDM_Reset(PDM);

  uint8_t dsr = 72;

  uint32_t sample_rate = MIC_SAMPLE_RATE;

  // Calculate gain (shift value) based on DSR and filter order
  //uint8_t gain = 31 - (1 + (uint32_t)(log10f(pow(dsr, 5)) / log10f(2)));

  // Calculate necessary prescaler based on desired sample rate and DSR
  uint32_t clock_freq = CMU_ClockFreqGet(cmuClock_PDM);
  uint32_t prescaler_val = (clock_freq / (sample_rate * dsr)) - 1;

  // Configure PDM
  pdmInit.start = true;
  pdmInit.dsr = dsr; //73 70
  pdmInit.gain = 8;//gain;
  pdmInit.ch0ClkPolarity = pdmCh0ClkPolarityRisingEdge;  // Normal
  pdmInit.ch1ClkPolarity = pdmCh1ClkPolarityFallingEdge; // Invert
  pdmInit.enableCh0Ch1Stereo = false;
  pdmInit.fifoValidWatermark = pdmFifoValidWatermarkOne;
  pdmInit.dataFormat = pdmDataFormatRight16;
  pdmInit.numChannels = pdmNumberOfChannelsOne;
  pdmInit.filterOrder = pdmFilterOrderFifth;
  pdmInit.prescaler = prescaler_val; //46 5


  // Initialize PDM peripheral
  PDM_Init(PDM, &pdmInit);
}
