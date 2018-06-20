#!/usr/bin/python
import ROOT as r
import sys, os
from array import array
from math import sqrt
import Rebin
from binning import bins2D
from vararg import Varargs

njets = sys.argv[1]
nominal = 'noEW'
numin = 10000 #int(sys.argv[2]) #12000 #10000
FixBins = True
#printLatex = True

ADD_EXPSYS = True
ADD_THSYS = True
ADD_THSYS_ST = True
ADD_NNLOpT = True
ADD_QCDcsvSYS = True
BreakDownJES = True
#minevents = 30

writeSysExp = ['btag', 'ltag', 'JER', 'pileup', 'MET', 'lep']
#writeSysExp_vj = ['btag', 'ltag', 'lep']
writeSysTH = ['damp', 'isr', 'fsr', 'tune', 'color', 'bdecay', 'bfrag', 'mt1'] #'mt3', 'pdf', 'alpha' 'pdfsum', 'pdf1', 'pdf2' are TH1D, so needs to do hadd after
writeSysTH_t = ['bdecay', 'bfrag'] #'fsr', 'pdf', 'alpha'
#breakdownJES = ['AbsoluteStat', 'AbsoluteScale', 'AbsoluteMPFBias', 'Fragmentation', 'SinglePionECAL', 'SinglePionHCAL', 'TimePtEta', 'RelativePtBB', 'RelativePtEC1', 'RelativePtEC2', 'RelativeBal', 'RelativeFSR', 'RelativeStatFSR', 'RelativeStatEC', 'PileUpDataMC', 'PileUpPtRef', 'PileUpPtBB', 'PileUpPtEC1', 'PileUpPtEC2', 'FlavorQCD']
breakdownJES = ['AbsoluteStat', 'AbsoluteScale', 'AbsoluteMPFBias', 'Fragmentation', 'SinglePionECAL', 'SinglePionHCAL', 'TimePtEta', 'RelativePtBB', 'RelativePtEC1', 'RelativePtEC2', 'RelativeBal', 'RelativeFSR', 'RelativeStatFSR', 'RelativeStatEC', 'PileUpDataMC', 'PileUpPtRef', 'PileUpPtBB', 'PileUpPtEC1', 'FlavorQCD']

#uncUptxt = open('err/uncerUp_%s.txt' %njets)
#uncDowntxt = open('err/uncerUp_%s.txt' %njets)
#uncUp = uncUptxt.readlines()
#uncDown = uncDowntxt.readlines()
#uncer = [x.strip() for x in uncUp]
#print uncer

inpath = "/uscms/home/yiting11/nobackup/CMSSW_7_4_12_patch4/src/ttbar_preparation/WrapUp/%s/skimroot/" %njets
inpathsb = "/uscms/home/yiting11/nobackup/CMSSW_7_4_12_patch4/src/ttbar_preparation/WrapUp/%s/skimrootSB/" %njets
inpathsys = "/uscms/home/yiting11/nobackup/CMSSW_7_4_12_patch4/src/ttbar_preparation/WrapUp/%s/skimrootSYS/" %njets
outpath = "/uscms/home/yiting11/nobackup/CMSSW_7_4_12_patch4/src/ttbar_preparation/WrapUp/%s/packroot/" %njets
kint = "mtt_dely_RECO" #vararg2D().xy_savename+"_RECO"

ybins = bins2D().ybins
absybins = bins2D().absybins

xbins = bins2D.xbins_4j if njets != '3j' else bins2D().xbins_3j
if(FixBins):
	xbins = [20*i for i in range(101)]
xfixbins = bins2D().xfixbins_3j
if njets == '4j':
	xfixbins = bins2D().xfixbins_4j
elif njets == '5j':
	xfixbins = bins2D().xfixbins_5j
elif njets == '6j':
	xfixbins = bins2D().xfixbins_6j

#print "xbins = ", bins2D().xbins_4j if njets != '3j' else bins2D().xbins_3j, " ", len(bins2D().xbins_4j)-1 if njets != '3j' else len(bins2D().xbins_3j)-1
#print "ybins = ", bins2D().ybins, " ", len(bins2D().ybins)-1
#print "absybins = ", bins2D().absybins, " ", len(bins2D().absybins)-1


def getHistOtherSide(hmean, hder):
	hdiff = hder.Clone()
	his = hmean.Clone()
	hdiff.Add(hmean, -1) #diff = der-mean;	diff = mean-der
	his.Add(hdiff, -1) #his = mean-diff;	his = mean+diff
	return his

def getScaledHist(hmean, hMulti, scale):
	hdiff = hMulti.Clone()
	his = hmean.Clone()
	hdiff.Add(hmean, -1)
	hdiff.Scale(scale)
	his.Add(hdiff, 1)
	return his

def with2sideError(hmc, htemplate): #not using now
	hup = r.TH2D(hmc.GetName()+"witherrup", hmc.GetTitle(), hmc.GetXaxis().GetNbins(), 0, 2000, hmc.GetYaxis().GetNbins(), -6, 6)
	hdown = r.TH2D(hmc.GetName()+"witherrdown", hmc.GetTitle(), hmc.GetXaxis().GetNbins(), 0, 2000, hmc.GetYaxis().GetNbins(), -6, 6)
	for jbin in range(hmc.GetYaxis().GetNbins()):
		for ibin in range(hmc.GetXaxis().GetNbins()):
			#print "print ", ibin+1, jbin+1, hmc.GetBinContent(ibin+1, jbin+1), hmc.GetBinError(ibin+1, jbin+1)
			hup.SetBinContent(ibin+1, jbin+1, hmc.GetBinError(ibin+1, jbin+1) + htemplate.GetBinContent(ibin+1, jbin+1))
			hdown.SetBinContent(ibin+1, jbin+1, htemplate.GetBinContent(ibin+1, jbin+1) - hmc.GetBinError(ibin+1, jbin+1))
	return hup, hdown



