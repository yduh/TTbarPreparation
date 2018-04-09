from ratioplot import *
import sys
import ROOT

SavePlots = True
sysRangeDown = -float(sys.argv[2])
sysRangeUp = float(sys.argv[2])
EWRangeDown = -0.09 #-float(sys.argv[3])
EWRangeUp = float(sys.argv[3])

#-----------------------------------------------------#
def cmstext():
	xpos = ROOT.gPad.GetLeftMargin()
	ypos = 1.-ROOT.gPad.GetTopMargin()

	lx = ROOT.TLatex(0., 0., 'Z')
	lx.SetNDC(True)
	lx.SetTextFont(62)
	lx.SetTextSize(0.10)
	lx.SetTextAlign(13)
	lx.DrawLatex(xpos+0.05, ypos-0.032, 'CMS & #it{HATHOR}')

	lx2 = ROOT.TLatex(0., 0., 'Z')
	lx2.SetNDC(True)
	lx2.SetTextFont(53)
	lx2.SetTextSize(18)
	lx2.SetTextAlign(13)
	#lx2.DrawLatex(xpos+0.04, ypos-0.08, '#it{Preliminary}')
	lx2.DrawLatex(xpos+0.05, ypos-0.16, 'Simulation')

	lx3 = ROOT.TLatex(0., 0., 'Z')
	lx3.SetNDC(True)
	lx3.SetTextFont(43)
	lx3.SetTextSize(20)
	lx3.SetTextAlign(31)
	lx3.DrawLatex(xpos+0.75, ypos+0.03,'35.8 fb^{-1}(13 TeV)')
	lx3.Draw()

def systext(txt):
	xpos = ROOT.gPad.GetLeftMargin()
	ypos = 1.-ROOT.gPad.GetTopMargin()

	lx4 = ROOT.TLatex(0., 0., 'Z')
	lx4.SetNDC(True)
	lx4.SetTextFont(63)
	lx4.SetTextSize(22)
	lx4.SetTextAlign(23)
	lx4.DrawLatex(xpos+0.4, ypos-0.03, sys.argv[1][0]+' jets'+txt)

def delytext(x1, x2, x3, y):
	lx5 = ROOT.TLatex(0., 0., 'Z')
	lx5.SetNDC(True)
	lx5.SetTextFont(63)
	lx5.SetTextSize(18)
	lx5.SetTextAlign(33)
	lx5.SetTextAngle(90)
	lx5.DrawLatex(x1, y, '0.0 < |#Delta_{y}| < 0.6')
	lx5.DrawLatex(x2, y, '0.6 < |#Delta_{y}| < 1.2')
	lx5.DrawLatex(x3, y, '1.2 < |#Delta_{y}| < 6.0')

#-----------------------------------------------------#

ROOT.gStyle.SetOptTitle(0)
f = ROOT.TFile('../WrapUp/%s/packroot/ch%s.root' %(sys.argv[1],sys.argv[1]))
fgt = ROOT.TFile('~/public/lucien/%s/ch%s_gt.root' %(sys.argv[1],sys.argv[1]))

h = createH(f, 'ttsig')
hgt = []
hup = []
hdw = []
hrup = []
hrdw = []
hrgt = []
for case in ['noEW','0.0y','1.0y','2.0y','3.0y']:
	hgt.append(createH(fgt, 'mtt_dely_RECO_'+case))
	hup_temp, hdw_temp = createHthUnc(f, fgt, case, ROOT.kRed, ROOT.kBlue)
	hup.append(hup_temp)
	hdw.append(hdw_temp)
	hrup.append(createRatio(hup_temp, h, ROOT.kRed, 'Rel Unc on t#bar{t}'))
	hrdw.append(createRatio(hdw_temp, h, ROOT.kBlue, 'Rel Unc on t#bar{t}'))
	hrgt.append(createRatio(createH(fgt, 'mtt_dely_RECO_'+case), h, ROOT.kBlack, 'EW correction'))
print 'hgt =',hgt,',hup = ',hup,'hdw = ',hdw
print 'hrup = ',hrup,', hrdw = ',hrdw,', hrdw = ',hrgt

linedely = []
for ibin in range(h.GetXaxis().GetNbins()):
	mttlow = int(float(str(h.GetXaxis().GetBinLabel(ibin+1).split(',')[0].split('-')[0])))
	mtthigh = int(float(str(h.GetXaxis().GetBinLabel(ibin+1).split(',')[0].split('-')[1])))
	if mtthigh == 2000:
		linedely.append(ibin+1)
	h.GetXaxis().SetBinLabel(ibin+1,'%s-%s' %(mttlow,mtthigh))
	h.GetXaxis().LabelsOption('v')
	#hrup[i].SetMarkerStyle(3001)
	#hrdw[i].SetMarkerStyle(3001)
	for i in range(5):
		hrup[i].GetXaxis().SetBinLabel(ibin+1,'%s-%s' %(mttlow,mtthigh))
		hrdw[i].GetXaxis().SetBinLabel(ibin+1,'%s-%s' %(mttlow,mtthigh))
		hrup[i].GetXaxis().LabelsOption('v')
		hrdw[i].GetXaxis().LabelsOption('v')


c, pad1, pad2, pad3, pad4, pad5 = createCanvasPadsgt()

