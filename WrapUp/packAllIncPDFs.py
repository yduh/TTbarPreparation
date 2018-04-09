#!/usr/bin/python
import ROOT as r
import sys, os

njets = sys.argv[1]

ftt = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/pdfsys/CT14/%s/skim_pdf_tt_PowhegP8_noEW.root" %njets)
ft = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/pdfsys/CT14/%s/skim_pdf_t_noEW.root" %njets)

########################################################################################################################
def pdfUpDown(rootfile,saveName):
	#get the nominal hist from chnj_partial.root (the output of the pack.py)
	fnominal = r.TFile('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/packroot/ch%s_partial.root' %(njets,njets))
	hnominal = fnominal.Get(saveName)
	if hnominal.GetNbinsX() != ftt.Get('relUnc_113').GetNbinsX():
		print hnominal.GetNbinsX(), ftt.Get('relUnc_113').GetNbinsX(), "binnings are not the same!"

	outfile = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/packroot/skim_pdfct14_%s.root" %(njets,saveName), "RECREATE")
	#CT14 PDF sets
	for pset in range(113, 169, 2):
		hpdfUp = r.TH1D("%s_pdf%s%sUp" %(saveName,str(pset),str(pset+1)), "%s_pdf%s%sUp" %(saveName,str(pset),str(pset+1)), hnominal.GetNbinsX(), 0, hnominal.GetNbinsX())
		hpdfDown = r.TH1D("%s_pdf%s%sDown" %(saveName,str(pset),str(pset+1)), "%s_pdf%s%sDown" %(saveName,str(pset),str(pset+1)), hnominal.GetNbinsX(), 0, hnominal.GetNbinsX())
		print pset, pset+1
		hrelUncUp = rootfile.Get('relUnc_'+str(pset))
		hrelUncDown = rootfile.Get('relUnc_'+str(pset+1))
		for ibin in range(hnominal.GetNbinsX()):
			hpdfUp.SetBinContent(ibin+1, hnominal.GetBinContent(ibin+1) *(1+hrelUncUp.GetBinContent(ibin+1)))
			hpdfDown.SetBinContent(ibin+1, hnominal.GetBinContent(ibin+1) *(1+hrelUncDown.GetBinContent(ibin+1)))
		hpdfUp.Write()
		hpdfDown.Write()
	outfile.Close()


def alphaUpDown(rootfile,saveName):
	#get the nominal hist from chnj_partial.root (the output of the pack.py)
	fnominal = r.TFile('/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/packroot/ch%s_partial.root' %(njets,njets))
	hnominal = fnominal.Get(saveName)

	outfile = r.TFile("/afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/ttbar_preparation/WrapUp/%s/packroot/skim_alpha_%s.root" %(njets,saveName), "RECREATE")
	#alpha_s
	halphaUp = r.TH1D("%s_alphaUp" %saveName, "%s_alphaUp" %saveName, hnominal.GetNbinsX(), 0, hnominal.GetNbinsX())
	halphaDown = r.TH1D("%s_alphaDown" %saveName, "%s_alphaDown" %saveName, hnominal.GetNbinsX(), 0, hnominal.GetNbinsX())
	hrelUncUp = rootfile.Get('relUnc_110')
	hrelUncDown = rootfile.Get('relUnc_111')
	for ibin in range(hnominal.GetNbinsX()):
		halphaUp.SetBinContent(ibin+1, hnominal.GetBinContent(ibin+1) *(1+hrelUncUp.GetBinContent(ibin+1)))
		halphaDown.SetBinContent(ibin+1, hnominal.GetBinContent(ibin+1) *(1+hrelUncDown.GetBinContent(ibin+1)))
	halphaUp.Write()
	halphaDown.Write()
	outfile.Close()

########################################################################################################################
pdfUpDown(ftt,'ttsig')
alphaUpDown(ftt,'ttsig')
alphaUpDown(ftt,'st')
#Remember the alpha uncertainty for single top is only saved for STt channels that I assumed it's the same for Wt channels
#This is the reason why I deal with the up/down templates by using the relative uncertainties

########################################################################################################################
#os.system("hadd -f %s/packroot/ch%s.root %s/packroot/ch%s_partial.root %s/packroot/skim_pdfct14_ttsig.root %s/packroot/skim_pdfct14_st.root" %(njets,njets,njets,njets,njets,njets))
os.system("hadd -f %s/packroot/ch%s.root %s/packroot/ch%s_partial.root %s/packroot/skim_pdfct14_ttsig.root %s/packroot/skim_alpha_ttsig.root %s/packroot/skim_alpha_st.root" %(njets,njets,njets,njets,njets,njets,njets))
os.system("cp %s/packroot/ch%s.root /afs/cern.ch/user/y/yduh/CMSSW_7_1_5/src/URStatTools/Input/%s" %(njets,njets,njets))

