#!/usr/bin/python2.7
import math, sys, re
from plotTogether import *
from SCALE import *

datadir = 'MCCENTRAL3j/'
DYfile = datadir+'DYJets.root'
Wfile = datadir+'WJets.root'
Tfile = datadir+'Wt.root'
Tbarfile = datadir+'Wtbar.root'
STtfile = datadir+'STt.root'
TTfile = datadir+'tt_PowhegP8.root'
TTscale = ttpowheg
#TTfile = datadir+'tt_PowhegP6.root'
#TTscale = ttpowhegp6scale
#TTfile = datadir+'tt_PowhegHpp.root'
#TTscale = ttpowheghppscale
#TTfile = datadir+'tt_scaleup_PowhegP8.root'
#TTscale = ttpowheg_scaleupscale
#TTfile = datadir+'tt_scaledown_PowhegP8.root'
#TTscale = ttpowheg_scaledownscale
#TTfile = datadir+'tt_aMCatNLO.root'
#TTscale = ttamcatnloscale
AL=''
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

Datafile = 'MCCENTRAL3j/DATA.root'
#Datafile = 'MCS/DATA.root'

plot = {}
plotnames = []
plotnames.append(['dbeta', 5, '', 0, 0, False])
plotnames.append(['bjet_pt', 2, '', 30, 350, False])
plotnames.append(['bjets_pthad_ptlep', 25, 'Y', 25, 350, False])
plotnames.append(['bjet_eta', 5, '', -2.4, 2.4, False])
plotnames.append(['wjet_pt', 1, '', 25, 200, False])
plotnames.append(['wjet_eta', 5, '', -2.4, 2.4, False])
plotnames.append(['lep_pt', 10, '', 30, 200, False])
plotnames.append(['lep_eta', 20, '', 0, 0, False])
plotnames.append(['nu_pt', 20, '', 0, 300, False])
plotnames.append(['MET', 5, '', 0, 300, False])
plotnames.append(['Mt_W', 5, '', 0, 300, False])
plotnames.append(['thad_pt', 20, '', 0, 5000, True])
plotnames.append(['thard_pt', 20, '', 0, 5000, True])
plotnames.append(['tsoft_pt', 20, '', 0, 5000, True])
plotnames.append(['thad_y', 10, '', 0, 2.5, False])
plotnames.append(['tlep_pt', 20, '', 0, 5000, True])
plotnames.append(['tlep_y', 10, '', 0, 2.5, False])
plotnames.append(['tt_M', 40, '', 200, 1500, True])
plotnames.append(['tt_pt', 10, '', 0, 500, True])
plotnames.append(['tt_y', 5, '', 0, 2.5, False])
plotnames.append(['njets', 1, '', 0, 7, False])
plotnames.append(['Whad_M_thad_M', 5, 'Y', 50, 300, False])

qcdcolor = ROOT.kBlue

