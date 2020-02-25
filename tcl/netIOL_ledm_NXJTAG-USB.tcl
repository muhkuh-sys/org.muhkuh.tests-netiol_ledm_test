proc read_data32 {addr} {
  set value(0) 0
  mem2array value 32 $addr 1
  return $value(0)
}

proc probe {} {
  global SC_CFG_RESULT
  set SC_CFG_RESULT 0
  set RESULT -1

  # Setup the interface.
echo {hi 1}
  adapter_khz 500
echo {hi 6}
  interface ftdi
echo {hi 2}
  ftdi_location %FTDI_LOCATION%
echo {hi 3}
  transport select jtag
echo {hi 4}
  ftdi_device_desc "NXJTAG-USB"
echo {hi 5}
  ftdi_vid_pid 0x1939 0x0023

echo {hi 7}
  ftdi_layout_init 0x0308 0x030b
  ftdi_layout_signal nTRST -data 0x0100 -oe 0x0100
  ftdi_layout_signal nSRST -data 0x0200 -oe 0x0200

  # Expect a netIOL scan chain.
  jtag newtap netIOL cpu -expected-id 0x101026ad -irlen 4 -ircapture 0x1 -irmask 0xf
  jtag configure netIOL.cpu -event setup { global SC_CFG_RESULT ; echo {Yay - setup netIOL} ; set SC_CFG_RESULT {OK} }

  # TODO: what to do here?
  #reset_config trst_and_srst

  # Try to initialize the JTAG layer.
  if {[ catch {jtag init} ]==0 } {
    if { $SC_CFG_RESULT=={OK} } {
      target create netIOL.cpu hinetiol -endian little -chain-position netIOL.cpu
      netIOL.cpu configure -event reset-init { halt }

      init

      # Try to stop the CPU.
      halt

      # Download the code.
      load_image ledm.bin 0x8000 bin

      # Set the LED values.
      mwh 0x4000 %LEDM_CFG%
      mwh 0x4002 %LEDM_VALUE0%
      mwh 0x4004 %LEDM_VALUE1%

      # Run the code.
      # The "resume" command throws an error as the code disables the JTAG
      # function on the netIOL pins. They are used as LEDM pins.
      reg pc 0x808c
      catch {resume}

      set RESULT 0
    }
  }

  return $RESULT
}

probe
