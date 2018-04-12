#!/usr/bin/python
import ROOT as r
import sys
from SCALE import *
import ScaleBook
from vararg import Varargs
from math import sqrt

njets = sys.argv[1]
nominal = sys.argv[2]

skimType = 'skimrootSB' if nominal == "noEW" else 'skimrootSB_'+nominal
outfile = r.TFile("./%s/%s/skim_Tqcd.root" %(njets,skimType), "RECREATE")

kint = Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO"

#=====================================================================
def getQCDshape(skimType, strnominal):
	fdata = r.TFile("./%s/%s/skim_DATA.root" %(njets,skimType))
	ftt = r.TFile("./%s/%s/skim_tt_PowhegP8_%s.root" %(njets,skimType,strnominal))
	ft = r.TFile("./%s/%s/skim_t.root" %(njets,skimType))
	fvj = r.TFile("./%s/%s/skim_VnJets.root" %(njets,skimType))
	fww = r.TFile("./%s/%s/skim_WW.root" %(njets,skimType))
	fwz = r.TFile("./%s/%s/skim_WZ.root" %(njets,skimType))

	hdata = fdata.Get(kint)
	htt = ftt.Get(kint)
	ht = ft.Get(kint)
	hvj = fvj.Get(kint)
	hww = fww.Get(kint)
	hwz = fwz.Get(kint)

	hsum = htt.Clone()
	hsum.Add(ht, 1)
	#hsum.Add(hvj, 1)
	#hsum.Add(hww, 1)
	#hsum.Add(hwz, 1)

	Tqcd = hdata.Clone()
	Tqcd.Add(hsum, -1)
	numdata = Tqcd.Integral()
	Tqcdtemp = Tqcd.Clone()
	errdata = Tqcdtemp.Rebin2D(Tqcdtemp.GetNbinsX(),Tqcdtemp.GetNbinsY())
	errdata = errdata.GetBinError(1, 1)
	Tqcd.Scale(1/Tqcd.Integral())

	hTqcd = r.TH2D(Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO", Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO", Tqcd.GetNbinsX(), 0, 2000, Tqcd.GetNbinsY(), -6, 6)
	hTqcdX = r.TH1D(Varargs().DefaultVarDict['_Mtt'].saveName+"_RECO", Varargs().DefaultVarDict['_Mtt'].saveName+"_RECO", Tqcd.GetNbinsX(), 0, 2000)
	hTqcdY = r.TH1D(Varargs().DefaultVarDict['_delY'].saveName+"_RECO", Varargs().DefaultVarDict['_delY'].saveName+"_RECO", Tqcd.GetNbinsY(), -6, 6)

	for i in range(Tqcd.GetNbinsX()):
		for j in range(Tqcd.GetNbinsY()):
			if(Tqcd.GetBinContent(i+1, j+1) >= 0):
				hTqcd.SetBinContent(i+1, j+1, Tqcd.GetBinContent(i+1, j+1))
			else:
				hTqcd.SetBinContent(i+1, j+1, 0)

	hTqcdX = hTqcd.ProjectionX()
	hTqcdY = hTqcd.ProjectionY()

	return numdata, errdata, hTqcd, hTqcdX, hTqcdY,[fdata,ftt,ft,fvj,fww,fwz]

#=====================================================================
def getQCDnorm(skimType, numdataSB, errdata):
	fqcdSR = r.TFile("./%s/skimroot/skim_QCD.root" %njets)
	fqcdSB = r.TFile("./%s/%s/skim_QCD.root" %(njets,skimType))

	numqcdSR = fqcdSR.Get(kint).Integral()
	numqcdSB = fqcdSB.Get(kint).Integral()
	numqcd = (numqcdSR/numqcdSB)*numdataSB
	norm = numqcd
	errqcdSR = fqcdSR.Get(kint).Rebin2D(fqcdSR.Get(kint).GetNbinsX(), fqcdSR.Get(kint).GetNbinsY())
	errqcdSR = errqcdSR.GetBinError(1, 1)
	errqcdSB = fqcdSB.Get(kint).Rebin2D(fqcdSB.Get(kint).GetNbinsX(), fqcdSB.Get(kint).GetNbinsY())
	errqcdSB = errqcdSB.GetBinError(1, 1)
	print "This is the case of csv region", skimType, ":"
	print "Norm =", norm, "+-", sqrt((errqcdSR/numqcdSR)**2+(errqcdSB/numqcdSB)**2+(errdata/numdataSB)**2)*norm
	print "MC Signal Region yields =", numqcdSR, "+-", errqcdSR
	print "MC Sideband      yields =", numqcdSB, "+-", errqcdSB
	print "data Sideband    yields =", numdataSB, "+-", errdata

	return norm

#=====================================================================


numdataCR, errdataCR, hTqcdCR, hTqcdCRX, hTqcdCRY,_ = getQCDshape('skimrootSB', 'noEW') #The shape of csv[0-0.6]
normCR = getQCDnorm('skimrootSB', numdataCR, errdataCR) #The normalization of csv[0-0.6]

if nominal == 'noEW':
	hTqcdCR.Scale(normCR)
	hTqcdCRX.Scale(normCR)
	hTqcdCRY.Scale(normCR)

	outfile.cd()
	hTqcdCR.Write()
	hTqcdCR.SetName('qcd')
else:
	numdata, errdata, hTqcd, hTqcdX, hTqcdY,flist = getQCDshape(skimType, nominal) #The shape of any feed-in csv region
	hTqcd.Scale(normCR) #Shpae is defined by any feed-in csv region, but the normalization is applied with which csv[0-0.6]
	hTqcdX.Scale(normCR)
	hTqcdY.Scale(normCR)

	outfile.cd()
	hTqcd.Write()
	hTqcd.SetName('qcd')

	#The print out helps you to compare btw up/down templates norm uncertainties
	norm = getQCDnorm(skimType, numdata, errdata) #The normalization of any feed-in csv regsion
	#hTqcd.Scale(norm) #Shpae is defined by any feed-in csv region, but the normalization is applied with which csv[0-0.6]
	#hTqcdX.Scale(norm)
	#hTqcdY.Scale(norm)
	#outfile.cd()
	#hTqcd.Write()
	#hTqcd.SetName('qcd')

#for f in flist:
#	print f
outfile.Close()


