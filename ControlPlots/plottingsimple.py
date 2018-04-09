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

DrawBckUseSB = False
DrawUnc = False
#DrawUnc = True if 'SB' not in sys.argv[3] else False
Splitt = True

datadir = sys.argv[1] + '/'
outfiles = sys.argv[2]

TTscale = ttpowheg
AL=''

DYfile = datadir+'DYJets.root'
Wfile = datadir+'WJets.root'
W1file = datadir+'W1Jets.root'
W2file = datadir+'W2Jets.root'
W3file = datadir+'W3Jets.root'
W4file = datadir+'W4Jets.root'
WWfile = datadir+'WW.root'
WZfile = datadir+'WZ.root'
Tfile = datadir+'Wt.root'
Tbarfile = datadir+'Wtbar.root'
STtopfile = datadir+'STt_top.root'
STtopbarfile = datadir+'STt_topbar.root'
TTfile = datadir+'tt_PowhegP8.root'

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
SBfile = '../WrapUp/'+sys.argv[3]+'/skimrootSBCR/skim_DATA_Tbck.root'

#bckList = [[DYfile,DYscale],[Wfile,Wscale],[WWfile,WWscale],[QCDMu50file,QCDMu50scale],[QCDMu80file,QCDMu80scale],[QCDMu120file,QCDMu120scale],[QCDMu170file,QCDMu170scale],[QCDMu300file,QCDMu300scale],[QCDMu470file,QCDMu470scale],[QCDMu600file,QCDMu600scale],[QCDMu800file,QCDMu800scale],[QCDMu1000file,QCDMu1000scale],[QCDMuInffile,QCDMuInfscale],[QCDEM50file,QCDEM50scale],[QCDEM80file,QCDEM80scale],[QCDEM120file,QCDEM120scale],[QCDEM170file,QCDEM170scale],[QCDEM300file,QCDEM300scale],[QCDEMInffile,QCDEMInfscale],[STtopbarfile,STtopbarscale],[STtopfile,STtopscale],[Tfile,WTscale],[Tbarfile,WTbarscale],[TTfile,TTscale]]
bckList = [[DYfile,DYscale],[W1file,W1scale],[W2file,W2scale],[W3file,W3scale],[W4file,W4scale],[QCDMu50file,QCDMu50scale],[QCDMu80file,QCDMu80scale],[QCDMu120file,QCDMu120scale],[QCDMu170file,QCDMu170scale],[QCDMu300file,QCDMu300scale],[QCDMu470file,QCDMu470scale],[QCDMu600file,QCDMu600scale],[QCDMu800file,QCDMu800scale],[QCDMu1000file,QCDMu1000scale],[QCDMuInffile,QCDMuInfscale],[QCDEM50file,QCDEM50scale],[QCDEM80file,QCDEM80scale],[QCDEM120file,QCDEM120scale],[QCDEM170file,QCDEM170scale],[QCDEM300file,QCDEM300scale],[QCDEMInffile,QCDEMInfscale],[WWfile,WWscale],[WZfile,WZscale],[STtopbarfile,STtopbarscale],[STtopfile,STtopscale],[Tfile,WTscale],[Tbarfile,WTbarscale],[TTfile,TTscale]]

plot = {}
plotnames = []