globalObjects = []
hlist = []
SysExp = []
FileExp = []
############################################################################################################
fdata = r.TFile(inpath+"skim_DATA.root")
ftt = r.TFile(inpath+"skim_tt_PowhegP8_%s.root" %nominal) #hsig = ftt.Get("1.0y/"+kint)
ft = r.TFile(inpath+"skim_t.root")
fvj = r.TFile(inpath+"skim_VnJets.root")
fqcd = r.TFile(inpathsb+"skim_Tqcd.root")

hnominal = ftt.Get(kint)

hdata = Rebin.Absy(Rebin.newRebin2D(fdata.Get(kint), 'data_obs_temp', xbins, ybins), 'data_obs', xbins, absybins)
hsig = Rebin.Absy(Rebin.newRebin2D(ftt.Get(kint), 'ttsig_temp', xbins, ybins), 'ttsig', xbins, absybins)
ht = Rebin.Absy(Rebin.newRebin2D(ft.Get(kint), 'st_temp', xbins, ybins), 'st', xbins, absybins)
hvj = Rebin.Absy(Rebin.newRebin2D(fvj.Get(kint), 'vjets_temp', xbins, ybins), 'vj', xbins, absybins)
hqcd = Rebin.Absy(Rebin.newRebin2D(fqcd.Get(kint), 'qcd_temp', xbins, ybins), 'qcd', xbins, absybins)

#MC bck templates:
#fvjmc = r.TFile(inpath+"skim_Vj.root")
#hvjmc = fvjmc.Get(kint)
#hvjmcup, hvjmcdown = with2sideError(hvjmc, hvj)
#fqcdmc = r.TFile(inpath+"skim_QCD.root")
#hqcdmc = fqcdmc.Get(kint)
#hqcdmcup, hqcdmcdown = with2sideError(hqcdmc, hqcd)

#hvjmcup2 = Rebin.Absy(Rebin.newRebin2D(hvjmcup, 'vjetsNorUp_temp', xbins, ybins), 'vjetsNorUp', xbins, absybins)
#hvjmcdown2 = Rebin.Absy(Rebin.newRebin2D(hvjmcdown, 'vjetsNorDown_temp', xbins, ybins), 'vjetsNorDown', xbins, absybins)
#hqcdmcup2 = Rebin.Absy(Rebin.newRebin2D(hqcdmcup, 'qcdNorUp_temp', xbins, ybins), 'qcdNorUp', xbins, absybins)
#hqcdmcdown2 = Rebin.Absy(Rebin.newRebin2D(hqcdmcdown, 'qcdNorDown_temp', xbins, ybins), 'qcdNorDown', xbins, absybins)

############################################################################################################
if(ADD_QCDcsvSYS):
	fcsvup = r.TFile("/uscms/home/yiting11/nobackup/CMSSW_7_4_12_patch4/src/ttbar_preparation/WrapUp/%s/skimrootSYS/csvUp/skim_csvUp_Tqcd.root" %njets)
	fcsvdown = r.TFile("/uscms/home/yiting11/nobackup/CMSSW_7_4_12_patch4/src/ttbar_preparation/WrapUp/%s/skimrootSYS/csvDown/skim_csvDown_Tqcd.root" %njets)
	#fcsvup = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/skimrootSB_B0.3to0.6/skim_Tqcd.root" %njets)
	#fcsvdown = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/skimrootSB_Aless0.3/skim_Tqcd.root" %njets)
	#fcsvup = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/skimrootSB_comp2/skim_Tqcd.root" %njets)
	#fcsvdown = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/skimrootSB_comp1/skim_Tqcd.root" %njets)
	hcsvup = Rebin.Absy(Rebin.newRebin2D(fcsvup.Get(kint), 'qcd_csvUp_temp', xbins, ybins), 'qcd_csvUp', xbins, absybins)
	hcsvdown = Rebin.Absy(Rebin.newRebin2D(fcsvdown.Get(kint), 'qcd_csvDown_temp', xbins, ybins), 'qcd_csvDown', xbins, absybins)


############################################################################################################
if(ADD_NNLOpT):
	fnnloup = r.TFile(inpathsys+"nnlopt/skim_nnlopt_tt_PowhegP8_noEW.root")

	hnnloup = getScaledHist(hnominal, fnnloup.Get(kint), 1.0) #1.03488696492)
	hnnlodown = getHistOtherSide(hnominal, fnnloup.Get(kint))
	#hnnlodown = getHistOtherSide(hnominal, hnominal)

	#hnnloup = Rebin.Absy(Rebin.newRebin2D(fnnloup.Get(kint), 'ttsig_ptUp_temp', xbins, ybins), 'ttsig_ptUp', xbins, absybins)
	hnnloup = Rebin.Absy(Rebin.newRebin2D(hnnloup, 'ttsig_ptUp_temp', xbins, ybins), 'ttsig_ptUp', xbins, absybins)
	hnnlodown = Rebin.Absy(Rebin.newRebin2D(hnnlodown, 'ttsig_ptDown_temp', xbins, ybins), 'ttsig_ptDown', xbins, absybins)

