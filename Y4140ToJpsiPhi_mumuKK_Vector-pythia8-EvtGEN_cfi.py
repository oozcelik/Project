import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(True),
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(0.0),
    filterEfficiency = cms.untracked.double(1.),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
	    list_forced_decays = cms.vstring('myY4140'),
	    operates_on_particles = cms.vint32(20443),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded = cms.vstring(
            """ 
################################################################################
#
Alias      myY4140      chi_c1   ## chi_c1 for vector particle assumption.
Particle   myY4140      4.140 0.092
ChargeConj myY4140      myY4140
#
Alias      myJpsi J/psi
ChargeConj myJpsi myJpsi
#
Alias      myPhi  phi
ChargeConj myPhi  myPhi
#
Decay myY4140
1.000      myJpsi myPhi PHSP;
Enddecay
#
Decay myJpsi
1.000      mu+    mu-   PHOTOS VLL;
Enddecay
#
Decay myPhi
1.000      K+    K-   VSS;
Enddecay
#
End"""
        )
    
     ),
        parameterSets = cms.vstring('EvtGen130')
  ),
     PythiaParameters = cms.PSet(pythia8CommonSettingsBlock,
                                 pythia8CUEP8M1SettingsBlock,
                                 processParameters = cms.vstring(
					                  'Charmonium:states(3PJ) = 20443', # generating only Chi_c1 particle
							  'Charmonium:O(3PJ)[3P0(1)] = 0.05', # The color-singlet long-distance matrix elements
							  'Charmonium:O(3PJ)[3S1(8)] = 0.0031', # The color-singlet long-distance matrix elements
							  'Charmonium:gg2ccbar(3PJ)[3PJ(1)]g = on', 
							  'Charmonium:qg2ccbar(3PJ)[3PJ(1)]q = on', 
							  'Charmonium:qqbar2ccbar(3PJ)[3PJ(1)]g = on', 
							  'Charmonium:gg2ccbar(3PJ)[3S1(8)]g = on', 
							  'Charmonium:qg2ccbar(3PJ)[3S1(8)]q = on', 
							  'Charmonium:qqbar2ccbar(3PJ)[3S1(8)]g = on',
							  'StringFlav:mesonCL1S1J1 = 3.00000', #the relative pseudovector production ratio (L=1,S=1,J=1) - here is max.  
							  'ParticleDecays:allowPhotonRadiation = on', 
							  '20443:m0 = 4.140',
							  '20443:mWidth = 0.092',
							  '20443:mMin = 4.116',
							  '20443:mMax = 5.886',
							  '20443:onMode = off',
							  ),
                                 parameterSets = cms.vstring('pythia8CommonSettings',
                                                             'pythia8CUEP8M1Settings',
                                                             'processParameters',
                                                             )
                                  )
 )
                         
###########
# Filters #
###########
                         
yfilter = cms.EDFilter(
    "PythiaFilter", 
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(20443) ## Chi_c1 as Y4140
    )

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*3),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(20443),
    DaughterIDs     = cms.untracked.vint32(443, 333),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999.,  9999.)
    )                       
                         
jpsifilter = cms.EDFilter(
        "PythiaDauVFilter",
	verbose         = cms.untracked.int32(4*1), 
	NumberDaughters = cms.untracked.int32(2), 
	MotherID        = cms.untracked.int32(20443),  
	ParticleID      = cms.untracked.int32(443),  
        DaughterIDs     = cms.untracked.vint32(13, -13),
	MinPt           = cms.untracked.vdouble(0.5, 0.5), 
	MinEta          = cms.untracked.vdouble(-2.5, -2.5), 
	MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )
 
phifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(20443),
    ParticleID      = cms.untracked.int32(333),
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(0.5, 0.5),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta          = cms.untracked.vdouble(2.5,  2.5)
    )
                         
ProductionFilterSequence = cms.Sequence(generator
                                        *yfilter
                                        *decayfilter
                                        *jpsifilter
                                        *phifilter
                                        )                       
                         