pad1.cd()
hrgt[1].GetYaxis().SetRangeUser(EWRangeDown, EWRangeUp)
hrgt[1].SetLineColor(30)
hrgt[1].Draw("p")
hrgt[2].Draw("psame")
hrgt[3].SetLineColor(6)
hrgt[3].Draw("psame")
hrgt[4].SetLineColor(9)
hrgt[4].Draw("psame")
pad2.cd()
hrup[1].GetYaxis().SetRangeUser(sysRangeDown, sysRangeUp)
hrup[1].Draw("hist")
hrdw[1].Draw("histsame")
pad3.cd()
hrup[2].GetYaxis().SetRangeUser(sysRangeDown, sysRangeUp)
hrup[2].Draw("hist")
hrdw[2].Draw("histsame")
pad4.cd()
hrup[3].GetYaxis().SetRangeUser(sysRangeDown, sysRangeUp)
hrup[3].Draw("hist")
hrdw[3].Draw("histsame")
pad5.cd()
hrup[4].GetYaxis().SetRangeUser(sysRangeDown, sysRangeUp)
hrup[4].Draw("hist")
hrdw[4].Draw("histsame")



#-----------------------------------------------------#
#-----------------------------------------------------#
from ROOT import gROOT
gROOT.GetListOfCanvases().Draw()

#-----------------------------------------------------#
pad1.cd()
leg1 = ROOT.TLegend( 0.75, 0.47, 0.89, 0.87 )
leg1.SetFillColor(0)
leg1.SetLineColor(0)
leg1.AddEntry(hrgt[1], "#it{y_{t}}=0", "L")
leg1.AddEntry(hrgt[2], "#it{y_{t}}=1", "L")
leg1.AddEntry(hrgt[3], "#it{y_{t}}=2", "L")
leg1.AddEntry(hrgt[4], "#it{y_{t}}=3", "L")
leg1.Draw()
pad2.cd()
leg2 = ROOT.TLegend( 0.66, 0.65, 0.89, 0.96 )
leg2.SetFillColor(0)
leg2.SetLineColor(0)
leg2.AddEntry(hup[0], "t#bar{t} EW sys up (+1#sigma)", "L")
leg2.AddEntry(hdw[0], "t#bar{t} EW sys down (-1#sigma)", "L")
leg2.Draw()


#-----------------------------------------------------#
pad1.cd()
linedely1_pad1 = ROOT.TLine(linedely[0], EWRangeDown, linedely[0], EWRangeUp)
linedely2_pad1 = ROOT.TLine(linedely[1], EWRangeDown, linedely[1], EWRangeUp)
linedely1_pad1.SetLineWidth(3)
linedely2_pad1.SetLineWidth(3)
linedely1_pad1.SetLineStyle(2)
linedely2_pad1.SetLineStyle(2)
linedely1_pad1.Draw()
linedely2_pad1.Draw()
pad2.cd()
linedely1_pad2 = ROOT.TLine(linedely[0], sysRangeDown, linedely[0], sysRangeUp)
linedely2_pad2 = ROOT.TLine(linedely[1], sysRangeDown, linedely[1], sysRangeUp)
linedely1_pad2.SetLineWidth(3)
linedely2_pad2.SetLineWidth(3)
linedely1_pad2.SetLineStyle(2)
linedely2_pad2.SetLineStyle(2)
linedely1_pad2.Draw()
linedely2_pad2.Draw()
pad3.cd()
linedely1_pad3 = ROOT.TLine(linedely[0], sysRangeDown, linedely[0], sysRangeUp)
linedely2_pad3 = ROOT.TLine(linedely[1], sysRangeDown, linedely[1], sysRangeUp)
linedely1_pad3.SetLineWidth(3)
linedely2_pad3.SetLineWidth(3)
linedely1_pad3.SetLineStyle(2)
linedely2_pad3.SetLineStyle(2)
linedely1_pad3.Draw()
linedely2_pad3.Draw()
pad4.cd()
linedely1_pad4 = ROOT.TLine(linedely[0], sysRangeDown, linedely[0], sysRangeUp)
linedely2_pad4 = ROOT.TLine(linedely[1], sysRangeDown, linedely[1], sysRangeUp)
linedely1_pad4.SetLineWidth(3)
linedely2_pad4.SetLineWidth(3)
linedely1_pad4.SetLineStyle(2)
linedely2_pad4.SetLineStyle(2)
linedely1_pad4.Draw()
linedely2_pad4.Draw()
pad5.cd()
linedely1_pad5 = ROOT.TLine(linedely[0], sysRangeDown, linedely[0], sysRangeUp)
linedely2_pad5 = ROOT.TLine(linedely[1], sysRangeDown, linedely[1], sysRangeUp)
linedely1_pad5.SetLineWidth(3)
linedely2_pad5.SetLineWidth(3)
linedely1_pad5.SetLineStyle(2)
linedely2_pad5.SetLineStyle(2)
linedely1_pad5.Draw()
linedely2_pad5.Draw()

pad1.cd()
cmstext()
systext('')
#delytext(linedely[0]-1.5, linedely[1]-1.5, linedely[2]-1.5, evtRangeUp-3000)
pad2.cd()
systext(', #it{y_{t}}=0')
pad3.cd()
systext(', #it{y_{t}}=1')
pad4.cd()
systext(', #it{y_{t}}=2')
pad5.cd()
systext(', #it{y_{t}}=3')


#-----------------------------------------------------#
if (SavePlots):
	c.SaveAs("./SYSTEMPLATES/%s/plot_thUnc.pdf" %sys.argv[1])