def DrawPlotnames(plotnames):
	for p, b, pro, rmin, rmax in plotnames:
		print p
		plot[p] = plotTogether()
		plot[p].addDAplot(Datafile, histarg +p, 'Data', 1, projection = pro)

		if DrawBckUseSB:
			plot[p].addMCplot(SBfile, histarg +p, 'V+jets QCD', 1, ROOT.kGreen+2, projection = pro)
		else:
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
			#plot[p].addMCplot(Wfile, histarg +p, '', Wscale, ROOT.kGreen-2, projection = pro)
			#plot[p].addMCplot(W1file, histarg +p, '', W1scale, ROOT.kGreen+2, projection = pro)#Green-4
			plot[p].addMCplot(W2file, histarg +p, '', W2scale, ROOT.kGreen+2, projection = pro)#Green-8
			plot[p].addMCplot(W3file, histarg +p, '', W3scale, ROOT.kGreen+2, projection = pro)#Green-10
			plot[p].addMCplot(W4file, histarg +p, '', W4scale, ROOT.kGreen+2, projection = pro)#Green+3

		plot[p].addMCplot(STtopbarfile, histarg +p, 'single top', STtopbarscale, ROOT.kOrange, projection = pro)
		plot[p].addMCplot(STtopfile, histarg +p, '', STtopscale, ROOT.kOrange, projection = pro)
		plot[p].addMCplot(Tfile, histarg +p, '', WTscale, ROOT.kOrange, projection = pro)
		plot[p].addMCplot(Tbarfile, histarg +p, '', WTbarscale, ROOT.kOrange, projection = pro)
		plot[p].addMCplot(WWfile, histarg +p, 'WW/WZ', WWscale, ROOT.kBlack, projection = pro)
		plot[p].addMCplot(WZfile, histarg +p, '', WZscale, ROOT.kBlack, projection = pro)

		if Splitt:
			plot[p].addMCplot(TTfile, histarg_ttother +p, 't#bar{t} bck', TTscale, ROOT.kMagenta-8, projection = pro)
			plot[p].addMCplot(TTfile, histarg_ttsemi +p, 't#bar{t} not reco', TTscale, ROOT.kBlue-5, projection = pro)
			plot[p].addMCplot(TTfile, histarg_ttwrong +p, 't#bar{t} wrong reco', TTscale, ROOT.kBlue-9, projection = pro)
			plot[p].addMCplot(TTfile, histarg_ttright +p, 't#bar{t} right reco', TTscale, ROOT.kRed-4, projection = pro)
		else:
			plot[p].addMCplot(TTfile, histarg +p, 't#bar{t} '+AL, TTscale, ROOT.kRed-3, projection = pro)


		if DrawUnc:
			if 'SB' in sys.argv[3]:
				csvdowndir = datadir+'../comp2/'
				csvupdir = datadir+'../comp1/'
				for cop in bckList:
					filename = cop[0].split('/')[-1]
					#plot[p].addUncerHist(cop[0], cop[1],cop[1],cop[1], csvdowndir+filename, csvupdir+filename, histarg +p, 1, projection = pro, Norm=True)
				#plot[p].addUncerVal(totsys[sys.argv[3]])

			else:
				for cop in [[TTfile,TTscale],[STtopfile,STtopscale],[STtopbarfile,STtopbarscale],[Tfile,WTscale],[Tbarfile,WTbarscale]]:
					filename = cop[0].split('/')[-1]
					for err in errList:
						plot[p].addUncerHist(cop[0], cop[1],cop[1],cop[1], datadir+'unc/%s/%s'%(err[0],filename), datadir+'unc/%s/%s'%(err[1],filename), histarg +p, 1, projection = pro)

				for cop in [[TTfile,TTscale]]:
					#plot[p].addUncerHist(cop[0], cop[1],ttpowheg_erdon,cop[1], datadir+'unc/MCs/tt_erdon_PowhegP8.root', cop[0], histarg +p, 2, projection = pro)
					plot[p].addUncerHist(cop[0], cop[1],ttpowheg_hddown,ttpowheg_hdup, datadir+'unc/MCs/tt_hddown_PowhegP8.root', datadir+'unc/MCs/tt_hdup_PowhegP8.root', histarg +p, 1, projection = pro)
					plot[p].addUncerHist(cop[0], cop[1],ttpowheg_isrdown,ttpowheg_isrup, datadir+'unc/MCs/tt_isrdown_PowhegP8.root', datadir+'unc/MCs/tt_isrup_PowhegP8.root', histarg +p, 1/sqrt(2), projection = pro)
					plot[p].addUncerHist(cop[0], cop[1],ttpowheg_fsrdown,ttpowheg_fsrup, datadir+'unc/MCs/tt_fsrdown_PowhegP8.root', datadir+'unc/MCs/tt_fsrup_PowhegP8.root', histarg +p, 1/sqrt(2), projection = pro)
					plot[p].addUncerHist(cop[0], cop[1],cop[1]*rsfsdw[sys.argv[3]],cop[1]*rsfsup[sys.argv[3]], datadir+'unc/rsfsSSDown/'+cop[0].split('/')[-1], datadir+'unc/rsfsSSUp/'+cop[0].split('/')[-1], histarg +p, 1, projection = pro)
					print rsfsdw[sys.argv[3]], rsfsup[sys.argv[3]]
					plot[p].addUncerHist(cop[0], cop[1],ttpowheg_mtdown3,ttpowheg_mtup3, datadir+'unc/MCs/tt_mtop1695_PowhegP8.root', datadir+'unc/MCs/tt_mtop1755_PowhegP8.root', histarg +p, 1/3., projection = pro)

				if 'njets' in p:
					plot[p].addUncerValBins(totsys[sys.argv[3]])
				else:
					print totsys[sys.argv[3]]
					plot[p].addUncerVal(totsys[sys.argv[3]])


			plot[p].setUncTitle('Total unc.')


		pbw = True
		xl = []

		if 'njets' in p:
			pbw = False
			xl = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
			can = plot[p].drawAddWithRatio('hist', rebin=b, title='35.8 fb^{-1} (13 TeV)', ratio=True, rangemin=rmin, rangemax=rmax, printbinwidth=pbw, xlabels=xl)
		elif 'massnutest' in p:
			can = plot[p].drawAddWithRatio('hist', rebin=b, title='35.8 fb^{-1} (13 TeV)', ratio=True, rangemin=rmin, rangemax=rmax, printbinwidth=pbw, xtitle='-ln(#lambda_{4})')
		elif 'MET' in p:
			can = plot[p].drawAddWithRatio('hist', rebin=b, title='35.8 fb^{-1} (13 TeV)', ratio=True, rangemin=rmin, rangemax=rmax, printbinwidth=pbw, xtitle='MET')
		else:
			can = plot[p].drawAddWithRatio('hist', rebin=b, title='35.8 fb^{-1} (13 TeV)', ratio=True, rangemin=rmin, rangemax=rmax, printbinwidth=pbw, xlabels=xl)

		#if(p == "delY"):
		#	plot[p].printLatexYieldTable('totyield_table.tex')

		can.SaveAs(outfiles+'/plot_'+p+'.png')
		can.SaveAs(outfiles+'/plot_'+p+'.pdf')

	return





