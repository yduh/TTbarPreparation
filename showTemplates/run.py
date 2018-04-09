#!/usr/bin/python
import os, sys

norm = ['pileup','lep','JER','btag','ltag','alpha','bdecay']
norm_tt = ['hdamp','isr']

JES = ['JESAbsoluteStat', 'JESAbsoluteScale', 'JESAbsoluteMPFBias', 'JESFragmentation', 'JESSinglePionECAL', 'JESSinglePionHCAL', 'JESTimePtEta', 'JESRelativePtBB', 'JESRelativePtEC1', 'JESRelativePtEC2', 'JESRelativeBal', 'JESRelativeFSR', 'JESRelativeStatFSR', 'JESRelativeStatEC', 'JESPileUpDataMC', 'JESPileUpPtRef', 'JESPileUpPtBB', 'JESPileUpPtEC1', 'JESPileUpPtEC2', 'JESFlavorQCD']
shape = ['fsr','bfrag','mt','pdf','rsfs']
shape_tt = ['mt','color']

checkonly = ['MET','tune']


for s in shape_tt:
	os.system('python plotTemplates_1comp.py %s %s' %(sys.argv[1],s))
for s in shape:
	os.system('python plotTemplates_2comp.py %s %s' %(sys.argv[1],s))

for s in norm_tt:
	os.system('python plotTemplates_1comp.py %s %s' %(sys.argv[1],s))
for s in norm:
	os.system('python plotTemplates_2comp.py %s %s' %(sys.argv[1],s))

for s in checkonly:
	os.system('python plotTemplates_2comp.py %s %s' %(sys.argv[1],s))
