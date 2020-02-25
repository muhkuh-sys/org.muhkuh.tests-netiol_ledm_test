import array
import elf_support
import os
import string
import subprocess
import tempfile
import SCons


__ausCrc12 = [
    0x0000, 0x0d31, 0x0753, 0x0a62, 0x0ea6, 0x0397, 0x09f5, 0x04c4,
    0x007d, 0x0d4c, 0x072e, 0x0a1f, 0x0edb, 0x03ea, 0x0988, 0x04b9,
    0x00fa, 0x0dcb, 0x07a9, 0x0a98, 0x0e5c, 0x036d, 0x090f, 0x043e,
    0x0087, 0x0db6, 0x07d4, 0x0ae5, 0x0e21, 0x0310, 0x0972, 0x0443,
    0x01f4, 0x0cc5, 0x06a7, 0x0b96, 0x0f52, 0x0263, 0x0801, 0x0530,
    0x0189, 0x0cb8, 0x06da, 0x0beb, 0x0f2f, 0x021e, 0x087c, 0x054d,
    0x010e, 0x0c3f, 0x065d, 0x0b6c, 0x0fa8, 0x0299, 0x08fb, 0x05ca,
    0x0173, 0x0c42, 0x0620, 0x0b11, 0x0fd5, 0x02e4, 0x0886, 0x05b7,
    0x03e8, 0x0ed9, 0x04bb, 0x098a, 0x0d4e, 0x007f, 0x0a1d, 0x072c,
    0x0395, 0x0ea4, 0x04c6, 0x09f7, 0x0d33, 0x0002, 0x0a60, 0x0751,
    0x0312, 0x0e23, 0x0441, 0x0970, 0x0db4, 0x0085, 0x0ae7, 0x07d6,
    0x036f, 0x0e5e, 0x043c, 0x090d, 0x0dc9, 0x00f8, 0x0a9a, 0x07ab,
    0x021c, 0x0f2d, 0x054f, 0x087e, 0x0cba, 0x018b, 0x0be9, 0x06d8,
    0x0261, 0x0f50, 0x0532, 0x0803, 0x0cc7, 0x01f6, 0x0b94, 0x06a5,
    0x02e6, 0x0fd7, 0x05b5, 0x0884, 0x0c40, 0x0171, 0x0b13, 0x0622,
    0x029b, 0x0faa, 0x05c8, 0x08f9, 0x0c3d, 0x010c, 0x0b6e, 0x065f,
    0x07d0, 0x0ae1, 0x0083, 0x0db2, 0x0976, 0x0447, 0x0e25, 0x0314,
    0x07ad, 0x0a9c, 0x00fe, 0x0dcf, 0x090b, 0x043a, 0x0e58, 0x0369,
    0x072a, 0x0a1b, 0x0079, 0x0d48, 0x098c, 0x04bd, 0x0edf, 0x03ee,
    0x0757, 0x0a66, 0x0004, 0x0d35, 0x09f1, 0x04c0, 0x0ea2, 0x0393,
    0x0624, 0x0b15, 0x0177, 0x0c46, 0x0882, 0x05b3, 0x0fd1, 0x02e0,
    0x0659, 0x0b68, 0x010a, 0x0c3b, 0x08ff, 0x05ce, 0x0fac, 0x029d,
    0x06de, 0x0bef, 0x018d, 0x0cbc, 0x0878, 0x0549, 0x0f2b, 0x021a,
    0x06a3, 0x0b92, 0x01f0, 0x0cc1, 0x0805, 0x0534, 0x0f56, 0x0267,
    0x0438, 0x0909, 0x036b, 0x0e5a, 0x0a9e, 0x07af, 0x0dcd, 0x00fc,
    0x0445, 0x0974, 0x0316, 0x0e27, 0x0ae3, 0x07d2, 0x0db0, 0x0081,
    0x04c2, 0x09f3, 0x0391, 0x0ea0, 0x0a64, 0x0755, 0x0d37, 0x0006,
    0x04bf, 0x098e, 0x03ec, 0x0edd, 0x0a19, 0x0728, 0x0d4a, 0x007b,
    0x05cc, 0x08fd, 0x029f, 0x0fae, 0x0b6a, 0x065b, 0x0c39, 0x0108,
    0x05b1, 0x0880, 0x02e2, 0x0fd3, 0x0b17, 0x0626, 0x0c44, 0x0175,
    0x0536, 0x0807, 0x0265, 0x0f54, 0x0b90, 0x06a1, 0x0cc3, 0x01f2,
    0x054b, 0x087a, 0x0218, 0x0f29, 0x0bed, 0x06dc, 0x0cbe, 0x018f
]

