import ROOT as r
import sys
from math import sqrt

njets = sys.argv[1]

def UnweightEvents(folder):
	f_Wj = r.TFile('../../%s/%s/skim_WnJets.root' %(njets, folder))
	f_DY = r.TFile('../../%s/%s/skim_DYJets.root' %(njets, folder))
	f_QCD = r.TFile('../../%s/%s/skim_QCD.root' %(njets, folder))
	f_DATA = r.TFile('../../%s/%s/skim_DATA.root' %(njets, folder))
	f_tt = r.TFile('../../%s/%s/skim_tt_PowhegP8_noEW.root' %(njets, folder))
	f_st = r.TFile('../../%s/%s/skim_t.root' %(njets, folder))

	h_Wj = f_Wj.Get('mtt_RECO')
	h_DY = f_DY.Get('mtt_RECO')
	h_QCD = f_QCD.Get('mtt_RECO')
	h_DATA = f_DATA.Get('mtt_RECO')
	h_tt = f_tt.Get('mtt_RECO')
	h_st = f_st.Get('mtt_RECO')

	error_Wj = r.Double(0)
	error_DY = r.Double(0)
	error_QCD = r.Double(0)
	h_Wj.IntegralAndError(1, h_Wj.GetXaxis().GetNbins(), error_Wj, "")
	h_DY.IntegralAndError(1, h_DY.GetXaxis().GetNbins(), error_DY, "")
	h_QCD.IntegralAndError(1, h_QCD.GetXaxis().GetNbins(), error_QCD, "")
	Nunweight_Wj = (1/(error_Wj/h_Wj.Integral()))**2
	Nunweight_DY = (1/(error_DY/h_DY.Integral()))**2
	Nunweight_QCD = (1/(error_QCD/h_QCD.Integral()))**2

	print "Signal region:" if folder == 'skimroot' else "Control region:"
	print "unweight W+jets = ", Nunweight_Wj
	print "unweight DY = ", Nunweight_DY
	print "unweight QCD = ", Nunweight_QCD
	print "weight W+jets = ", h_Wj.Integral(), ",", h_Wj.Integral()/(h_Wj.Integral()+h_QCD.Integral()+h_DY.Integral())*100, "%"
	print "weight DY = ", h_DY.Integral(), ",", h_DY.Integral()/(h_Wj.Integral()+h_QCD.Integral()+h_DY.Integral())*100, "%"
	print "weight QCD = ", h_QCD.Integral(), ",", h_QCD.Integral()/(h_Wj.Integral()+h_QCD.Integral()+h_DY.Integral())*100, "%"
	print "data = ", h_DATA.Integral()
	print "data exclude others = ", h_DATA.Integral() - h_tt.Integral() - h_st.Integral(), ", Vjets + QCD MC = ", h_Wj.Integral() + h_DY.Integral() + h_QCD.Integral()


UnweightEvents('skimroot')
UnweightEvents('skimrootSB')