for p, b, pro, rmin, rmax, logy in plotnames:
	print p
	plot[p] = plotTogether()
	plot[p].addDAplot(Datafile, 'RECO/all_'+p, 'Data', projection = pro)
	plot[p].addMCplot(QCDMu50file, 'RECO/all_'+p, 'Multijet', QCDMu50scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu80file, 'RECO/all_'+p, '', QCDMu80scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu120file, 'RECO/all_'+p, '', QCDMu120scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu170file, 'RECO/all_'+p, '', QCDMu170scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu300file, 'RECO/all_'+p, '', QCDMu300scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu470file, 'RECO/all_'+p, '', QCDMu470scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu600file, 'RECO/all_'+p, '', QCDMu600scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu800file, 'RECO/all_'+p, '', QCDMu800scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu1000file, 'RECO/all_'+p, '', QCDMu1000scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMuInffile, 'RECO/all_'+p, '', QCDMuInfscale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM50file, 'RECO/all_'+p, '', QCDEM50scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM80file, 'RECO/all_'+p, '', QCDEM80scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM120file, 'RECO/all_'+p, '', QCDEM120scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM170file, 'RECO/all_'+p, '', QCDEM170scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM300file, 'RECO/all_'+p, '', QCDEM300scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEMInffile, 'RECO/all_'+p, '', QCDEMInfscale, qcdcolor, projection = pro)
	plot[p].addMCplot(DYfile, 'RECO/all_'+p, 'W/DY+jets', DYscale, ROOT.kGreen+2, projection = pro)
	plot[p].addMCplot(Wfile, 'RECO/all_'+p, '', Wscale, ROOT.kGreen+2, projection = pro)
	plot[p].addMCplot(STtfile, 'RECO/all_'+p, 'Single t', STtscale, ROOT.kOrange, projection = pro)
	plot[p].addMCplot(Tfile, 'RECO/all_'+p, '', WTscale, ROOT.kOrange, projection = pro)
	plot[p].addMCplot(Tbarfile, 'RECO/all_'+p, '', WTbarscale, ROOT.kOrange, projection = pro)
	#plot[p].addMCplot(TTfile, 'TRUTH/other_'+p, 't#bar{t} '+AL, TTscale, ROOT.kRed-3, projection = pro)
	plot[p].addMCplot(TTfile, 'TRUTH/other_'+p, 't#bar{t} background', TTscale, ROOT.kRed-8, projection = pro)
	plot[p].addMCplot(TTfile, 'TRUTH/semi_'+p, 't#bar{t} signal', TTscale, ROOT.kRed-3, projection = pro)
	#plot[p].addMCplot(TTfile, 'TRUTH/semi_'+p, '', TTscale, ROOT.kRed-3, projection = pro)
	plot[p].addMCplot(TTfile, 'TRUTH/wrong_'+p, '', TTscale, ROOT.kRed-3, projection = pro)
	plot[p].addMCplot(TTfile, 'TRUTH/right_'+p, '', TTscale, ROOT.kRed-3, projection = pro)
	plot[p].addUncerHist(TTfile, 'MCjetm1sig/tt_PowhegP8.root', 'MCjetp1sig/tt_PowhegP8.root', 'RECO/all_'+p, projection = pro)
	plot[p].addUncerHist(TTfile, 'MCbtagup/tt_PowhegP8.root', 'MCbtagdown/tt_PowhegP8.root', 'RECO/all_'+p, projection = pro)
	plot[p].addUncerVal(float(info['leptonerr']))
	plot[p].addUncerVal(float(info['lumierr']))
	pbw = True
	xl = []
	if 'njet' in p:
		pbw = False
		xl = ['0', '1', '2', '3', '4', '5', '>=6']
	can = plot[p].drawAddWithRatio('hist', rebin = b, title = '2.3 fb^{-1} (13 TeV)', ratio = True, rangemin = rmin, rangemax = rmax, printbinwidth = pbw, xlabels = xl, logy = logy)
	if (p == "Whad_M_thad_M"):
		plot[p].printLatexYieldTable('totyield_table.tex')
	can.SaveAs('PLOTSCONTROL/plot_'+p+'.png')
	can.SaveAs('PLOTSCONTROL/plot_'+p+'.pdf')


