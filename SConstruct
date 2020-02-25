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

