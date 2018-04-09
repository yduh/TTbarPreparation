#!/usr/bin/python2.7
import math, sys, re, sys
from plotUnc import *
import ROOT
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetOptTitle(ROOT.kFALSE)

channel = "3j"

TTfile = "../"+channel+"/packroot/ch"+channel+".root"
outfiles = "./shapeunc"

AL=''

syslist = ['PS', 'hadro', 'NLO']
c = ROOT.TCanvas("c", "c", 1200, 1200)
c.Divide(1, 2)
#hcentral = TTfile.Get("ttsig")
#hup = TTfile.Get("PSUp")
#hdown = TTfile.Get("PSDown")

#hcentral.Draw()
#hup.Draw("same")
#hdown.Draw("same")


plot = {}
plotnames = []
plotnames.append(['ttsig', 'hadro', '', 0, 62])

def DrawPlotnames(plotnames):
	for p, sys, pro, rmin, rmax in plotnames:
		#c.Print(outfiles+"/plot_"+sys+".png[")
		print p
		plot[p] = plotUnc()

		plot[p].addCentralplot(TTfile, 'ttsig', 'central value', 1, ROOT.kBlack, projection = pro)
		plot[p].addOtherplot(TTfile, sys +'Up', sys+'+1 #sigma', 1, ROOT.kRed, projection = pro)
		plot[p].addOtherplot(TTfile, sys +'Down', sys+'-1 #sigma', 1, ROOT.kBlue, projection = pro)
		#plot[p].addTplotUp(TTfile, sys +'Up', sys+'+1 #sigma', 1, ROOT.kRed, projection = pro)
		#plot[p].addTplotDown(TTfile, sys +'Down', sys+'-1 #sigma', 1, ROOT.kBlue, projection = pro)
		#plot[p].addOtherplot(TTfile, sys +'Down', sys+'-1 #sigma', 1, ROOT.kBlue, projection = pro)

		pbw = True
		xl = []
		can = plot[p].drawAddWithRelUnc('histsame', rebin=1, title='2.3 fb^{-1} (13 TeV)', ratio=True, rangemin=rmin, rangemax=rmax, printbinwidth=pbw)


		can.SaveAs(outfiles+'/plot_'+sys+'.png')
		can.SaveAs(outfiles+'/plot_'+sys+'.pdf')

		#c.Print(outfiles+"/plot_"+sys+".png")

	return

DrawPlotnames(plotnames)