plotnames = []
plotnames.append(['RECO/reco_counter', 1, '', 1, 4, '', True, ['', '1 lepton', '4 jets', '2 b jets', 'algo/#lambda_{m}-cut']])
plotnames.append(['RECO/reco_btag_high', 4, '', 0, 0, 'highest b-tag discriminant', False, []])
plotnames.append(['RECO/reco_btag_low', 4, '', 0, 0, '2nd highest b-tag discriminant', False, []])
plotnames.append(['RECO/reco_bjetmulti', 1, '', 0, 6, '', False, []])
plotnames.append(['RECO/reco_jetmulti', 1, '', 0, 10, '', False, []])
plotnames.append(['RECO/reco_bjetmultiW', 1, '', 0, 6, '', False, []])
#plotnames.append(['RECO/all_testb_thadpt', 5, 'X', 0, 100, '', False, []])
#plotnames.append(['RECO/reco_Mt_W', 20, '', 0, 0, '', False, []])
plotnames.append(['RECO/all_DRminW', 5, '', 0, 6, '', False, []])
plotnames.append(['RECO/all_DRminbl', 5, '', 0, 6, '', False, []])
plotnames.append(['RECO/all_DRminbh', 5, '', 0, 6, '', False, []])
plotnames.append(['RECO/all_DRminadd', 5, '', 0, 6, '', False, []])
plotnames.append(['RECO/all_addjet1_pt', 5, '', 0, 250, '', False, []])
plotnames.append(['RECO/all_addjet2_pt', 5, '', 0, 250, '', False, []])
plotnames.append(['RECO/all_addjet3_pt', 5, '', 0, 250, '', False, []])
plotnames.append(['RECO/all_addjet4_pt', 5, '', 0, 250, '', False, []])
#plotnames.append(['RECO/reco_MuIsolation', 2, '', 0, 0.4, '', False, []])
#plotnames.append(['RECO/reco_ElIsolation', 2, '', 0, 0.4, '', False, []])
plotnames.append(['RECO/reco_NumVertices', 1, '', 0, 50, '', False, []])
plotnames.append(['RECO/reco_NumVerticesWeighted', 1, '', 0, 50, '', False, []])
#plotnames.append(['RECO/all_Mt_W', 10, '', 0, 200, '', False, []])
#plotnames.append(['RECO/all_METunc', 4, 'X', 0, 0.5, '', False, []])
plotnames.append(['RECO/all_Whad_M_thad_M', 5, 'X', 0, 150, '', False, []])
plotnames.append(['TRUTH/response/njets_thadpt_all', 1, '', 0, 0, '4 n-jets #times 9 p_{T}(t_{h})', False, []])
plotnames.append(['TRUTH/response/njets_ttpt_all', 1, '', 0, 0, '4 n-jets #times 5 p_{T}(t#bar{t})', False, []])
plotnames.append(['TRUTH/response/thady_thadpt_all', 1, '', 0, 0, '4 |y(t_{h})| #times 9 p_{T}(t_{h})', False, []])
plotnames.append(['TRUTH/response/ttm_tty_all', 1, '', 0, 0, '4 m(t#bar{t}) #times 6 y(t#bar{t})', False, []])
plotnames.append(['TRUTH/response/ttpt_ttm_all', 1, '', 0, 0, '4 p_{T}(t#bar{t}) #times 8 M(t#bar{t})', False, []])
#plotnames.append(['RECO/all_njets', 1 , '', 0, 0, '', False, []])
for p, b, pro, rmin, rmax, x_title, logy, xlabels in plotnames:
	print p
	plot[p] = plotTogether()
	plot[p].addDAplot(Datafile, p, 'Data', projection = pro)
	plot[p].addMCplot(QCDMu50file, p, 'Multijet', QCDMu50scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu80file, p, '', QCDMu80scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu120file, p, '', QCDMu120scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu170file, p, '', QCDMu170scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu300file, p, '', QCDMu300scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu470file, p, '', QCDMu470scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu600file, p, '', QCDMu600scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu800file, p, '', QCDMu800scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMu1000file, p, '', QCDMu1000scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDMuInffile, p, '', QCDMuInfscale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM50file, p, '', QCDEM50scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM80file, p, '', QCDEM80scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM120file, p, '', QCDEM120scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM170file, p, '', QCDEM170scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEM300file, p, '', QCDEM300scale, qcdcolor, projection = pro)
	plot[p].addMCplot(QCDEMInffile, p, '', QCDEMInfscale, qcdcolor, projection = pro)
	plot[p].addMCplot(DYfile, p, 'W/DY+jets', DYscale, ROOT.kGreen+2, projection = pro)
	plot[p].addMCplot(Wfile, p, '', Wscale, ROOT.kGreen+2, projection = pro)
	plot[p].addMCplot(STtfile, p, 'Single t', STtscale, ROOT.kOrange, projection = pro)
	plot[p].addMCplot(Tfile, p, '', WTscale, ROOT.kOrange, projection = pro)
	plot[p].addMCplot(Tbarfile, p, '', WTbarscale, ROOT.kOrange, projection = pro)
	plot[p].addMCplot(TTfile, p, 't#bar{t}'+AL, TTscale, ROOT.kRed-3, projection = pro)
	plot[p].addUncerHist(TTfile, 'MCjetm1sig/tt_PowhegP8.root', 'MCjetp1sig/tt_PowhegP8.root', p, projection = pro)
	plot[p].addUncerHist(TTfile, 'MCbtagup/tt_PowhegP8.root', 'MCbtagdown/tt_PowhegP8.root', p, projection = pro)
	plot[p].addUncerVal(float(info['leptonerr']))
	plot[p].addUncerVal(float(info['lumierr']))
	can = plot[p].drawAddWithRatio('hist', rebin = b, title = '2.3 fb^{-1} (13 TeV)', ratio = True, rangemin = rmin, rangemax = rmax, xtitle = x_title, logy = logy, xlabels = xlabels)
	can.SaveAs('PLOTSCONTROL/plot_'+p.split('/')[-1]+'.png')
	can.SaveAs('PLOTSCONTROL/plot_'+p.split('/')[-1]+'.pdf')

