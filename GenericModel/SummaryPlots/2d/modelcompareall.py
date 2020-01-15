#!/bin/usr/python
import ROOT as r
import sys

r.gROOT.SetBatch(r.kTRUE)
r.gStyle.SetPadBottomMargin(0.13)
r.gStyle.SetPadRightMargin(0.05)
r.gStyle.SetPadLeftMargin(0.20)
r.gStyle.SetPadBottomMargin(0.13)
r.gStyle.SetTitleSize(0.9)

njets = ['3j']
#njets = ['4j', '5j']
drawnumber = int(sys.argv[1])
drawXmin = 0 #-4
drawXmax = 4
drawYmin = 0.9 #-0.1 #0.9
drawYmax = 1.3 #0.3 #1.3
outfile = 'singlebin/'+str(njets[0])+'/bin'+sys.argv[1]+'.pdf'
#outfile = 'singlebin/45j/bin'+sys.argv[1]+'.pdf'

c = r.TCanvas("c", "c", 420, 400)
c.Divide(1, 1)
#cList = []
#for i in range(drawnumber):
#	c = r.TCanvas("csingle", "csingle", 1000, 1000)
#	cList.append(c)

htot = []
for mttbin in range(1, 17+1):
	h = []
	for jet in njets:
		f = r.TFile("../../couplingmodels/"+jet+"/parabola_2d/signal_proc_ch"+jet+".root")
		h.append(f.Get("Graph;%i"%mttbin))
		#h.append(f.Get("bin_content_par1_%i;2"%mttbin))
	htot.append(h)
for mttbin in range(18, 21+1):
	h = []
	for jet in ['3j']:
		f = r.TFile("../../couplingmodels/"+jet+"/parabola_2d/signal_proc_ch"+jet+".root")
		h.append(f.Get("Graph;%i"%mttbin))
		#h.append(f.Get("bin_content_par1_%i;2"%mttbin))
	htot.append(h)

print htot

r.gStyle.SetOptTitle(0)
#c.Print(outfile+"[")
leg = {}
for mtt in range(drawnumber):
	leg[mtt] = r.TLegend(0.6, 0.76, 0.85, 0.87)
	leg[mtt].SetTextSize(0.05)
	leg[mtt].SetFillColor(r.kWhite)
	#leg[mtt].SetFillStyle(0)
	leg[mtt].SetLineColor(0);
	leg[mtt].SetLineStyle(0);
	leg[mtt].SetBorderSize(0);
	leg[mtt].SetShadowColor(0);
	for j in range(len(htot[mtt])):
		print mtt, j
		htot[mtt][j].GetXaxis().SetRangeUser(drawXmin, drawXmax)
		htot[mtt][j].GetYaxis().SetRangeUser(drawYmin, drawYmax)

		p = c.cd(mtt+1)
		p.SetGrid()
		#p.SetGridy()
		r.gStyle.SetGridColor(16)
		r.gStyle.SetGridStyle(7)

		if j == 0:
			#r.gStyle.SetTitleFontSize(0.08)
			#htot[mtt][j].SetTitle("bin %i"%int(mtt+1))
			#htot[mtt][j].SetTitleSize(0.2)
			#htot[mtt][j].SetTitle("m(tt) ["+str(binning.xbins[mtt])+","+str(binning.xbins[mtt+1])+"] (GeV)")
			htot[mtt][j].GetXaxis().SetTitleOffset(0.95)
			htot[mtt][j].GetYaxis().SetTitleOffset(1.45)
			htot[mtt][j].GetXaxis().SetTitle("#it{Y}_{t}")
			#htot[mtt][j].GetYaxis().SetTitle("anomalous/SM yields")
			#htot[mtt][j].GetYaxis().SetTitle("(#it{Y_{t}} yields)/(Powheg yields)")
			htot[mtt][j].GetYaxis().SetTitle("#it{R}^{bin}")
			htot[mtt][j].GetXaxis().SetTitleSize(0.065)
			htot[mtt][j].GetYaxis().SetTitleSize(0.065)
			htot[mtt][j].GetXaxis().SetLabelSize(0.06)
			htot[mtt][j].GetYaxis().SetLabelSize(0.06)
			#htot[mtt][j].SetLineStyle(22) #no use, may need to change from the root file source
			htot[mtt][j].SetMarkerStyle(9) #sepecfic for 3 jets
			htot[mtt][j].Draw("AP")
		else:
			htot[mtt][j].SetMarkerStyle(22) #for 5 jets
			htot[mtt][j].Draw("p")

		if '5j' not in njets[j]:
			leg[mtt].AddEntry(htot[mtt][j], str(njets[j].split('j')[0])+' jets', "lp")
		else:
			leg[mtt].AddEntry(htot[mtt][j], "#geq 5 jets", "lp")

	leg[mtt].Draw("same")


xpos = r.gPad.GetLeftMargin()
ypos = 1.-r.gPad.GetTopMargin()

#box = r.TPave(0.1, 1.18, 1.4, 1.28, 0, '')
box = r.TPave(0.1, 1.22, 1.4, 1.28, 0, '')
box.SetFillColor(0)
box.Draw('same')
box2 = r.TPave(0.1, 1.135, 2.1, 1.21, 0, '')
box2.SetFillColor(0)
box2.Draw('same')

#leg[mtt].Draw("same")

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
#lx2.DrawLatex(xpos+0.04, ypos-0.13, 'Preliminary')
lx2.DrawLatex(xpos+0.04, ypos-0.08, 'Simulation')


lx3 = r.TLatex(0., 0., 'Z')
#lx3.SetNDC(True)
lx3.SetTextFont(43)
lx3.SetTextSize(18)
lx3.SetTextAlign(11)
lx3.DrawLatex(0.25, 1.2, 'bin '+sys.argv[1]+':')
lx3.SetTextSize(17)
lx3.DrawLatex(0.27, 1.17, 'M_{t#bar{t}} = %s-%s GeV'%(sys.argv[2],sys.argv[3]))
lx3.DrawLatex(0.27, 1.14, '|#Deltay_{t#bar{t}}| = 0.6-1.2')
#lx3.DrawLatex(0.27, 1.14, '|#Deltay_{t#bar{t}}| > 1.2')

lx4 = r.TLatex(0., 0., 'Z')
lx4.SetNDC(True)
lx4.SetTextFont(43)
lx4.SetTextSize(24)
lx4.SetTextAlign(31)
#lx4.DrawLatex(xpos+0.75, ypos+0.015, '35.8 fb^{-1} (13 TeV)')
lx4.DrawLatex(xpos+0.75, ypos+0.015, '(13 TeV)')
lx4.Draw()

'''for mtt in range(drawnumber):
	c.cd(mtt+1)
	leg[mtt] = r.TLegend(0.37, 0.7, 0.63, 0.9)
	leg[mtt].AddEntry(htot[mtt][0], "3j", "l")
	leg[mtt].AddEntry(htot[mtt][1], "4j", "l")
	leg[mtt].AddEntry(htot[mtt][2], "5j", "l")
	leg[mtt].AddEntry(htot[mtt][3], "6j and more", "l")
	leg[mtt].Draw("same")'''

#c.Print(outfile)
#c.SaveAs("modelcompareall_newbinning3.pdf")
c.SaveAs(outfile)
