#!/usr/bin/python
import os, sys

upnum = 24000

JES = ['JESAbsoluteStat', 'JESAbsoluteScale', 'JESAbsoluteMPFBias', 'JESFragmentation', 'JESSinglePionECAL', 'JESSinglePionHCAL', 'JESTimePtEta', 'JESRelativePtBB', 'JESRelativePtEC1', 'JESRelativePtEC2', 'JESRelativeBal', 'JESRelativeFSR', 'JESRelativeStatFSR', 'JESRelativeStatEC', 'JESPileUpDataMC', 'JESPileUpPtRef', 'JESPileUpPtBB', 'JESPileUpPtEC1', 'JESFlavorQCD']
#JESPileUpPtEC2

for s in JES:
	os.system('python plotTemplates_2comp.py %s %s %s 0.06' %(sys.argv[1],s,upnum))