__PRAM_SIZE_IN_BYTES = 0x6000
__DRAM_SIZE_IN_BYTES = 0x3000


def __crc12(strData):
    usCrc = 0x0000
    for strByte in strData:
        ucByte = ord(strByte)

        uiIndex = (usCrc >> 4) ^ ucByte
        usCrc = ((usCrc << 8) & 0x0fff) ^ __ausCrc12[uiIndex]

    return usCrc


def __get_data_contents_elf(tEnv, strAbsFilePath, strSegments):
    strData = None
    pulLoadAddress = None

    # Get the segment names to dump. It is a comma separated string.
    strSegmentsToDump = strSegments.strip()
    astrSegmentsToDump = None
    if len(strSegmentsToDump) != 0:
        astrSegmentsToDump = [
            strSegment.strip() for strSegment in
            string.split(strSegmentsToDump, ',')
        ]

    # Extract the segments.
    atSegments = elf_support.get_segment_table(
        tEnv,
        strAbsFilePath,
        astrSegmentsToDump
    )
    # Does at least one segment exist?
    fFoundSegment = False
    for strSegment in astrSegmentsToDump:
        for atAttr in atSegments:
            if atAttr['name'] == strSegment:
                fFoundSegment = True
                break
    if fFoundSegment is True:
        # Get the estimated binary size from the segments.
        ulEstimatedBinSize = elf_support.get_estimated_bin_size(
            atSegments
        )
        # Do not create files larger than 64KB.
        if ulEstimatedBinSize >= 0x00010000:
            raise Exception('The resulting file seems to extend '
                            '64KBytes. Too scared to continue!')

        if ulEstimatedBinSize > 0:
            pulLoadAddress = elf_support.get_load_address(atSegments)

            # Extract the binary.
            tBinFile, strBinFileName = tempfile.mkstemp()
            os.close(tBinFile)
            astrCmd = [
                tEnv['OBJCOPY'],
                '--output-target=binary'
            ]
            if astrSegmentsToDump is not None:
                for strSegment in astrSegmentsToDump:
                    astrCmd.append('--only-section=%s' % strSegment)
            astrCmd.append(strAbsFilePath)
            astrCmd.append(strBinFileName)
            subprocess.check_call(astrCmd)

            # Get the application data.
            tBinFile = open(strBinFileName, 'rb')
            strData = tBinFile.read()
            tBinFile.close()

            # Remove the temp file.
            os.remove(strBinFileName)

    return strData, pulLoadAddress


def niol_image_action(target, source, env):
    # Get the comma separated section lists.
    strPramSections = env['NIOL_IMAGE_PRAM_SECTIONS']
    strDramSections = env['NIOL_IMAGE_DRAM_SECTIONS']
    ulSpeed = int(env['NIOL_IMAGE_SPEED_AND_FILTER'])

    # Get the absolute file name of the ELF.
    strElfFile = source[0].get_path()

    # Get the PRAM contents and the load address.
    strPramData, ulPramLoadAddress = __get_data_contents_elf(
        env,
        strElfFile,
        strPramSections
    )
    if strPramData is None:
        raise Exception(
            'The image "%s" contains no PRAM data in the sections %s.' %
            (
                strElfFile,
                strPramSections
            )
        )
    sizPramData = len(strPramData)
#    print('PRAM: %d, %x' % (sizPramData, ulPramLoadAddress))
    strDramData, ulDramLoadAddress = __get_data_contents_elf(
        env,
        strElfFile,
        strDramSections
    )
    if strDramData is None:
