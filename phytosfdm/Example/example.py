#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib as mpl

from phytosfdm.EnvForcing.envforcing import ExtractEnvFor
from phytosfdm.SizeModels.sizemodels import SM

__version__ = "1.0.0b"


def environemntalforcing(lat, lon, rbb):
    tos = time.time()
    print '\nComputation Time of Environmental Forcing'
    # Extract environmental forcing using the class ExtractEnvFor in the module envforcing
    MLD = ExtractEnvFor(lat, lon, rbb, 'mld')
    tos1 = time.time()
    print '    MLD=%4.3f sec' % (tos1-tos)
    PAR = ExtractEnvFor(lat, lon, rbb, 'par')
    tos2 = time.time()
    print '    PAR=%4.3f sec' % (tos2-tos1)
    SST = ExtractEnvFor(lat, lon, rbb, 'sst')
    tos3 = time.time()
    print '    SST=%4.3f sec' % (tos3-tos2)
    N0X = ExtractEnvFor(lat, lon, rbb, 'n0x')
    tos4 = time.time()
    print '    NOX=%4.3f sec' % (tos4-tos3)
    
    nt = np.arange(0., 365., 1.0)
    
    # Figure NO.1
    f1, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex='col', sharey='row')
    # MLD
    ax1.plot(nt, MLD.dailyinterp(nt), c='black', lw=3)
    ax1.set_ylabel('MLD (m)', multialignment='center', fontsize=12)
    ax1.set_xlim(0, 365)
    ax1.invert_yaxis()
    # PAR
    ax2.plot(nt, PAR.dailyinterp(nt), c='black', lw=3)
    ax2.set_ylabel('PAR \n' '(Ein / m^2 / d^1)', multialignment='center', fontsize=12)
    # SST
    ax3.plot(nt, SST.dailyinterp(nt), c='black', lw=3)
    ax3.set_ylabel('SST \n' '(degrees C)', multialignment='center', fontsize=12)
    # N0
    ax4.plot(nt, N0X.dailyinterp(nt), c='black', lw=3)
    ax4.set_ylabel('N0 \n' '(mmol N / m^3)', multialignment='center', fontsize=12)
    ax4.set_xlabel('Time (days)', fontsize=14)