if '3jup' in sys.argv[3]:
	if Splitt:
		histarg = 'YUKAWA_RECO/yukawa_'
		histarg_ttright = 'YUKAWA_RECO_right/yukawa_'
		histarg_ttwrong = 'YUKAWA_RECO_wrong/yukawa_'
		histarg_ttsemi = 'YUKAWA_RECO_semi/yukawa_'
		histarg_ttother = 'YUKAWA_RECO_other/yukawa_'
		plotnames = [['njets', 1, '', 3, 11]]
		DrawPlotnames(plotnames)
	else:
		histarg = 'RECO/reco_'
		plotnames.append(['NumVertices', 1, '', 0, 50])
		plotnames.append(['NumVerticesWeighted', 1, '', 0, 50])
		DrawPlotnames(plotnames)

elif '3j' in sys.argv[3]:
	if Splitt:
		histarg = '3j_RECO/3j_'
		histarg_ttright = '3j_RECO_right/3j_'
		histarg_ttwrong = '3j_RECO_wrong/3j_'
		histarg_ttsemi = '3j_RECO_semi/3j_'
		histarg_ttother = '3j_RECO_other/3j_'
		if 'SB' not in sys.argv[3]:
			plotnames.append(['tlep_pt', 20, '', 0, 5000])
			plotnames.append(['thad_pt', 20, '', 0, 5000])
			plotnames.append(['tlep_y', 10, '', 0, 2.4])
			plotnames.append(['thad_y', 10, '', 0, 2.4])
			plotnames.append(['MET', 5, '', 0, 300])
			plotnames.append(['lep_eta', 40, '', 0, 0])
			plotnames.append(['tt_pt', 10, '', 0, 500])
			plotnames.append(['tt_y', 5, '', 0, 2.5])
		else:
			plotnames.append(['Mtt', 40, '', 200, 1500])
			plotnames.append(['delY', 50, '', -4, 4])
		DrawPlotnames(plotnames)
	else:
		histarg = 'RECO/reco_'
		plotnames.append(['btag_high', 5, '', 0, 1])
		plotnames.append(['btag_low', 5, '', 0, 1])
		#histarg = '3j_RECO/3j_'
		#plotnames.append(['mu_pt', 1, '', 20, 100])
		#plotnames.append(['el_pt', 1, '', 20, 100])
		DrawPlotnames(plotnames)


