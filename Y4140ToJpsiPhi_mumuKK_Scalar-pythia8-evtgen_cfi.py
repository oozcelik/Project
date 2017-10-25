import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(108800000),
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
			      Alias      myY4140      chi_c0   ## chi_c1 for vector particle assumption.
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
	
	PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
             'Charmonium:states(3PJ) = 10441',
             'StringFlav:mesonSL1S1J0 = 1.0000', # Scalar production : L=1 && S=1 && J=0
	      'Charmonium:O(3PJ)[3P0(1)] = 0.05', # The color-singlet long-distance matrix elements
	      'Charmonium:O(3PJ)[3S1(8)] = 0.0031', # The color-singlet long-distance matrix elements
	      'Charmonium:gg2ccbar(3PJ)[3PJ(1)]g = on', # Colour-singlet production of 3PJ charmonium states via g g
	      'Charmonium:qg2ccbar(3PJ)[3PJ(1)]q = on',
	      'Charmonium:qqbar2ccbar(3PJ)[3PJ(1)]g = on',
	      'Charmonium:gg2ccbar(3PJ)[3S1(8)]g = on',
	      'Charmonium:qg2ccbar(3PJ)[3S1(8)]q = on',
	      'Charmonium:qqbar2ccbar(3PJ)[3S1(8)]g = on',
	      'ParticleDecays:allowPhotonRadiation = on', 
             '10441:m0 = 4.140', # Chi_c0 assigned as Y(4140) 4.5060 
             '10441:mWidth = 0.092',
             '10441:mMin = 4.116', # 4.116 = m(J/psi) + m(phi)                                                                                                       
             '10441:mMax = 5.886', # 4.568 = 4.506 +15*mWidth                                                                                                        
             '10441:onMode = off',        # turn off Y(4500) decays inherited from Chi_c0                                                                           
             ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                        'pythia8CUEP8M1Settings',
                                        'processParameters',
                                       )
    )
)


#pythia.particleData.listChangedd() #To list only the data of the particles that have been changed                                                                    

yfilter = cms.EDFilter(
    "PythiaFilter",
    MaxEta = cms.untracked.double(9999.),
    MinEta = cms.untracked.double(-9999.),
    ParticleID = cms.untracked.int32(10441) # Chi_c0 as Y particle. 
    )

# verbose threshold for "PythiaDauVFilter" are 2,5,10                                                                                                                 
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
    MinPt           = cms.untracked.vdouble(0.5, 0.5),
    MaxEta          = cms.untracked.vdouble(2.5, 2.5),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5)
    )

phifilter = cms.EDFilter(
    "PythiaDauVFilter",
    verbose         = cms.untracked.int32(4*1),
    NumberDaughters = cms.untracked.int32(2),
    MotherID        = cms.untracked.int32(10441),
    ParticleID      = cms.untracked.int32(333),
    DaughterIDs     = cms.untracked.vint32(321, -321),
    MinPt           = cms.untracked.vdouble(0.5, 0.5),
    MaxEta          = cms.untracked.vdouble(2.5, 2.5),
    MinEta          = cms.untracked.vdouble(-2.5, -2.5)
    )


ProductionFilterSequence = cms.Sequence(generator
                                        *yfilter
                                        *decayfilter
                                        *jpsifilter
                                        *phifilter
                                        )