def modelscomparison(lat, lon, rbb):
    tos = time.time()
    print '\nComputation Time of Size Models'
    # Calculation of Size Models
    SM_Full = SM(lat, lon, rbb, 'FullModel')
    tos1 = time.time()
    print '    Full=%4.3f sec' % (tos1-tos)
    Mtypes = SM_Full.outvariables[:, 3:]
    Ptot = np.sum(Mtypes, 1)
    sizerange = SM_Full.Params['sizerange']
    Lmean = np.sum(Mtypes*sizerange, 1)/Ptot
    Lvar = np.sum(Mtypes*sizerange**2, 1)/Ptot - Lmean**2
    SM_VUnsust = SM(lat, lon, rbb, 'UnsustVar')
    tos2 = time.time()
    print '    Unsustained Variance=%4.3f sec' % (tos2-tos1)
    SM_FixVar = SM(lat, lon, rbb, 'FixVar')
    tos3 = time.time()
    print '    Fixed Variance=%4.3f sec' % (tos3-tos2)
    SM_TraitDif = SM(lat, lon, rbb, 'TraitDif')
    tos4 = time.time()
    print '    Trait Diffusion=%4.3f sec' % (tos4-tos3)
    SM_Imm = SM(lat, lon, rbb, 'Imm')
    tos5 = time.time()
    print '    Immigration=%4.3f sec' % (tos5-tos4)
    
    nt = np.arange(0., 365., 1.0)
    runtime = SM_VUnsust.Params['timeyears']
    
    colors = ['#00C90D', '#01939A', 'black', 'grey', '#E2680B']
    alphas = [1., 0.8, 0.6, 0.4]
    lws = [1, 2.5, 4, 5.5]
    orangescmap = mpl.cm.Oranges(np.linspace(0, 1, SM_Full.Params['NoMtype']))

    # artist for legends
    ImmArtist = plt.Line2D((0, 1), (0, 0), c=colors[0], alpha=alphas[0], lw=lws[0])
    TdfArtist = plt.Line2D((0, 1), (0, 0), c=colors[1], alpha=alphas[1], lw=lws[1])
    FxvArtist = plt.Line2D((0, 1), (0, 0), c=colors[2], alpha=alphas[2], lw=lws[2])
    UnsVArtist = plt.Line2D((0, 1), (0, 0), c=colors[3], alpha=alphas[3], lw=lws[3])
    FullArtist = plt.Line2D((0, 1), (0, 0), c=colors[4], alpha=alphas[1], lw=lws[0])
    
    # Figure NO.2
    f2, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex='col', sharey='row')
    # N
    ax1.plot(SM_Full.timedays/365., SM_Full.outvariables[:, 0], c=colors[4], lw=lws[0], alpha=alphas[0])
    ax1.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 0], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax1.set_ylabel('Nutrients \n' '(mmol N / m^3)', multialignment='center', fontsize=10)
    ax1.set_ylim(0, 12)
    ax1.tick_params('y', labelsize=10)
    # P
    ax2.plot(SM_Full.timedays/365., Ptot, c=colors[4], lw=lws[0], alpha=alphas[0])
    ax2.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 3], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax2.set_ylabel('Phytoplankton \n' '(mmol N / m^3)', multialignment='center', fontsize=9)
    ax2.tick_params('y', labelsize=10)
    # Z
    ax3.plot(SM_Full.timedays/365., SM_Full.outvariables[:, 1], c=colors[4], lw=lws[0], alpha=alphas[0])
    ax3.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 1], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax3.set_ylabel('Zooplankton \n' '(mmol N / m^3)', multialignment='center', fontsize=9)
    ax3.tick_params('y', labelsize=10)
    # D
    ax4.plot(SM_Full.timedays/365., SM_Full.outvariables[:, 2], c=colors[4], lw=lws[0], alpha=alphas[0])
    ax4.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 2], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax4.set_ylabel('Detritus \n' '(mmol N / m^3)', multialignment='center', fontsize=9)
    ax4.tick_params('y', labelsize=10)
    ax4.set_xlabel('Time (years)', fontsize=14)
    # Legend
    f2.legend([FullArtist, UnsVArtist], ['Full Model', 'Unsustained Variance'], ncol=2, prop={'size': 10}, loc='upper center')
    
    # Figure NO.3
    f3, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='col')
    # P
    ax1.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 3], c=colors[3], alpha=alphas[3], lw=lws[3])
    for i in range(SM_Full.Params['NoMtype']):
        ax1.plot(SM_Full.timedays/365., SM_Full.outvariables[:, 3+i], c=orangescmap[i])
    ax1.set_ylabel('Phytoplankton \n' '(mmol N / m^3)', multialignment='center', fontsize=12)
    ax1.tick_params('y', labelsize=12)
    ax1.set_ylim(0, 9)
    # S
    ax2.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 4], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax2.plot(SM_Full.timedays/365., Lmean, c=colors[4], lw=lws[0], alpha=alphas[0])
    ax2.set_ylabel('Mean Size \n' '(Ln microm ESD)', multialignment='center', fontsize=12)
    ax2.set_ylim(0, 4)
    ax2.set_yticks([0, 1, 2, 3, 4])
    ax2.tick_params('y', labelsize=12)
    # V
    ax3.plot(SM_VUnsust.timedays/365., SM_VUnsust.outvariables[:, 5], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax3.plot(SM_Full.timedays/365., Lvar, c=colors[4], lw=lws[0], alpha=alphas[0])
    ax3.set_ylabel('Size Variance \n' '([Ln microm ESD]^2)', multialignment='center', fontsize=12)
    ax3.set_xlabel(r'Time (years)', fontsize=12)
    ax3.tick_params('both', labelsize=12)
    # Legend
    f3.legend([FullArtist, UnsVArtist], ['Full Model', 'Unsustained Variance'], ncol=2, prop={'size': 10}, loc='upper center')

    # Figure NO.4
    f4, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex='col')
    # N
    ax1.plot(nt, SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 0], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax1.plot(nt, SM_FixVar.outvariables[365*(runtime-1):365*runtime, 0], c=colors[2], alpha=alphas[2], lw=lws[2])
    ax1.plot(nt, SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 0], c=colors[1], alpha=alphas[1], lw=lws[1])
    ax1.plot(nt, SM_Imm.outvariables[365*(runtime-1):365*runtime, 0], c=colors[0], alpha=alphas[0], lw=lws[0])
    ax1.set_ylabel('Nutrients \n' '(mmol N / m^3)', multialignment='center', fontsize=10)
    ax1.set_ylim(0, 12)
    ax1.tick_params('y', labelsize=10)
    ax1.set_xlim(0, 365)
    # P
    ax2.plot(nt, SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 3], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax2.plot(nt, SM_FixVar.outvariables[365*(runtime-1):365*runtime, 3], c=colors[2], alpha=alphas[2], lw=lws[2])
    ax2.plot(nt, SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 3], c=colors[1], alpha=alphas[1], lw=lws[1])
    ax2.plot(nt, SM_Imm.outvariables[365*(runtime-1):365*runtime, 3], c=colors[0], alpha=alphas[0], lw=lws[0])
    ax2.set_ylabel('Phytoplankton \n' '(mmol N / m^3)', multialignment='center', fontsize=10)
    ax2.tick_params('y', labelsize=10)
    # Z
    ax3.plot(nt, SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 1], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax3.plot(nt, SM_FixVar.outvariables[365*(runtime-1):365*runtime, 1], c=colors[2], alpha=alphas[2], lw=lws[2])
    ax3.plot(nt, SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 1], c=colors[1], alpha=alphas[1], lw=lws[1])
    ax3.plot(nt, SM_Imm.outvariables[365*(runtime-1):365*runtime, 1], c=colors[0], alpha=alphas[0], lw=lws[0])
    ax3.set_ylabel('Zooplankton \n' '(mmol N / m^3)', multialignment='center', fontsize=10)
    ax3.tick_params('y', labelsize=10)
    # D
    ax4.plot(nt, SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 2], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax4.plot(nt, SM_FixVar.outvariables[365*(runtime-1):365*runtime, 2], c=colors[2], alpha=alphas[2], lw=lws[2])
    ax4.plot(nt, SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 2], c=colors[1], alpha=alphas[1], lw=lws[1])
    ax4.plot(nt, SM_Imm.outvariables[365*(runtime-1):365*runtime, 2], c=colors[0], alpha=alphas[0], lw=lws[0])
    ax4.set_ylabel('Detritus \n' '(mmol N / m^3)', multialignment='center', fontsize=10)
    ax4.tick_params('y', labelsize=10)
    ax4.set_xlabel(r'Time (days)', fontsize=14)
    f4.legend([ImmArtist, TdfArtist, FxvArtist, UnsVArtist], ['Immigration', 'Trait Diffusion', 'Fixed Variance', 'Unsustained Variance'], ncol=4, prop={'size': 10}, loc='upper center')
    
    # Figure NO.5
    f5, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='col')
    # P
    ax1.plot(nt, SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 3], c=colors[3], alpha=alphas[3], lw=lws[3])
    ax1.plot(nt, SM_FixVar.outvariables[365*(runtime-1):365*runtime, 3], c=colors[2], alpha=alphas[2], lw=lws[2])
    ax1.plot(nt, SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 3], c=colors[1], alpha=alphas[1], lw=lws[1])
    ax1.plot(nt, SM_Imm.outvariables[365*(runtime-1):365*runtime, 3], c=colors[0], alpha=alphas[0], lw=lws[0])
    ax1.set_ylabel('Phytoplankton \n' '(mmol N / m^3)', multialignment='center', fontsize=12)
    ax1.tick_params('y', labelsize=12)
    ax1.set_xlim(0, 365)
    # S
    ax2.plot(nt, (SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 4]), c=colors[3], alpha=alphas[3], lw=lws[3])
    ax2.plot(nt, (SM_FixVar.outvariables[365*(runtime-1):365*runtime, 4]), c=colors[2], alpha=alphas[2], lw=lws[2])
    ax2.plot(nt, (SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 4]), c=colors[1], alpha=alphas[1], lw=lws[1])
    ax2.plot(nt, (SM_Imm.outvariables[365*(runtime-1):365*runtime, 4]), c=colors[0], alpha=alphas[0], lw=lws[0])
    ax2.set_ylabel('Mean Size \n' '(Ln microm ESD)', multialignment='center', fontsize=12)
    ax2.set_ylim(0, 4)
    ax2.set_yticks([0, 1, 2, 3, 4])
    ax2.tick_params('y', labelsize=12)
    # V
    ax3.plot(nt, (SM_VUnsust.outvariables[365*(runtime-1):365*runtime, 5]), c=colors[3], alpha=alphas[3], lw=lws[3])
    ax3.plot(nt, (SM_FixVar.outvariables[365*(runtime-1):365*runtime, 5]), c=colors[2], alpha=alphas[2], lw=lws[2])
    ax3.plot(nt, (SM_TraitDif.outvariables[365*(runtime-1):365*runtime, 5]), c=colors[1], alpha=alphas[1], lw=lws[1])
    ax3.plot(nt, (SM_Imm.outvariables[365*(runtime-1):365*runtime, 5]), c=colors[0], alpha=alphas[0], lw=lws[0])
    ax3.set_ylabel('Size Variance \n' '([Ln microm ESD]^2)', multialignment='center', fontsize=12)
    ax3.set_xlabel(r'Time (days)', fontsize=12)
    ax3.tick_params('both', labelsize=12)
    ax3.set_ylim(0, 0.8)
    # Legend
    f5.legend([ImmArtist, TdfArtist, FxvArtist, UnsVArtist], ['Immigration', 'Trait Diffusion', 'Fixed Variance', 'Unsustained Variance'], ncol=4, prop={'size': 10}, loc='upper center')

                                                                                                                                                    
def main():
    
    print 'PhytoSFDM version:%s, Copyright (C) 2015 Esteban Acevedo-Trejos' % __version__
    print 'PhytoSFDM comes with ABSOLUTELY NO WARRANTY; for details see LICENSE.'
    print 'This is a free software, and you are welcome to redistributed it'
    print 'under certain conditions; see LICENSE for details.'
    
    # Geographical coordinates of modelled region.
    Latitude = 47.5  # 90 to -90 degrees, North positive
    Longitude = 344.5  # 0 to 360 degrees
    RangeBoundingBox = 2.  # In degrees
    
    print '\nSize Models calculated at test location: %.2f°N %.2f°W' % (Latitude, Longitude-360)

    environemntalforcing(Latitude, Longitude, RangeBoundingBox)
    
    modelscomparison(Latitude, Longitude, RangeBoundingBox)
    
    plt.show()