############################################################################################################
#Theoretical systematics
if(ADD_THSYS):
	#up/down
	ffsup = r.TFile(inpathsys+"fsUp/skim_fsUp_tt_PowhegP8_%s.root" %nominal)
	ffsdown = r.TFile(inpathsys+"fsDown/skim_fsDown_tt_PowhegP8_%s.root" %nominal)
	frsup = r.TFile(inpathsys+"rsUp/skim_rsUp_tt_PowhegP8_%s.root" %nominal)
	frsdown = r.TFile(inpathsys+"rsDown/skim_rsDown_tt_PowhegP8_%s.root" %nominal)
	frsfsSSup = r.TFile(inpathsys+"rsfsUp/skim_rsfsUp_tt_PowhegP8_%s.root" %nominal)
	frsfsSSdown = r.TFile(inpathsys+"rsfsDown/skim_rsfsDown_tt_PowhegP8_%s.root" %nominal)
	fbdecayup = r.TFile(inpathsys+"bdecayUp/skim_bdecayUp_tt_PowhegP8_%s.root" %nominal)
	fbdecaydown = r.TFile(inpathsys+"bdecayDown/skim_bdecayDown_tt_PowhegP8_%s.root" %nominal)
	fbfragup = r.TFile(inpathsys+"bfragUp/skim_bfragUp_tt_PowhegP8_%s.root" %nominal)
	fbfragdown = r.TFile(inpathsys+"bfragDown/skim_bfragDown_tt_PowhegP8_%s.root" %nominal)

	hfsup = Rebin.Absy(Rebin.newRebin2D(ffsup.Get(kint), 'ttsig_fsUp_temp', xbins, ybins), 'ttsig_fsUp', xbins, absybins)
	hfsdown = Rebin.Absy(Rebin.newRebin2D(ffsdown.Get(kint), 'ttsig_fsDown_temp', xbins, ybins), 'ttsig_fsDown', xbins, absybins)
	hrsup = Rebin.Absy(Rebin.newRebin2D(frsup.Get(kint), 'ttsig_rsUp_temp', xbins, ybins), 'ttsig_rsUp', xbins, absybins)
	hrsdown = Rebin.Absy(Rebin.newRebin2D(frsdown.Get(kint), 'ttsig_rsDown_temp', xbins, ybins), 'ttsig_rsDown', xbins, absybins)
	hrsfsSSup = Rebin.Absy(Rebin.newRebin2D(frsfsSSup.Get(kint), 'ttsig_rsfsSSUp_temp', xbins, ybins), 'ttsig_rsfsSSUp', xbins, absybins)
	hrsfsSSdown = Rebin.Absy(Rebin.newRebin2D(frsfsSSdown.Get(kint), 'ttsig_rsfsSSDown_temp', xbins, ybins), 'ttsig_rsfsSSDown', xbins, absybins)
	hbdecayup = Rebin.Absy(Rebin.newRebin2D(fbdecayup.Get(kint), 'ttsig_bdecayUp_temp', xbins, ybins), 'ttsig_bdecayUp', xbins, absybins)
	hbdecaydown = Rebin.Absy(Rebin.newRebin2D(fbdecaydown.Get(kint), 'ttsig_bdecayDown_temp', xbins, ybins), 'ttsig_bdecayDown', xbins, absybins)
	hbfragup = Rebin.Absy(Rebin.newRebin2D(fbfragup.Get(kint), 'ttsig_bfragUp_temp', xbins, ybins), 'ttsig_bfragUp', xbins, absybins)
	hbfragdown = Rebin.Absy(Rebin.newRebin2D(fbfragdown.Get(kint), 'ttsig_bfragDown_temp', xbins, ybins), 'ttsig_bfragDown', xbins, absybins)

	#rsfs envelope
	rnnlo_up = 851.53/831.76
	rnnlo_dw = 802.56/831.76
	#hrsfsenup = hsig
	#hrsfsendw = hsig
	#hrsfsenup.SetName("ttsig_rsfsUp")
	#hrsfsendw.SetName("ttsig_rsfsDown")
	hrsfsenup = r.TH2D("ttsig_rsfsUp", "ttsig_rsfsup", len(xbins), 0, 2000, len(absybins), 0, 6)
	hrsfsendw = r.TH2D("ttsig_rsfsDown", "ttsig_rsfsDown", hsig.GetNbinsX(), 0, 2000, hsig.GetNbinsY(), 0, 6)
	for xbin in range(hsig.GetNbinsX()):
		for ybin in range(hsig.GetNbinsY()):
			mean = hsig.GetBinContent(xbin+1,ybin+1)
			envelope_up = min(hrsup.GetBinContent(xbin+1,ybin+1), hfsup.GetBinContent(xbin+1,ybin+1), hrsfsSSup.GetBinContent(xbin+1,ybin+1), hsig.GetBinContent(xbin+1,ybin+1))
			envelope_dw = max(hrsdown.GetBinContent(xbin+1,ybin+1), hfsdown.GetBinContent(xbin+1,ybin+1), hrsfsSSdown.GetBinContent(xbin+1,ybin+1), hsig.GetBinContent(xbin+1,ybin+1))
			#hrsfsenup.SetBinContent(xbin+1, ybin+1, mean + (rnnlo_up*(envelope_up-mean)))
			#hrsfsendw.SetBinContent(xbin+1, ybin+1, mean + (rnnlo_dw*(envelope_dw-mean)))
			hrsfsenup.SetBinContent(xbin+1, ybin+1, envelope_up)
			hrsfsendw.SetBinContent(xbin+1, ybin+1, envelope_dw)
			hrsfsenup.SetBinError(xbin+1, ybin+1, hrsfsSSup.GetBinError(xbin+1,ybin+1))#a little simplied case
			hrsfsendw.SetBinError(xbin+1, ybin+1, hrsfsSSdown.GetBinError(xbin+1,ybin+1))#directly take the error from rsfs, the fitting result won't affect; this only shows the error bar of the up/down templates
	print "rsfs:", hsig.Integral(), hrsfsenup.Integral(), hrsfsendw.Integral(), hrsfsSSup.GetNbinsX(), hrsfsSSdown.GetNbinsY()
	hrsfsenup.Scale(rnnlo_dw*(hsig.Integral()/hrsfsenup.Integral()))
	hrsfsendw.Scale(rnnlo_up*(hsig.Integral()/hrsfsendw.Integral()))

	hrsfsSSup.Scale(rnnlo_dw*(hsig.Integral()/hrsfsSSup.Integral()))
	hrsfsSSdown.Scale(rnnlo_up*(hsig.Integral()/hrsfsSSdown.Integral()))


	#new PDF sets taken after runing Otto's algorithm:
	#fpdf = r.TFile('pdfsys/combineSubsetPDFs/%s/pdfT.root' %njets)
	#hpdf1up = fpdf.Get('ttsig_pdf1Up')
	#hpdf1down = fpdf.Get('ttsig_pdf1Down')
	#hpdf2up = fpdf.Get('ttsig_pdf2Up')
	#hpdf2down = fpdf.Get('ttsig_pdf2Down')
	#hpdfsumup = fpdf.Get('ttsig_pdfsumUp')
	#hpdfsumdown = fpdf.Get('ttsig_pdfsumDown')

	#RMS of the 100 pset, read-in file is generated by syspdf.py
	#fpdf = r.TFile(inpath+"skim_pdf_tt_PowhegP8_%s.root" %nominal)
	#hpdfup = fpdf.Get("2DPDF")
	#hpdfup = Rebin.newRebin2D(hpdfup, 'ttsig_pdfUp', xbins, absybins)
	#hpdfdown = getHistOtherSide(hsig, hpdfup)
	#hpdfdown.SetName("ttsig_pdfDown")
	#alpha_s
	#halphaup = fpdf.Get("2DalphaUp")
	#halphadown = fpdf.Get("2DalphaDown")
	#halphaup = Rebin.newRebin2D(halphaup, 'ttsig_alphaUp', xbins, absybins)
	#halphadown = Rebin.newRebin2D(halphadown, 'ttsig_alphaDown', xbins, absybins)


	#sys derived with dedicated MC samples
	fmt1up = r.TFile(inpathsys+"MCs/skim_mtop1735_tt_PowhegP8_%s.root" %nominal)
	fmt1down = r.TFile(inpathsys+"MCs/skim_mtop1715_tt_PowhegP8_%s.root" %nominal)
	#fmt3up = r.TFile(inpathsys+"/MCs/skim_mtop1755_tt_PowhegP8_%s.root" %nominal)
	#fmt3down = r.TFile(inpathsys+"/MCs/skim_mtop1695_tt_PowhegP8_%s.root" %nominal)
	fisrup = r.TFile(inpathsys+"MCs/skim_isrup_tt_PowhegP8_%s.root" %nominal)
	fisrdown = r.TFile(inpathsys+"MCs/skim_isrdown_tt_PowhegP8_%s.root" %nominal)
	ffsrup = r.TFile(inpathsys+"MCs/skim_fsrup_tt_PowhegP8_%s.root" %nominal)
	ffsrdown = r.TFile(inpathsys+"MCs/skim_fsrdown_tt_PowhegP8_%s.root" %nominal)
	fhdampup = r.TFile(inpathsys+"MCs/skim_hdup_tt_PowhegP8_%s.root" %nominal)
	fhdampdown = r.TFile(inpathsys+"MCs/skim_hddown_tt_PowhegP8_%s.root" %nominal)
	ftuneup = r.TFile(inpathsys+"MCs/skim_tuneup_tt_PowhegP8_%s.root" %nominal)
	ftunedown = r.TFile(inpathsys+"MCs/skim_tunedown_tt_PowhegP8_%s.root" %nominal)
	fcolorup = r.TFile(inpathsys+"MCs/skim_erdon_tt_PowhegP8_%s.root" %nominal)

	#hmt3up = getScaledHist(hnominal, fmt3up.Get(kint), 1./3.)
	#hmt3down = getScaledHist(hnominal, fmt3down.Get(kint), 1./3.)
	hisrup = getScaledHist(hnominal, fisrup.Get(kint), 1/sqrt(2))
	hisrdown = getScaledHist(hnominal, fisrdown.Get(kint), 1/sqrt(2))
	hfsrup = getScaledHist(hnominal, ffsrup.Get(kint), 1/sqrt(2))
	hfsrdown = getScaledHist(hnominal, ffsrdown.Get(kint), 1/sqrt(2))
	hcolorup = getScaledHist(hnominal, fcolorup.Get(kint), 1) #1.03488696492)
	hcolordown = getHistOtherSide(hnominal, fcolorup.Get(kint))

	hmt1up = Rebin.Absy(Rebin.newRebin2D(fmt1up.Get(kint), 'ttsig_mt1Up_temp', xbins, ybins), 'ttsig_mt1Up', xbins, absybins)
	hmt1down = Rebin.Absy(Rebin.newRebin2D(fmt1down.Get(kint), 'ttsig_mt1Down_temp', xbins, ybins), 'ttsig_mt1Down', xbins, absybins)
	#hmt3up = Rebin.Absy(Rebin.newRebin2D(hmt3up, 'ttsig_mt3Up_temp', xbins, ybins), 'ttsig_mt3Up', xbins, absybins)
	#hmt3down = Rebin.Absy(Rebin.newRebin2D(hmt3down, 'ttsig_mt3Down_temp', xbins, ybins), 'ttsig_mt3Down', xbins, absybins)
	hdampup = Rebin.Absy(Rebin.newRebin2D(fhdampup.Get(kint), 'ttsig_hdampUp_temp', xbins, ybins), 'ttsig_hdampUp', xbins, absybins)
	hdampdown = Rebin.Absy(Rebin.newRebin2D(fhdampdown.Get(kint), 'ttsig_hdampDown_temp', xbins, ybins), 'ttsig_hdampDown', xbins, absybins)
	hisrup = Rebin.Absy(Rebin.newRebin2D(hisrup, 'ttsig_isrUp_temp', xbins, ybins), 'ttsig_isrUp', xbins, absybins)
	hisrdown = Rebin.Absy(Rebin.newRebin2D(hisrdown, 'ttsig_isrDown_temp', xbins, ybins), 'ttsig_isrDown', xbins, absybins)
	hfsrup = Rebin.Absy(Rebin.newRebin2D(hfsrup, 'ttsig_fsrUp_temp', xbins, ybins), 'ttsig_fsrUp', xbins, absybins)
	hfsrdown = Rebin.Absy(Rebin.newRebin2D(hfsrdown, 'ttsig_fsrDown_temp', xbins, ybins), 'ttsig_fsrDown', xbins, absybins)
	htuneup = Rebin.Absy(Rebin.newRebin2D(ftuneup.Get(kint), 'ttsig_tuneUp_temp', xbins, ybins), 'ttsig_tuneUp', xbins, absybins)
	htunedown = Rebin.Absy(Rebin.newRebin2D(ftunedown.Get(kint), 'ttsig_tuneDown_temp', xbins, ybins), 'ttsig_tuneDown', xbins, absybins)
	hcolorup = Rebin.Absy(Rebin.newRebin2D(fcolorup.Get(kint), 'ttsig_colorUp_temp', xbins, ybins), 'ttsig_colorUp', xbins, absybins)
	hcolordown = Rebin.Absy(Rebin.newRebin2D(hcolordown, 'ttsig_colorDown_temp', xbins, ybins), 'ttsig_colorDown', xbins, absybins)
	#hcolorup = Rebin.newRebin2D(fcolorup.Get(kint), 'colorUp_temp', xbins, ybins)
	#hcolordown = Rebin.newRebin2D(hcolordown, 'colorDown_temp', xbins, ybins)
	#hcolorup = fcolorup.Get(kint)
	#hcolordown = hcolordown

