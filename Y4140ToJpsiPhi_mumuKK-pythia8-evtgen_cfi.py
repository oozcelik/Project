import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(0.0),
    filterEfficiency = cms.untracked.double(1.),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
	    list_forced_decays = cms.vstring('myY4140'),
	    operates_on_particles = cms.vint32(10441),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded = cms.vstring(
            """ 
################################################################################
#
Alias      myY4140      chi_c0   ## chi_c0 for scalar particle assumption.
Particle   myY4140      4.140 0.0
ChargeConj myY4140      myY4140 
#
Alias      myJpsi J/psi
ChargeConj myJpsi myJpsi
#
Alias      myPhi  phi
ChargeConj myPhi  myPhi
#
Decay myY4140
1.000      myJpsi myPhi SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;
Enddecay
#
Decay myAnti-Y4140
1.000      myJpsi myPhi SVV_HELAMP 1.0 0.0 1.0 0.0 1.0 0.0;
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
                                 processParameters = cms.vstring('SoftQCD:nonDiffractive = on',
								 '10441:m0 = 4.140',
								 '10441:mWidth = 0.092',
							         '10441:mMin = 4.116',             
								 '10441:mMax = 5.886', 
								 '10441:onMode = off',                                                                            
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
    ParticleID = cms.untracked.int32(10441) ## chi_c0 as Y4140
    )

decayfilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*3),
    NumberDaughters = cms.untracked.int32(2),
    ParticleID      = cms.untracked.int32(10441),
    DaughterIDs     = cms.untracked.vint32(443, 333),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999., -9999.),
    MaxEta          = cms.untracked.vdouble( 9999.,  9999.)
    )                       
                         
jpsifilter = cms.EDFilter(
        "PythiaDauVFilter",
	verbose         = cms.untracked.int32(4*1), 
	NumberDaughters = cms.untracked.int32(2), 
	MotherID        = cms.untracked.int32(10441),  
	ParticleID      = cms.untracked.int32(443),  
        DaughterIDs     = cms.untracked.vint32(13, -13),
	MinPt           = cms.untracked.vdouble(2.5, 2.5), 
	MinEta          = cms.untracked.vdouble(-2.5, -2.5), 
	MaxEta          = cms.untracked.vdouble( 2.5,  2.5)
    )
 
phifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(10441),
    ParticleID      = cms.untracked.int32(333),
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(-1.0, -1.0),
    MinEta          = cms.untracked.vdouble(-9999, -9999),
    MaxEta          = cms.untracked.vdouble( 9999,  9999)
    )
                         
ProductionFilterSequence = cms.Sequence(generator
                                        *yfilter
                                        *decayfilter
                                        *jpsifilter
                                        *phifilter
                                        )                       
                         
