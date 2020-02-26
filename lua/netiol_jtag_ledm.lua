local class = require 'pl.class'
local NetiolJtagLedm = class()


function NetiolJtagLedm:_init(tLog)
  self.tLog = tLog

  self.luaftdi = require 'luaftdi'
  self.pl = require'pl.import_into'()

  local openocd = require 'luaopenocd'
  self.tOpenOCD = openocd.luaopenocd()
end



function NetiolJtagLedm:setLeds(strTemplateFile, strLocation, usCfg, usValue0, usValue1)
  local tLog = self.tLog
  local tOpenOCD = self.tOpenOCD

  local strScriptTemplate, strError = self.pl.utils.readfile(strTemplateFile, false)
  if strScriptTemplate==nil then
    tLog.error('Failed to read from "%s": %s', strTemplateFile, tostring(strError))
    error('Failed to read.')
  end

  -- Replace the data fields in the form %XYZ%.
  local atReplace = {
    FTDI_LOCATION = strLocation,
    LEDM_CFG = usCfg,
    LEDM_VALUE0 = usValue0,
    LEDM_VALUE1 = usValue1
  }
  local strScript = string.gsub(strScriptTemplate, '%%([%w_]+)%%', atReplace)

  tLog.debug('Initialize OpenOCD.')
  tOpenOCD:initialize()

  local strResult
  local iResult = tOpenOCD:run(strScript)
  if iResult~=0 then
    error('Failed to execute the script.')
  else
    strResult = tOpenOCD:get_result()
    tLog.info('Script result: %s', strResult)
    if strResult=='0' then
      fOK = true
    else
      tLog.error('The script result is not "0".')
      error('Failed to run the LED TCL script.')
    end
  end

  tLog.debug('Uninitialize OpenOCD.')
  tOpenOCD:uninit()
end



function NetiolJtagLedm:setAllJtagAdapterToHiZ(astrLocations, usJtagAdapterVID, usJtagAdapterPID)
  local luaftdi = self.luaftdi
  local tLog = self.tLog

  local uiSwitched = 0
  local tContext = luaftdi.Context()
  local tList = tContext:usb_get_all()
  if tList==nil then
    error('Failed to get all USB devices.')
  end
  for tListEntry in tList:iter() do
    local usVID = tListEntry:get_vid()
    local usPID = tListEntry:get_pid()
    if usVID==usJtagAdapterVID and usPID==usJtagAdapterPID then
      local tPorts = tListEntry:get_port_numbers()
      -- Skip root devices (which have no ports).
      if #tPorts~=0 then
        -- Combine the bus and all ports to the location.
        local auiPorts = {}
        for _, uiPort in ipairs(tPorts) do
          table.insert(auiPorts, math.floor(uiPort))
        end
        local strLocation = string.format('%d:', tListEntry:get_bus_number()) .. table.concat(tPorts, ',')
        -- Is the location part of the table astrLocations?
        local fFound = false
        for _, strLocationItem in ipairs(astrLocations) do
          if strLocationItem==strLocation then
            fFound = true
            break
          end
        end
        if fFound==true then
          tLog.debug('Switch all pins of JTAG adapter %s to hi-Z.', strLocation)

          -- Set all pins to hi-Z.
          local tContextA = luaftdi.Context()
          local tResult, strError = tContextA:usb_open_dev(tListEntry)
          assert(tResult, strError)
          local strCmd = string.char(luaftdi.SET_BITS_LOW, 0x00, 0x00, luaftdi.SET_BITS_HIGH, 0x00, 0x00, luaftdi.SEND_IMMEDIATE)
          tContextA:write_data(strCmd)
          tContextA:usb_close()

          uiSwitched = uiSwitched + 1
        end
      end
    end
  end

  -- Were all JTAG adapter swiched to hi-Z?
  if uiSwitched~=#astrLocations then
    error('Not all JTAG adapter switched to hi-Z.')
  end
end


return NetiolJtagLedm