#fhadro = r.TFile(inpath+"skim_tt_PowhegHpp.root")
#hadroup = fhadro.Get(kint)
#hadrodown = getHistOtherSide(hnominal, hadroup)
#fnlo = r.TFile(inpath+"skim_tt_aMCatNLO.root")
#hnloup = fnlo.Get(kint)
#hnlodown = getHistOtherSide(hnominal, hnloup)

#hadroup2 = Rebin.Absy(Rebin.newRebin2D(hadroup, 'hadroUp_temp', xbins, ybins), 'hadroUp', xbins, absybins)
#hadrodown2 = Rebin.Absy(Rebin.newRebin2D(hadrodown, 'hadroDown_temp', xbins, ybins), 'hadroDown', xbins, absybins)
#hnloup2 = Rebin.Absy(Rebin.newRebin2D(hnloup, 'NLOUp_temp', xbins, ybins), 'NLOUp', xbins, absybins)
#hnlodown2 = Rebin.Absy(Rebin.newRebin2D(hnlodown, 'NLODown_temp', xbins, ybins), 'NLODown', xbins, absybins)

############################################################################################################
if(ADD_THSYS_ST):
	#ffsrdown_st = r.TFile(inpath+"skim_fsrDown_t.root", "READ")
	#hfsrdown_st = getScaledHist(ft.Get(kint), ffsrdown_st.Get(kint), 1/sqrt(2))
	#hfsrdown_st = Rebin.Absy(Rebin.newRebin2D(hfsrdown_st, 'st_fsrDown_temp', xbins, ybins), 'st_fsrDown', xbins, absybins)

	#hfsrup_st = getHistOtherSide(ht, hfsrdown_st)
	#hfsrup_st.SetName("st_fsrUp")

	fbfragup_st = r.TFile(inpathsys+"bfragUp/skim_bfragUp_t.root", "READ")
	fbfragdown_st = r.TFile(inpathsys+"bfragDown/skim_bfragDown_t.root", "READ")
	hbfragup_st = Rebin.Absy(Rebin.newRebin2D(fbfragup_st.Get(kint), 'st_bfragUp_temp', xbins, ybins), 'st_bfragUp', xbins, absybins)
	hbfragdown_st = Rebin.Absy(Rebin.newRebin2D(fbfragdown_st.Get(kint), 'st_bfragDown_temp', xbins, ybins), 'st_bfragDown', xbins, absybins)

	fbdecayup_st = r.TFile(inpathsys+"bdecayUp/skim_bdecayUp_t.root", "READ")
	fbdecaydown_st = r.TFile(inpathsys+"bdecayDown/skim_bdecayDown_t.root", "READ")
	hbdecayup_st = Rebin.Absy(Rebin.newRebin2D(fbdecayup_st.Get(kint), 'st_bdecayUp_temp', xbins, ybins), 'st_bdecayUp', xbins, absybins)
	hbdecaydown_st = Rebin.Absy(Rebin.newRebin2D(fbdecaydown_st.Get(kint), 'st_bdecayDown_temp', xbins, ybins), 'st_bdecayDown', xbins, absybins)

	#fwt = r.TFile(inpath+"skim_Wt.root")
	#fwtbar = r.TFile(inpath+"skim_Wtbar.root")
	#hwt = Rebin.Absy(Rebin.newRebin2D(fwt.Get(kint), 'wt_temp', xbins, ybins), 'st_pdfUp_temp', xbins, absybins)
	#hwtbar = Rebin.Absy(Rebin.newRebin2D(fwtbar.Get(kint), 'wtbar_temp', xbins, ybins), 'st_pdfUp_temp', xbins, absybins)

	#RMS of the 100 pset, read-in file is generated by syspdf.py
	#fpdf_st_part = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/pdfsys/RMS/%s/skim_pdf_STt.root" %njets)
	#hpdfup_st_part = fpdf_st_part.Get("2DPDF")
	#hpdfup_st_part = Rebin.newRebin2D(hpdfup_st_part, 'st_pdfUp', xbins, absybins)
	#hpdfup_st = hpdfup_st_part.Clone()
	#hpdfup_st.Add(hwt,1)
	#hpdfup_st.Add(hwtbar,1)
	#hpdfdown_st = getHistOtherSide(ht, hpdfup_st)
	#hpdfdown_st.SetName("st_pdfDown")

	#halphaup_st_part = fpdf_st_part.Get("2DalphaUp")
	#halphadown_st_part = fpdf_st_part.Get("2DalphaDown")
	#halphaup_st_part = Rebin.newRebin2D(halphaup_st_part, 'st_alphaUp', xbins, absybins)
	#halphadown_st_part = Rebin.newRebin2D(halphadown_st_part, 'st_alphaDown', xbins, absybins)
	#halphaup_st = halphaup_st_part.Clone()
	#halphadown_st = halphadown_st_part.Clone()
	#halphaup_st.Add(hwt,1)
	#halphaup_st.Add(hwtbar,1)
	#halphadown_st.Add(hwt,1)
	#halphadown_st.Add(hwtbar,1)


