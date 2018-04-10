#!/bin/usr/python
import ROOT as r
import binning
import sys

njets = sys.argv[1]
Numbins = {'3j':23, '4j':17, '5j':11, '6j':6}
drawibin = int(sys.argv[2])

drawXmin = -4
drawXmax = 4
drawYmin = -0.2 #-0.1 #0.9
drawYmax = 0.25 #0.3 #1.3
outfile = 'singlebin/'+njets+'/bin'+str(drawibin)+'.png'

c = r.TCanvas("c", "c", 520, 500)
c.SetGrid()
r.gStyle.SetPadBottomMargin(0.23)
r.gStyle.SetPadRightMargin(0.05)
r.gStyle.SetPadLeftMargin(0.30)
r.gStyle.SetTitleSize(0.9)
r.gStyle.SetOptTitle(0)
r.gStyle.SetGridColor(16)
r.gStyle.SetGridStyle(7)

f = r.TFile(njets+"/signal_proc_ch"+njets+".root")
fold = r.TFile(njets+"/signal_proc_ch"+njets+"old.root")

htot = []
htotold = []
for ibin in range(Numbins[njets]):
	htot.append(f.Get("Graph;%i"%(ibin+1)))
	htotold.append(fold.Get("Graph;%i"%(ibin+1)))
#print htotold


htot[drawibin-1].GetXaxis().SetRangeUser(drawXmin, drawXmax)
htot[drawibin-1].GetYaxis().SetRangeUser(drawYmin, drawYmax)
htot[drawibin-1].GetXaxis().SetTitleOffset(0.95)
htot[drawibin-1].GetYaxis().SetTitleOffset(1.45)
htot[drawibin-1].GetXaxis().SetTitleSize(0.035)
htot[drawibin-1].GetYaxis().SetTitleSize(0.035)
htot[drawibin-1].GetXaxis().SetTitle("mass variation from nominal m_{t}=172.5 (GeV)")
htot[drawibin-1].GetYaxis().SetTitle("relative variation of the yields")
htot[drawibin-1].GetXaxis().SetLabelSize(0.05)
htot[drawibin-1].GetYaxis().SetLabelSize(0.05)
#htot[drawibin-1].Draw("AP")
htot[drawibin-1].Draw()

htotold[drawibin-1].GetXaxis().SetRangeUser(drawXmin, drawXmax)
htotold[drawibin-1].GetYaxis().SetRangeUser(drawYmin, drawYmax)
htotold[drawibin-1].Draw("same")


leg = r.TLegend(0.5, 0.58, 0.65, 0.68)
leg.SetTextSize(0.02)
leg.SetFillColor(r.kWhite)
leg.SetLineColor(0);
leg.SetLineStyle(0);
leg.SetBorderSize(0);
leg.SetShadowColor(0);
if njets != '6j':
	leg.AddEntry(htot[drawibin-1], "%s jets" sys.argv[1][0], "lp")
else:
	leg.AddEntry(htot[drawibin-1], "#geq6 jets", "lp")
leg.Draw()

xpos = r.gPad.GetLeftMargin()
ypos = 1.-r.gPad.GetTopMargin()

box = r.TPave(0.1, 1.18, 1.4, 1.28, 0, '')
box.SetFillColor(0)
box.Draw()


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
lx2.DrawLatex(xpos+0.04, ypos-0.08, 'Simulation')


lx3 = r.TLatex(0., 0., 'Z')
lx3.SetTextFont(43)
lx3.SetTextSize(23)
lx3.SetTextAlign(11)
lx3.DrawLatex(0.25, 1.2, 'bin '+str(drawibin))

c.SaveAs(outfile)