elif '4jup' in sys.argv[3]:
	histarg = 'RECO/all_'
	histarg_ttright = 'TRUTH/right_'
	histarg_ttwrong = 'TRUTH/wrong_'
	histarg_ttsemi = 'TRUTH/semi_'
	histarg_ttother = 'TRUTH/other_'
	plotnames.append(['massnutest', 2, 'test', 10, 22])
	DrawPlotnames(plotnames)

elif '4j' in sys.argv[3] or '5j' in sys.argv[3] or '6j' in sys.argv[3]:
	if Splitt:
		histarg = 'YUKAWA_RECO/yukawa_'
		histarg_ttright = 'YUKAWA_RECO_right/yukawa_'
		histarg_ttwrong = 'YUKAWA_RECO_wrong/yukawa_'
		histarg_ttsemi = 'YUKAWA_RECO_semi/yukawa_'
		histarg_ttother = 'YUKAWA_RECO_other/yukawa_'
		if 'SB' not in sys.argv[3]:
			plotnames.append(['tlep_pt', 20, '', 0, 5000])
			plotnames.append(['thad_pt', 20, '', 0, 5000])
			plotnames.append(['tlep_y', 10, '', 0, 2.4])
			plotnames.append(['thad_y', 10, '', 0, 2.4])
			histarg = 'RECO/all_'
			histarg_ttright = 'TRUTH/right_'
			histarg_ttwrong = 'TRUTH/wrong_'
			histarg_ttsemi = 'TRUTH/semi_'
			histarg_ttother = 'TRUTH/other_'
			plotnames.append(['lep_eta', 40, '', 0, 0])
			plotnames.append(['MET', 5, '', 0, 300])
			plotnames.append(['tt_pt', 10, '', 0, 500])
			plotnames.append(['tt_y', 5, '', 0, 2.5])
		else:
			plotnames.append(['Mtt', 40, '', 200, 1500])
			plotnames.append(['delY', 50, '', -4, 4])
		DrawPlotnames(plotnames)
	else:
		histarg = 'RECO/reco_'
		plotnames.append(['btag_high', 5, '', 0, 1])
		plotnames.append(['btag_low', 5, '', 0, 1])
		#histarg = 'YUKAWA_RECO/yukawa_'
		#plotnames.append(['mu_pt', 1, '', 20, 100])
		DrawPlotnames(plotnames)


'''
	histarg = 'TRUTH/'
	plotnames.append(['bjet_pt', 2, '', 30, 350])
	plotnames.append(['bjets_pthad_ptlep', 25, 'Y', 25, 350])
	plotnames.append(['bjet_eta', 5, '', -2.4, 2.4])
	plotnames.append(['wjet_pt', 1, '', 25, 200])
	plotnames.append(['wjet_eta', 5, '', -2.4, 2.4])
	plotnames.append(['lep_pt', 10, '', 30, 200])
	plotnames.append(['nu_pt', 20, '', 0, 300])
	plotnames.append(['Mt_W', 5, '', 0, 300])
	plotnames.append(['thard_pt', 20, '', 0, 5000])
	plotnames.append(['tsoft_pt', 20, '', 0, 5000])
	plotnames.append(['tt_M', 40, '', 200, 1500])
	plotnames.append(['Whad_M_thad_M', 5, 'Y', 50, 300])
	plotnames.append(['truth_Jetstt_JetsAll', 1, 'Y', 3, 10])
'''