############################################################################################################
#Experimental systematics
hup = r.TH2D()
hdw = r.TH2D()

if(ADD_EXPSYS):
	for sys in writeSysExp:
		fup = r.TFile(inpathsys+sys+"Up/skim_"+sys+"Up_tt_PowhegP8_"+nominal+".root","READ")
		fdw = r.TFile(inpathsys+sys+"Down/skim_"+sys+"Down_tt_PowhegP8_"+nominal+".root","READ")
		FileExp.append(fup)
		FileExp.append(fdw)
		hup = Rebin.Absy(Rebin.newRebin2D(fup.Get(kint), 'ttsig_'+sys+"Up_temp", xbins, ybins), 'ttsig_'+sys+'Up', xbins, absybins)
		hdw = Rebin.Absy(Rebin.newRebin2D(fdw.Get(kint), 'ttsig_'+sys+"Down_temp", xbins, ybins), 'ttsig_'+sys+'Down', xbins, absybins)
		SysExp.append(hup)
		SysExp.append(hdw)

	for sys in writeSysExp:
		fup = r.TFile(inpathsys+sys+"Up/skim_"+sys+"Up_t.root","READ")
		fdw = r.TFile(inpathsys+sys+"Down/skim_"+sys+"Down_t.root","READ")
		FileExp.append(fup)
		FileExp.append(fdw)
		hup = Rebin.Absy(Rebin.newRebin2D(fup.Get(kint), 'st_'+sys+"Up_temp", xbins, ybins), 'st_'+sys+'Up', xbins, absybins)
		hdw = Rebin.Absy(Rebin.newRebin2D(fdw.Get(kint), 'st_'+sys+"Down_temp", xbins, ybins), 'st_'+sys+'Down', xbins, absybins)
		SysExp.append(hup)
		SysExp.append(hdw)

	#for sys in writeSysExp_vj:
	#	fup = r.TFile(inpath+"skim_"+sys+"Up_VnJets.root","READ")
	#	fdw = r.TFile(inpath+"skim_"+sys+"Down_VnJets.root","READ")
	#	FileExp.append(fup)
	#	FileExp.append(fdw)
	#	hup = Rebin.Absy(Rebin.newRebin2D(fup.Get(kint), 'vj_'+sys+"Up_temp", xbins, ybins), 'vj_'+sys+'Up', xbins, absybins)
	#	hdw = Rebin.Absy(Rebin.newRebin2D(fdw.Get(kint), 'vj_'+sys+"Down_temp", xbins, ybins), 'vj_'+sys+'Down', xbins, absybins)
	#	SysExp.append(hup)
	#	SysExp.append(hdw)

	if(BreakDownJES):
		for jescomp in breakdownJES:
			fup = r.TFile(inpathsys+"JESUp"+jescomp+"/skim_JESUp"+jescomp+"_tt_PowhegP8_"+nominal+".root","READ")
			fdw = r.TFile(inpathsys+"JESDown"+jescomp+"/skim_JESDown"+jescomp+"_tt_PowhegP8_"+nominal+".root","READ")
			FileExp.append(fup)
			FileExp.append(fdw)
			hup = Rebin.Absy(Rebin.newRebin2D(fup.Get(kint), 'ttsig_JES'+jescomp+"Up_temp", xbins, ybins), 'ttsig_JES'+jescomp+'Up', xbins, absybins)
			hdw = Rebin.Absy(Rebin.newRebin2D(fdw.Get(kint), 'ttsig_JES'+jescomp+"Down_temp", xbins, ybins), 'ttsig_JES'+jescomp+'Down', xbins, absybins)
			SysExp.append(hup)
			SysExp.append(hdw)

		for jescomp in breakdownJES:
			fup = r.TFile(inpathsys+"JESUp"+jescomp+"/skim_JESUp"+jescomp+"_t.root","READ")
			fdw = r.TFile(inpathsys+"JESDown"+jescomp+"/skim_JESDown"+jescomp+"_t.root","READ")
			FileExp.append(fup)
			FileExp.append(fdw)
			hup = Rebin.Absy(Rebin.newRebin2D(fup.Get(kint), 'st_JES'+jescomp+"Up_temp", xbins, ybins), 'st_JES'+jescomp+"Up", xbins, absybins)
			hdw = Rebin.Absy(Rebin.newRebin2D(fdw.Get(kint), 'st_JES'+jescomp+"Down_temp", xbins, ybins), 'st_JES'+jescomp+"Down", xbins, absybins)
			SysExp.append(hup)
			SysExp.append(hdw)

		#for jescomp in breakdownJES:
		#	fup = r.TFile(inpath+"skim_JESUp"+jescomp+"_VnJets.root","READ")
		#	fdw = r.TFile(inpath+"skim_JESDown"+jescomp+"_VnJets.root","READ")
		#	FileExp.append(fup)
		#	FileExp.append(fdw)
		#	hup = Rebin.Absy(Rebin.newRebin2D(fup.Get(kint), 'vj_JES'+jescomp+"Up_temp", xbins, ybins), 'vj_JES'+jescomp+"Up", xbins, absybins)
		#	hdw = Rebin.Absy(Rebin.newRebin2D(fdw.Get(kint), 'vj_JES'+jescomp+"Down_temp", xbins, ybins), 'vj_JES'+jescomp+"Down", xbins, absybins)
		#	SysExp.append(hup)
		#	SysExp.append(hdw)

