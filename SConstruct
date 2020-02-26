# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
#   Copyright (C) 2018 by Christoph Thelen                                #
#   doc_bacardi@users.sourceforge.net                                     #
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#   This program is distributed in the hope that it will be useful,       #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#   GNU General Public License for more details.                          #
#                                                                         #
#   You should have received a copy of the GNU General Public License     #
#   along with this program; if not, write to the                         #
#   Free Software Foundation, Inc.,                                       #
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
#-------------------------------------------------------------------------#

import os


#----------------------------------------------------------------------------
#
# Set up the Muhkuh Build System.
#
SConscript('mbs/SConscript')
Import('atEnv')

# Create a build environment for the RISCV based netX chips.
env_riscv = atEnv.DEFAULT.CreateEnvironment(['gcc-riscv-none-embed-7.2', 'asciidoc'])
env_riscv.CreateCompilerEnv('NETIOL', ['arch=rv32im', 'abi=ilp32'], ['arch=rv32imc', 'abi=ilp32'])

tEnvNetIOL = atEnv.NETIOL

tEnvNetIOL.Replace(LIBS = ['c'])
tEnvNetIOL.Append(LINKFLAGS = ['-melf32lriscv'])
tEnvNetIOL.Append(CFLAGS = ['-ggdb'])
tEnvNetIOL.Replace(OBJSUFFIX = '.o')

import niol_image
niol_image.ApplyToEnv(tEnvNetIOL)


#----------------------------------------------------------------------------
# This is the list of sources for the ROM code.
sources = """
    src/main.c
    src/vectors.S
"""

#----------------------------------------------------------------------------
#
# Build the project.
#

# The list of include folders.
astrIncludePaths = ['src', '#platform/src']

tEnv = tEnvNetIOL.Clone()
tEnv.Append(CPPPATH = astrIncludePaths)
tEnv.Replace(LDFILE = 'src/netiol.ld')
tSrc = tEnv.SetBuildPath('targets', 'src', sources)
tElf = tEnv.Elf('targets/ledm.elf', tSrc)

# Dump the complete ELF.
tTxt = tEnv.ObjDump('targets/ledm.txt', tElf, OBJDUMP_FLAGS=['--disassemble', '--source', '--all-headers', '--wide'])

#-----------------------------------------------------------------------------
#
# Create a NIOL image from the ELF.
#
tBin = tEnv.ObjCopy('targets/ledm.bin', tElf)
tNiol01 = tEnv.NiolImage('targets/ledm.niol', tElf)

# ---------------------------------------------------------------------------
#
# Build an archive.
#
strGroup = 'org.muhkuh.tests'
strModule = 'netiol_ledm_test'

# Split the group by dots.
aGroup = strGroup.split('.')
# Build the path for all artifacts.
strModulePath = 'targets/jonchki/repository/%s/%s/%s' % ('/'.join(aGroup), strModule, PROJECT_VERSION)

strArtifact = 'netiol_ledm_test'

tArcList = atEnv.DEFAULT.ArchiveList('zip')

#tArcList.AddFiles('doc/',
#    doc)

tArcList.AddFiles('netx/',
    tNiol01
)

tArcList.AddFiles('lua/',
    'lua/netiol_jtag_ledm.lua'
}

tArcList.AddFiles('tcl/',
    'tcl/netIOL_ledm_NXJTAG-4000-USB.tcl',
    'tcl/netIOL_ledm_NXJTAG-USB.tcl'
)

tArcList.AddFiles('',
    'installer/%s-%s/install.lua' % (strGroup, strModule))


strBasePath = os.path.join(strModulePath, '%s-%s' % (strArtifact, PROJECT_VERSION))
tArtifact = atEnv.DEFAULT.Archive('%s.zip' % strBasePath, None, ARCHIVE_CONTENTS = tArcList)
tArtifactHash = atEnv.DEFAULT.Hash('%s.hash' % tArtifact[0].get_path(), tArtifact[0].get_path(), HASH_ALGORITHM='md5,sha1,sha224,sha256,sha384,sha512', HASH_TEMPLATE='${ID_UC}:${HASH}\n')
tConfiguration = atEnv.DEFAULT.Version('%s.xml' % strBasePath, 'installer/%s-%s/%s.xml' % (strGroup, strModule, strArtifact))
tConfigurationHash = atEnv.DEFAULT.Hash('%s.hash' % tConfiguration[0].get_path(), tConfiguration[0].get_path(), HASH_ALGORITHM='md5,sha1,sha224,sha256,sha384,sha512', HASH_TEMPLATE='${ID_UC}:${HASH}\n')
tPom = atEnv.DEFAULT.ArtifactVersion('%s.pom' % strBasePath, 'installer/%s-%s/%s.pom' % (strGroup, strModule, strArtifact))
