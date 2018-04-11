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

kint = Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO"


#=====================================================================

fdata = r.TFile("./%s/%s/skim_DATA.root" %(njets,skimType))
ftt = r.TFile("./%s/%s/skim_tt_PowhegP8_%s.root" %(njets,skimType,nominal))
ft = r.TFile("./%s/%s/skim_t.root" %(njets,skimType))
fvj = r.TFile("./%s/%s/skim_VnJets.root" %(njets,skimType))

hdata = fdata.Get(kint)
htt = ftt.Get(kint)
ht = ft.Get(kint)
hvj = fvj.Get(kint)

hsum = htt.Clone()
hsum.Add(ht, 1)
hsum.Add(hvj, 1)

Tqcd = hdata.Clone()
Tqcd.Add(hsum, -1)
numdataCR = Tqcd.Integral()
Tqcdtemp = Tqcd.Clone()
errdataCR = Tqcdtemp.Rebin2D(Tqcdtemp.GetNbinsX(),Tqcdtemp.GetNbinsY())
errdataCR = errdataCR.GetBinError(1, 1)
Tqcd.Scale(1/Tqcd.Integral())

hTbck = r.TH2D(Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO", Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO", Tqcd.GetNbinsX(), 0, 2000, Tqcd.GetNbinsY(), -6, 6)
hTbckX = r.TH1D(Varargs().DefaultVarDict['_Mtt'].saveName+"_RECO", Varargs().DefaultVarDict['_Mtt'].saveName+"_RECO", Tqcd.GetNbinsX(), 0, 2000)
hTbckY = r.TH1D(Varargs().DefaultVarDict['_delY'].saveName+"_RECO", Varargs().DefaultVarDict['_delY'].saveName+"_RECO", Tqcd.GetNbinsY(), -6, 6)

for i in range(Tqcd.GetNbinsX()):
	for j in range(Tqcd.GetNbinsY()):
		if(Tqcd.GetBinContent(i+1, j+1) >= 0):
			hTbck.SetBinContent(i+1, j+1, Tqcd.GetBinContent(i+1, j+1))
		else:
			hTbck.SetBinContent(i+1, j+1, 0)

hTbckX = hTbck.ProjectionX()
hTbckY = hTbck.ProjectionY()

#=====================================================================
fqcdSR = r.TFile("./%s/skimroot/skim_QCD.root" %njets)
fqcdCR = r.TFile("./%s/%s/skim_QCD.root" %(njets,skimType))

numqcdSR = fqcdSR.Get(kint).Integral()
numqcdCR = fqcdCR.Get(kint).Integral()
numqcd = (numqcdSR/numqcdCR)*numdataCR
numqcd = (numqcdSR/numqcdCR)*numdataCR
norm = numqcd
errqcdSR = fqcdSR.Get(kint).Rebin2D(fqcdSR.Get(kint).GetNbinsX(), fqcdSR.Get(kint).GetNbinsY())
errqcdSR = errqcdSR.GetBinError(1, 1)
errqcdCR = fqcdCR.Get(kint).Rebin2D(fqcdCR.Get(kint).GetNbinsX(), fqcdCR.Get(kint).GetNbinsY())
errqcdCR = errqcdCR.GetBinError(1, 1)
print "Norm =", norm, "+-", sqrt((errqcdSR/numqcdSR)**2+(errqcdCR/numqcdCR)**2+(errdataCR/numdataCR)**2)*norm
print "MC SR yields =", numqcdSR, "+-", errqcdSR
print "MC CR yields =", numqcdCR, "+-", errqcdCR
print "data CR yields =", numdataCR, "+-", errdataCR

hTbck.Scale(norm)
hTbckX.Scale(norm)
hTbckY.Scale(norm)

outfile = r.TFile("./%s/%s/skim_Tqcd.root" %(njets,skimType), "RECREATE")
hTbck.Write()
#hTbckX.Write()
#hTbckY.Write()

#hTbck.SetName(Varargs().DefaultVarDict['_Mtt_delY'].saveName+"_RECO")
hTbck.SetName('qcd')
#hTbckX.SetName(Varargs().DefaultVarDict['_Mtt'].saveName+"_RECO")
#hTbckY.SetName(Varargs().DefaultVarDict['_delY'].saveName+"_RECO")

outfile.Close()
#=====================================================================


