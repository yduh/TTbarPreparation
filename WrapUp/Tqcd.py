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

#=====================================================================
def getQCDshape(skimType, strnominal, info):
	fdata = r.TFile("./%s/%s/skim_DATA.root" %(njets,skimType))
	ftt = r.TFile("./%s/%s/skim_tt_PowhegP8_%s.root" %(njets,skimType,strnominal))
	ft = r.TFile("./%s/%s/skim_t.root" %(njets,skimType))
	fvj = r.TFile("./%s/%s/skim_VnJets.root" %(njets,skimType))
	fww = r.TFile("./%s/%s/skim_WW.root" %(njets,skimType))
	fwz = r.TFile("./%s/%s/skim_WZ.root" %(njets,skimType))

	kint = info.saveName+'_RECO'
	hdata = fdata.Get(kint)
	htt = ftt.Get(kint)
	ht = ft.Get(kint)
	hvj = fvj.Get(kint)
	hww = fww.Get(kint)
	hwz = fwz.Get(kint)

	hsum = htt.Clone()
	hsum.Add(ht, 1)
	hsum.Add(hvj, 1)
	hsum.Add(hww, 1)
	hsum.Add(hwz, 1)

	Tqcd = hdata.Clone()
	Tqcd.Add(hsum, -1)
	numdata = Tqcd.Integral()
	Tqcdtemp = Tqcd.Clone()
	errdata = Tqcdtemp.Rebin2D(Tqcdtemp.GetNbinsX(),Tqcdtemp.GetNbinsY()) if info.getHistDim() == 2 else Tqcdtemp.Rebin(Tqcdtemp.GetNbinsX())
	errdata = errdata.GetBinError(1, 1) if info.getHistDim() == 2 else errdata.GetBinError(1)
	Tqcd.Scale(1/Tqcd.Integral())

	hTqcd = r.TH2D(kint, kint, Tqcd.GetNbinsX(), Tqcd.GetXaxis().GetBinLowEdge(1), Tqcd.GetXaxis().GetBinUpEdge(Tqcd.GetNbinsX()), Tqcd.GetNbinsY(), Tqcd.GetYaxis().GetBinLowEdge(1), Tqcd.GetYaxis().GetBinUpEdge(Tqcd.GetNbinsY())) if info.getHistDim() == 2 else r.TH1D(kint, kint, Tqcd.GetNbinsX(), Tqcd.GetXaxis().GetBinLowEdge(1), Tqcd.GetXaxis().GetBinUpEdge(Tqcd.GetNbinsX()))

	if info.getHistDim() == 2:
		for i in range(Tqcd.GetNbinsX()):
			for j in range(Tqcd.GetNbinsY()):
				if(Tqcd.GetBinContent(i+1, j+1) >= 0):
					hTqcd.SetBinContent(i+1, j+1, Tqcd.GetBinContent(i+1, j+1))
					hTqcd.SetBinError(i+1, j+1, Tqcd.GetBinError(i+1, j+1))
				else:
					hTqcd.SetBinContent(i+1, j+1, 0)
					hTqcd.SetBinError(i+1, j+1, Tqcd.GetBinError(i+1, j+1))
	else:
		for i in range(Tqcd.GetNbinsX()):
			if(Tqcd.GetBinContent(i+1) >=0):
				hTqcd.SetBinContent(i+1, Tqcd.GetBinContent(i+1))
				hTqcd.SetBinError(i+1, Tqcd.GetBinError(i+1))
			else:
				hTqcd.SetBinContent(i+1, 0)
				hTqcd.SetBinError(i+1, Tqcd.GetBinError(i+1))

	return numdata, errdata, hTqcd, [fdata,ftt,ft,fvj,fww,fwz]

#=====================================================================
def getQCDnorm(skimType, numdataSB, errdata, info):
	fqcdSR = r.TFile("./%s/skimroot/skim_QCD.root" %njets)
	fqcdSB = r.TFile("./%s/%s/skim_QCD.root" %(njets,skimType))

	#kint = info.saveName+'_RECO'
	kint = Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO"
	numqcdSR = fqcdSR.Get(kint).Integral()
	numqcdSB = fqcdSB.Get(kint).Integral()
	numqcd = (numqcdSR/numqcdSB)*numdataSB
	norm = numqcd

	if info.getHistDim() == 2:
		errqcdSR = fqcdSR.Get(kint).Rebin2D(fqcdSR.Get(kint).GetNbinsX(), fqcdSR.Get(kint).GetNbinsY())
		errqcdSR = errqcdSR.GetBinError(1, 1)
		errqcdSB = fqcdSB.Get(kint).Rebin2D(fqcdSB.Get(kint).GetNbinsX(), fqcdSB.Get(kint).GetNbinsY())
		errqcdSB = errqcdSB.GetBinError(1, 1)
		print "This is the case of csv region", skimType, ":"
		print "Norm =", norm, "+-", sqrt((errqcdSR/numqcdSR)**2+(errqcdSB/numqcdSB)**2+(errdata/numdataSB)**2)*norm
		print "MC Signal Region yields =", numqcdSR, "+-", errqcdSR
		print "MC Sideband      yields =", numqcdSB, "+-", errqcdSB
		print "data Sideband    yields =", numdataSB, "+-", errdata
		print "====================================================="
		print "norm uncert in Combine", sqrt((errqcdSR/numqcdSR)**2+(errqcdSB/numqcdSB)**2+(errdata/numdataSB)**2)

	return norm

#=====================================================================

#kint = Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO"
varargs = Varargs().DefaultVarDict
varargs.update(Varargs().AddVarDict)

for histname, info in varargs.iteritems():
	print info.saveName
	numdataCR, errdataCR, hTqcdCR, _ = getQCDshape('skimrootSB','noEW',info) #The shape of csv[0-0.6]
	normCR = getQCDnorm('skimrootSB', numdataCR, errdataCR, info) #The shape/normalization of csv[0-0.6]

	if nominal == 'noEW':
		hTqcdCR.Scale(normCR)
		print "Using norm =", normCR

		outfile.cd()
		hTqcdCR.Write()
		hTqcdCR.SetName('qcd')
	else:
		numdata, errdata, hTqcd, flist = getQCDshape(skimType,nominal,info) #The shape of any feed-in csv region
		hTqcd.Scale(normCR) #Shpae is defined by any feed-in csv region, but the normalization is applied with which csv[0-0.6]
		print "Using norm =", normCR

		outfile.cd()
		hTqcd.Write()
		hTqcd.SetName('qcd')

		#The print out helps you to compare btw up/down templates norm uncertainties
		norm = getQCDnorm(skimType, numdata, errdata, kint) #The normalization of any feed-in csv regsion
		#hTqcd.Scale(norm) #Shpae is defined by any feed-in csv region, but the normalization is applied with which csv[0-0.6]

outfile.Close()