############################################################################################################
os.system("mkdir -p "+outpath)
outfileshow = r.TFile(outpath+"ch%sdraw2d.root"%njets, "RECREATE")
writeComponents = [hdata, hsig, ht, hvj, hqcd, hcsvup, hcsvdown] if(ADD_QCDcsvSYS) else [hdata, hsig, ht, hvj, hqcd]

SysTH = []
SysTH_t = []
for s in writeSysTH:
	SysTH.append("h"+s+"up")
	SysTH.append("h"+s+"down")
for s in writeSysTH_t:
	SysTH_t.append("h"+s+"up_st")
	SysTH_t.append("h"+s+"down_st")

print "SysExp:",SysExp
print "SysTH:",SysTH
print "SysTH_t:",SysTH_t

for his in writeComponents:
	his.Write()
	hlist.append(his)

if(ADD_EXPSYS):
	for his in SysExp:
		#his = r.gDirectory.Get(his)
		#r.gDirectory.ls()
		#his = eval(his)
		his.Write()
		hlist.append(his)
if(ADD_THSYS):
	for his in SysTH:
		his = eval(his)
		his.Write()
		hlist.append(his)
	hlist.append(hrsfsSSup)
	hlist.append(hrsfsSSdown)
	#hlist.append(hrsfsenup)
	#hlist.append(hrsfsendw)
