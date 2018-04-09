#!/usr/bin/python
from ROOT import gStyle, gPad, TCanvas, TPad, TGraph
import ROOT as r
import numpy as np
from array import array
from Utils.rootHistTools import SetPalette

palette = SetPalette()
palette('kBird')

def cmstext():
	xpos = r.gPad.GetLeftMargin()
	ypos = 1.-r.gPad.GetTopMargin()

	lx = r.TLatex(0., 0., 'Z')
	lx.SetNDC(True)
	lx.SetTextFont(62)
	lx.SetTextSize(0.05)
	lx.SetTextAlign(13)
	lx.DrawLatex(xpos+0.04, ypos-0.03, 'CMS')

	lx2 = r.TLatex(0., 0., 'Z')
	lx2.SetNDC(True)
	lx2.SetTextFont(53)
	lx2.SetTextSize(20)
	lx2.SetTextAlign(13)
	#lx2.DrawLatex(xpos+0.04, ypos-0.08, '#it{Preliminary}')
	lx2.DrawLatex(xpos+0.04, ypos-0.08, 'Simulation')

	lx3 = r.TLatex(0., 0., 'Z')
	lx3.SetNDC(True)
	lx3.SetTextFont(43)
	lx3.SetTextSize(23)
	lx3.SetTextAlign(31)
	lx3.DrawLatex(xpos+0.78, ypos+0.015,'35.8 fb^{-1}(13 TeV)')
	lx3.Draw()

	lx4 = r.TLatex(0., 0., 'Z')
	lx4.SetNDC(True)
	lx4.SetTextFont(63)
	lx4.SetTextSize(25)
	lx4.SetTextAlign(13)
	lx4.DrawLatex(0.45, ypos-0.03,'e/#mu+jets')




f = r.TFile("/afs/cern.ch/user/y/yduh/work/lpcresults/4jup/noEW/tt_PowhegP8.root") #3j

h = f.Get("TRUTH/right_thad_M_Whad_M")

#h.Rebin2D(2, 2)
h.Scale(1/h.Integral('width'))
h.GetXaxis().SetTitle("M(t_{h}) [GeV]")
h.GetYaxis().SetTitle("M(W_{h}) [GeV]")
h.GetXaxis().SetTitleOffset(1.2)
h.GetYaxis().SetTitleOffset(1.2)


c1 = r.TCanvas("c1","comparison", 600,500)
#gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
#gStyle.SetTitleStyle(0)
#gStyle.SetLabelSize(2)
pad = TPad('pad','pad', 0.022, 0.015, 0.98, 0.99)
pad.SetTopMargin(0.09)
#pad.SetBottomMargin(0.07)
pad.SetLeftMargin(0.145)
pad.SetRightMargin(0.13)
pad.Draw()
pad.cd()
gPad.SetLogz()

#h.SetLineWidth(3)
#h.SetLineColor(r.kRed)
h.GetYaxis().SetRangeUser(0, 300)
#h.GetXaxis().SetRangeUser(0, 400)
#h.SetMaximum(0.018)
h.Draw("COLZ")
cmstext()

c1.SaveAs("4j_thad_whad.pdf")
c1.SaveAs("4j_thad_whad.png")



