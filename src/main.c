#include "netx_io_areas.h"


static unsigned short ausLedmValues[3] __attribute__ ((section (".parameter")));


void start(void) __attribute__ ((noreturn));
void start(void)
{
	HOSTDEF(ptAsicCtrlArea);
	HOSTDEF(ptPadCtrlArea);
	HOSTDEF(ptLedmArea);
	unsigned short usConfig;
	unsigned short usValue;


	/* Setup the IO multiplexer. */
	usValue  =  0U << SRT_NIOL_asic_ctrl_io_config0_sel_uart_d;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config0_sel_spi;
	usValue |=  1U << SRT_NIOL_asic_ctrl_io_config0_sel_hispi;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config0_sel_jtag;
	usValue |= PW_VAL_NIOL_asic_ctrl_io_config0;
	ptAsicCtrlArea->aulAsic_ctrl_io_config[0] = usValue;

	usValue  =  0U << SRT_NIOL_asic_ctrl_io_config1_sel_sync_out_p;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config1_sel_sync_in_p;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config1_sel_irq_ext_p;
	usValue |= PW_VAL_NIOL_asic_ctrl_io_config1;
	ptAsicCtrlArea->aulAsic_ctrl_io_config[1] = usValue;

	usValue  =  7U << SRT_NIOL_asic_ctrl_io_config2_sel_led_c;
	usValue |= 15U << SRT_NIOL_asic_ctrl_io_config2_sel_led_r;
	usValue |= PW_VAL_NIOL_asic_ctrl_io_config2;
	ptAsicCtrlArea->aulAsic_ctrl_io_config[2] = usValue;

	usValue  =  0U << SRT_NIOL_asic_ctrl_io_config3_sel_adc_gpz;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config3_sel_adc_gpo0;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config3_sel_adc_gpo1;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config3_sel_adc_gpo2;
	usValue |=  0U << SRT_NIOL_asic_ctrl_io_config3_sel_adc_gpo3;
	usValue |= PW_VAL_NIOL_asic_ctrl_io_config3;
	ptAsicCtrlArea->aulAsic_ctrl_io_config[3] = usValue;

	/* Set the PAD control register. */
	usValue  = PW_VAL_NIOL_pad_ctrl_led_r0;
	usValue |= MSK_NIOL_pad_ctrl_led_r0_ie;
	ptPadCtrlArea->aulPad_ctrl_led_r[0] = usValue;

	usValue  = PW_VAL_NIOL_pad_ctrl_led_r1;
	usValue |= MSK_NIOL_pad_ctrl_led_r1_ie;
	ptPadCtrlArea->aulPad_ctrl_led_r[1] = usValue;

	usValue  = PW_VAL_NIOL_pad_ctrl_led_r2;
	usValue |= MSK_NIOL_pad_ctrl_led_r2_ie;
	ptPadCtrlArea->aulPad_ctrl_led_r[2] = usValue;

	usValue  = PW_VAL_NIOL_pad_ctrl_led_r3;
	usValue |= MSK_NIOL_pad_ctrl_led_r3_ie;
	ptPadCtrlArea->aulPad_ctrl_led_r[3] = usValue;

	usValue  = PW_VAL_NIOL_pad_ctrl_led_c0;
	usValue |= MSK_NIOL_pad_ctrl_led_c0_ie;
	ptPadCtrlArea->aulPad_ctrl_led_c[0] = usValue;

	usValue  = PW_VAL_NIOL_pad_ctrl_led_c1;
	usValue |= MSK_NIOL_pad_ctrl_led_c1_ie;
	ptPadCtrlArea->aulPad_ctrl_led_c[1] = usValue;

	usValue  = PW_VAL_NIOL_pad_ctrl_led_c2;
	usValue |= MSK_NIOL_pad_ctrl_led_c2_ie;
	ptPadCtrlArea->aulPad_ctrl_led_c[2] = usValue;


	/* Disable the LED matrix. */
	ptLedmArea->ulLedm_cfg = DFLT_VAL_NIOL_ledm_cfg;

	/* Set the configuration, but do not enable the module yet. */
	usConfig = ausLedmValues[0];
	usValue = usConfig & (unsigned short)((~MSK_NIOL_ledm_cfg_en)&0xffffU);
//	usValue  =  1U << SRT_NIOL_ledm_cfg_precharge_en;
//	usValue |=  1U << SRT_NIOL_ledm_cfg_column_adaptive;
//	usValue |=  1U << SRT_NIOL_ledm_cfg_bipolar;
//	usValue |=  5U << SRT_NIOL_ledm_cfg_column_last;
//	usValue |=  0U << SRT_NIOL_ledm_cfg_en;
	ptLedmArea->ulLedm_cfg = usValue;

	/* Set the prescaler. */
	ptLedmArea->ulLedm_prescaler = 1;

	/* Set the LED matrix time 0. */
	ptLedmArea->aulLedm_t[0] =  100;
	/* Set the LED matrix time 1. */
	ptLedmArea->aulLedm_t[1] =   25;
	/* Set the LED matrix time 2. */
	ptLedmArea->aulLedm_t[2] =   25;
	/* Set the LED matrix time 3. */
	ptLedmArea->aulLedm_t[3] = 4000;

	/* Enable the LEDM module. */
	usValue = usConfig | MSK_NIOL_ledm_cfg_en;
//	usValue  =  1U << SRT_NIOL_ledm_cfg_precharge_en;
//	usValue |=  1U << SRT_NIOL_ledm_cfg_column_adaptive;
//	usValue |=  1U << SRT_NIOL_ledm_cfg_bipolar;
//	usValue |=  5U << SRT_NIOL_ledm_cfg_column_last;
//	usValue |=  1U << SRT_NIOL_ledm_cfg_en;
	ptLedmArea->ulLedm_cfg = usValue;

	/* Set all LEDs. */
	ptLedmArea->ulLedm_led15_0_rld = ausLedmValues[1];
	ptLedmArea->ulLedm_led23_16_rld = ausLedmValues[2];

	/* stop */
	while(1) {};
}
