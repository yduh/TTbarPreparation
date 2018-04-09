#usage: python plottingsimple.py MCCENTRAL3j PLOTSCONTROL3j 3j
#!/usr/bin/python2.7
import math, sys, re, sys
from math import sqrt
from plotTogether import *
from SCALE import *
from SysBook import *
import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetOptTitle(ROOT.kFALSE)

DrawUnc = True

datadir = sys.argv[1] + '/'
outfiles = sys.argv[2]

TTscale = ttpowheg
AL=''

DYfile = datadir+'DYJets.root'
Wfile = datadir+'WJets.root'
QCDMu15file = datadir+'QCDMu15.root'
QCDMu30file = datadir+'QCDMu30.root'
QCDMu50file = datadir+'QCDMu50.root'
QCDMu80file = datadir+'QCDMu80.root'
QCDMu120file = datadir+'QCDMu120.root'
QCDMu170file = datadir+'QCDMu170.root'
QCDMu300file = datadir+'QCDMu300.root'
QCDMu470file = datadir+'QCDMu470.root'
QCDMu600file = datadir+'QCDMu600.root'
QCDMu800file = datadir+'QCDMu800.root'
QCDMu1000file = datadir+'QCDMu1000.root'
QCDMuInffile = datadir+'QCDMuInf.root'
QCDEM50file = datadir+'QCDEM50.root'
QCDEM80file = datadir+'QCDEM80.root'
QCDEM120file = datadir+'QCDEM120.root'
QCDEM170file = datadir+'QCDEM170.root'
QCDEM300file = datadir+'QCDEM300.root'
QCDEMInffile = datadir+'QCDEMInf.root'
Datafile = datadir+'DATA.root'
SBfile = 'bck_template/MCCENTRAL'+sys.argv[3]+'/DATA.root'
SBUpfile = 'bck_template/MCCENTRAL'+sys.argv[3]+'/../comp1/DATA.root'
SBDownfile = 'bck_template/MCCENTRAL'+sys.argv[3]+'/../comp2/DATA.root'

plot = {}
plotnames = []

def DrawPlotnames(plotnames):
	for p, b, pro, rmin, rmax in plotnames:
		f = TFile(SBfile,'READ')
		fDown = TFile(SBDownfile,'READ')
		fUp = TFile(SBUpfile,'READ')
		Bckscale = evt[sys.argv[3]][-1]/f.Get(histarg+p).Integral()
		BckDownscale = evt[sys.argv[3]][-1]/fDown.Get(histarg+p).Integral()
		BckUpscale = evt[sys.argv[3]][-1]/fUp.Get(histarg+p).Integral()
		print p
		plot[p] = plotTogether()
		plot[p].addDAplot(SBfile, histarg +p, 'Data SB', Bckscale, projection = pro)
		plot[p].addOtherplot(SBUpfile, histarg +p, 'Data 0.4<CSV<0.7', BckUpscale, ROOT.kRed, projection = pro)
		plot[p].addOtherplot(SBDownfile, histarg +p, 'Data CSV<0.4', BckDownscale, ROOT.kRed, 2, projection = pro)

		plot[p].addMCplot(QCDMu50file, histarg +p, 'QCD', QCDMu50scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu80file, histarg +p, '', QCDMu80scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu120file, histarg +p, '', QCDMu120scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu170file, histarg +p, '', QCDMu170scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu300file, histarg +p, '', QCDMu300scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu470file, histarg +p, '', QCDMu470scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu600file, histarg +p, '', QCDMu600scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu800file, histarg +p, '', QCDMu800scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMu1000file, histarg +p, '', QCDMu1000scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDMuInffile, histarg +p, '', QCDMuInfscale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDEM50file, histarg +p, '', QCDEM50scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDEM80file, histarg +p, '', QCDEM80scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDEM120file, histarg +p, '', QCDEM120scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDEM170file, histarg +p, '', QCDEM170scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDEM300file, histarg +p, '', QCDEM300scale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(QCDEMInffile, histarg +p, '', QCDEMInfscale, ROOT.kBlue, projection = pro)
		plot[p].addMCplot(DYfile, histarg +p, 'V+jets', DYscale, ROOT.kGreen+2, projection = pro)
		plot[p].addMCplot(Wfile, histarg +p, '', Wscale, ROOT.kGreen-2, projection = pro)

		if DrawUnc:
			plot[p].addUncerVal(totsys[sys.argv[3]+'SB'])

			plot[p].setUncTitle('Total norm. unc.')


		pbw = True
		xl = []

		can = plot[p].drawAddWithRatio('hist', rebin=b, title='35.8 fb^{-1} (13 TeV)', ratio=True, rangemin=rmin, rangemax=rmax, printbinwidth=pbw, xlabels=xl)

		#if(p == "delY"):
		#	plot[p].printLatexYieldTable('totyield_table.tex')

		can.SaveAs(outfiles+'/plot_'+p+'.png')
		can.SaveAs(outfiles+'/plot_'+p+'.pdf')

	return




if '3j' in sys.argv[3]:
	histarg = '3j_RECO/3j_'
	histarg_ttright = '3j_RECO_right/3j_'
	histarg_ttwrong = '3j_RECO_wrong/3j_'
	histarg_ttsemi = '3j_RECO_semi/3j_'
	histarg_ttother = '3j_RECO_other/3j_'
	plotnames.append(['Mtt', 50, '', 200, 1500])
	plotnames.append(['delY', 60, '', -4, 4])
	DrawPlotnames(plotnames)
else:
	histarg = 'YUKAWA_RECO/yukawa_'
	histarg_ttright = 'YUKAWA_RECO_right/yukawa_'
	histarg_ttwrong = 'YUKAWA_RECO_wrong/yukawa_'
	histarg_ttsemi = 'YUKAWA_RECO_semi/yukawa_'
	histarg_ttother = 'YUKAWA_RECO_other/yukawa_'
	plotnames.append(['Mtt', 50, '', 200, 1500])
	plotnames.append(['delY', 55, '', -4, 4])
	DrawPlotnames(plotnames)