if(ADD_THSYS_ST):
	for his in SysTH_t:
		his = eval(his)
		his.Write()
		hlist.append(his)
if(ADD_NNLOpT):
	for his in [hnnloup, hnnlodown]:
		his.Write()
		hlist.append(his)

outfileshow.Close()

############################################################################################################
outfile = r.TFile(outpath+"ch%s_partial.root" %njets, "RECREATE")

h = {}
for h in hlist:
	if(FixBins):
		optbin = 0
		opthall = r.TH1D(h.GetName()+"_temp", h.GetTitle(), sum(len(x) for x in xfixbins), 0, sum(len(x) for x in xfixbins))
		for j in range(hsig.GetYaxis().GetNbins()):
			arrayi = xfixbins[j]
			for i in range(len(arrayi)-1):
				carry = 0
				Ecarry = r.Double(0)
				optbin += 1

				#print arrayi[i], arrayi[i+1]
				#print h.GetXaxis().FindFixBin(arrayi[i]), h.GetXaxis().FindFixBin(arrayi[i+1])-1
				carry = h.IntegralAndError(h.GetXaxis().FindFixBin(arrayi[i]), h.GetXaxis().FindFixBin(arrayi[i+1])-1, j+1, j+1, Ecarry)
				opthall.SetBinContent(optbin, carry)
				opthall.SetBinError(optbin, Ecarry)
				opthall.GetXaxis().SetBinLabel(optbin,"%s-%s,%s-%s" %(arrayi[i],arrayi[i+1], absybins[j],absybins[j+1]))

		#print optbin
		hall = r.TH1D(h.GetName(), h.GetTitle(), optbin, 0, optbin)
		for ibin in range(optbin):
			print "final binning", ibin+1, opthall.GetXaxis().GetBinLabel(ibin+1)
			hall.SetBinContent(ibin+1, opthall.GetBinContent(ibin+1))
			hall.SetBinError(ibin+1, opthall.GetBinError(ibin+1))
			hall.GetXaxis().SetBinLabel(ibin+1, str(opthall.GetXaxis().GetBinLabel(ibin+1)))
		hall.Write()

	else:
		#print xbins
		opthall = r.TH1D(h.GetName()+"_temp", h.GetTitle(), 1000, 0, 1000) #1000 is just a big number which definiely larger than the bins we want in the end
		optbin = 0
		lastbinmark = []
		for j in range(hsig.GetYaxis().GetNbins()):
			bee = 0
			carry = 0
			Ecarry = 0
			mbin = 0
			mark = []

			for i in range(hsig.GetXaxis().GetNbins()):
				bee = hsig.GetBinContent(i+1, j+1) + bee #number of signal hist
				carry = h.GetBinContent(i+1, j+1) + carry #number of target hist
				#E = r.Double(0.)
				#Ecarry = h.IntegralAndError(i+1, i+1, j+1, j+1, E) + Ecarry
				Ecarry = h.GetBinError(i+1, j+1)*h.GetBinError(i+1, j+1) + Ecarry
				print carry, Ecarry
				#print hsig.GetBinContent(i+1, j+1), bee

				if(bee >numin):
					optbin += 1
					if(hsig.GetBinContent(i+1, j+1) == bee):
						opthall.GetXaxis().SetBinLabel(optbin,"%s-%s,%s-%s" %(hsig.GetXaxis().GetBinLowEdge(i+1),hsig.GetXaxis().GetBinLowEdge(i+2),absybins[j],absybins[j+1]))
						#opthall.GetXaxis().SetBinLabel(optbin,"%s" %hsig.GetXaxis().GetBinLowEdge(i+1))
						#print optbin, hsig.GetXaxis().GetBinLowEdge(i+1),hsig.GetXaxis().GetBinLowEdge(i+2),absybins[j],absybins[j+1], "mark = ", mark, "mbin=", mbin
					else:
						opthall.GetXaxis().SetBinLabel(optbin,"%s-%s,%s-%s" %(mark[-mbin],hsig.GetXaxis().GetBinLowEdge(i+2),absybins[j],absybins[j+1]))
						#opthall.GetXaxis().SetBinLabel(optbin,"%s" %mark[-mbin])
						#print optbin, mark[-mbin],hsig.GetXaxis().GetBinLowEdge(i+2),absybins[j],absybins[j+1], "mark = ", mark, "mbin=", mbin

					if(carry>=0):
						opthall.SetBinContent(optbin, carry)
						opthall.SetBinError(optbin, sqrt(Ecarry))
					else:
						opthall.SetBinContent(optbin, 0.0)
						opthall.SetBinError(optbin, sqrt(Ecarry))

					bee = 0
					carry = 0
					Ecarry = 0
					mbin = 0

				else:
					mbin += 1
					mark.append(hsig.GetXaxis().GetBinLowEdge(i+1))

					if(i == hsig.GetXaxis().GetNbins()-1): #if it couldn't accumulate enough events event when it goes to the last bin
						optbin += 1
						opthall.SetBinContent(optbin, carry)
						opthall.SetBinError(optbin, sqrt(Ecarry))
						opthall.GetXaxis().SetBinLabel(optbin,"%s-%s,%s-%s" %(mark[-mbin],hsig.GetXaxis().GetBinLowEdge(i+2),absybins[j],absybins[j+1]))
						#opthall.GetXaxis().SetBinLabel(optbin,"%s" %mark[-mbin])
						lastbinmark.append(optbin)
						bee = 0
						carry = 0
						Ecarry = 0

			mbin = 0
			del mark[:]

		print lastbinmark

		raw = []
		Eraw = []
		for ibin in range(optbin):
			raw.append(opthall.GetBinContent(ibin+1))
			Eraw.append(opthall.GetBinError(ibin+1))
		print len(raw), raw

		# ______________________
		refine = []
		mergeLastBin = True
		lastbinmarkminusone = [each-1 for each in lastbinmark]
		lastbinmarkminustwo = [each-2 for each in lastbinmark]
		print lastbinmarkminusone, lastbinmarkminustwo
		labelList = []
		labelListprintX = []
		for ielement,element in enumerate(raw):
			if mergeLastBin:
				if ielement in lastbinmarkminustwo:
					refine.append(element+raw[ielement+1])
					s = opthall.GetXaxis().GetBinLabel(ielement+1)
					labelList.append("%s-2000,%s" %(s.split(',')[0].split('-')[0], s.split(',')[1]))
					labelListprintX.append(s.split(',')[0].split('-')[0])
					#print ielement+1, "%s-2000,%s" %(s.split(',')[0].split('-')[0], s.split(',')[1])
				elif ielement in lastbinmarkminusone:
					continue
				else:
					refine.append(element)
					s = opthall.GetXaxis().GetBinLabel(ielement+1)
					labelList.append(s)
					labelListprintX.append(s.split(',')[0].split('-')[0])
					#print ielement+1
			else:
				refine.append(element)
				labelList.append(opthall.GetXaxis().GetBinLabel(ielement+1))
		print "here", len(refine),refine
		#print labelList
		labelListprintX.append(2000)
		print labelListprintX

		Erefine = []
		for ielement,element in enumerate(Eraw):
			if mergeLastBin:
				if ielement in lastbinmarkminustwo:
					Erefine.append(element+Eraw[ielement+1])
				elif ielement in lastbinmarkminusone:
					continue
				else:
					Erefine.append(element)
			else:
				Erefine.append(element)

		print "here err", len(Erefine),Erefine
		# ______________________

		#re-save the opthall to the bin number it should be
		hall = r.TH1D(h.GetName(), h.GetTitle(), len(refine), 0, len(refine))
		for ibin in range(len(refine)):
			print "final binning", ibin+1, labelList[ibin]
			hall.SetBinError(ibin+1, Erefine[ibin])
			hall.SetBinContent(ibin+1, refine[ibin])
			#hall.SetBinContent(ibin+1, opthall.GetBinContent(ibin+1))
			#hall.GetXaxis().SetBinLabel(ibin+1, str(ibin+1))
			hall.GetXaxis().SetBinLabel(ibin+1, str(labelList[ibin]))
			#hall.GetXaxis().SetLabelSize(0.03)
			#hall.GetXaxis().LabelsOption("v")
		hall.Write()


outfile.Close()


for file in globalObjects:
	file.Close()