#        print('DRAM: None')
        sizDramData = 0
    else:
#        print('DRAM: %d, %x' % (len(strDramData), ulDramLoadAddress))
        sizDramData = len(strDramData)

    # Check the size of the PRAM data.
    if sizPramData > __PRAM_SIZE_IN_BYTES:
        raise Exception(
            'The PRAM data has 0x%04x bytes. This exceeds the allowed '
            'maximum of 0x%04x bytes.' % (
                sizPramData,
                __PRAM_SIZE_IN_BYTES
            )
        )
    # Check the size of the DRAM data.
    if sizDramData > __DRAM_SIZE_IN_BYTES:
        raise Exception(
            'The DRAM data has 0x%04x bytes. This exceeds the allowed '
            'maximum of 0x%04x bytes.' % (
                sizDramData,
                __DRAM_SIZE_IN_BYTES
            )
        )
    # Check the speed.
    if (ulSpeed < 0) or (ulSpeed > 65535):
        raise Exception(
            'The speed must be an unsigned 16 bit number, '
            'but it is %d .' % ulSpeed
        )

    # Construct the image.
    aucImage = array.array('B')
    # Add the NVM cookie.
    aucImage.extend([ord('N'), ord('I'), ord('O'), ord('L')])
    # Add the new speed.
    aucImage.append(ulSpeed & 0xff)
    aucImage.append((ulSpeed >> 8) & 0xff)
    # Add the length of the PRAM data in bytes.
    aucImage.append(sizPramData & 0xff)
    aucImage.append((sizPramData >> 8) & 0xff)
    # Add the length of the DRAM data in bytes.
    aucImage.append(sizDramData & 0xff)
    aucImage.append((sizDramData >> 8) & 0xff)

    # Get the CRC12 of the header.
    strHeaderData = aucImage.tostring()
    usHeaderCrc = __crc12(strHeaderData)

    # Add the header CRC.
    aucImage.append(usHeaderCrc & 0xff)
    aucImage.append((usHeaderCrc >> 8) & 0xff)

    # Add the PRAM data.
    aucImage.fromstring(strPramData)
    # Add the DRAM data if it exists.
    if strDramData is not None:
        aucImage.fromstring(strDramData)

    # Get the CRC12 of the image.
    strImageData = aucImage.tostring()
    usImageCrc = __crc12(strImageData)

    # Add the image CRC.
    aucImage.append(usImageCrc & 0xff)
    aucImage.append((usImageCrc >> 8) & 0xff)

    # Get the absolute path name of the output file.
    strNiolFile = target[0].get_path()
    tFile = open(strNiolFile, 'wb')
    aucImage.tofile(tFile)
    tFile.close()

    return 0


def niol_image_emitter(target, source, env):
    # Depend on the PRAM and DRAM sections.
    env.Depends(target, SCons.Node.Python.Value('NIOL_IMAGE_PRAM_SECTIONS:%s' % (str(env['NIOL_IMAGE_PRAM_SECTIONS']))))
    env.Depends(target, SCons.Node.Python.Value('NIOL_IMAGE_DRAM_SECTIONS:%s' % (str(env['NIOL_IMAGE_DRAM_SECTIONS']))))
    env.Depends(target, SCons.Node.Python.Value('NIOL_IMAGE_SPEED_AND_FILTER:%s' % (str(env['NIOL_IMAGE_SPEED_AND_FILTER']))))

    return target, source


def niol_image_string(target, source, env):
    return 'NIOL image %s' % target[0].get_path()


def ApplyToEnv(env):
    # Add the NIOL image builder.
    env['NIOL_IMAGE_PRAM_SECTIONS'] = '.code'
    env['NIOL_IMAGE_DRAM_SECTIONS'] = '.data'
    env['NIOL_IMAGE_SPEED_AND_FILTER'] = 0

    niol_image_act = SCons.Action.Action(
        niol_image_action,
        niol_image_string
    )
    niol_image_bld = SCons.Script.Builder(
        action=niol_image_act,
        emitter=niol_image_emitter,
        suffix='.xml'
    )
    env['BUILDERS']['NiolImage'] = niol_image_bld
