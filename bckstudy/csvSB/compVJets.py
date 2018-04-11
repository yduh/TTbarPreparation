import ROOT as r
import sys,argparse,os
from math import sqrt
from array import array

r.gROOT.SetBatch(r.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument('--njets',action='store')
parser.add_argument('--var',action='store')
parser.add_argument('--fitFunc',action='store',default="linear")
parser.add_argument('--region',action='store',default="SR")

option = parser.parse_args()

njets = option.njets
var = option.var
objs = []

def quad(*xs):
	return sqrt(sum(x*x for x in xs))

def fitOrthPoly(ratioHist,mcHist):
	histToFit = ratioHist.Clone()
	nBins = histToFit.GetXaxis().GetNbins()
	weightMeanNum = 0.
	weightMeanDem = 0.
	for ibin in range(1,nBins+1):
		ratio = ratioHist.GetBinContent(ibin)
		statUnc = ratioHist.GetBinError(ibin)
		pred = mcHist.GetBinContent(ibin)
		binCenter = mcHist.GetXaxis().GetBinCenter(ibin)
		histToFit.SetBinContent(ibin,ratio)
		histToFit.SetBinError(ibin,statUnc)
		weightMeanNum += binCenter*pred
		weightMeanDem += pred
	lowRange = mcHist.GetXaxis().GetBinCenter(1)
	highRange = mcHist.GetXaxis().GetBinCenter(nBins)
	orthPolyFunc = r.TF1("orthPoly","[0]+[1]*(x-{0})".format(weightMeanNum/weightMeanDem),lowRange,highRange)
	fitResult = histToFit.Fit(orthPolyFunc,"S")
	return fitResult,orthPolyFunc


#fsr = r.TFile('../../%s/skimroot/skim_Vj.root' %(njets))
#fa = r.TFile('../../%s/skimrootSB_CSVDown/skim_Vj.root' %(njets))
#fb = r.TFile('../../%s/skimrootSB_new/skim_Vj.root' %(njets))
#fc = r.TFile('../../%s/skimrootSB_CSVUp/skim_Vj.root' %(njets))
fsr = r.TFile('../../%s/skimroot/skim_VnJets.root' %(njets))
fa = r.TFile('../../%s/skimroot_Aless0.3/skim_VnJets.root' %(njets))
fb = r.TFile('../../%s/skimroot_B0.3to0.6/skim_VnJets.root' %(njets))
fc = r.TFile('../../%s/skimroot_C0.6to0.8/skim_VnJets.root' %(njets))

#binningX = [i*50 for i in range(41)]
binningX = [200, 300, 340, 380, 420, 460, 520, 720, 1000, 1200, 1500]
binningY = [-6., -2.4, -1.2, -0.6, -0.3, 0., 0.3, 0.6, 1.2, 2.4, 6.]
hxSR = fsr.Get('mtt_RECO').Rebin(len(binningX)-1,"hxSRnew", array("d",binningX))
hySR = fsr.Get('dely_RECO').Rebin(len(binningY)-1, "hySRnew", array("d",binningY))
hxC = fc.Get('mtt_RECO').Rebin(len(binningX)-1,"hxCnew", array("d",binningX))
hyC = fc.Get('dely_RECO').Rebin(len(binningY)-1, "hyCnew", array("d",binningY))
hxB = fb.Get('mtt_RECO').Rebin(len(binningX)-1,"hxBnew", array("d",binningX))
hyB = fb.Get('dely_RECO').Rebin(len(binningY)-1, "hyBnew", array("d",binningY))
hxA = fa.Get('mtt_RECO').Rebin(len(binningX)-1,"hxAnew", array("d",binningX))
hyA = fa.Get('dely_RECO').Rebin(len(binningY)-1, "hyAnew", array("d",binningY))

med = int(hySR.GetXaxis().GetNbins()/2)
hySRabs = r.TH1D('dely4_RECO', 'dely4_RECO', med, 0, 6)
for ibin in range(med):
	hySRabs.SetBinContent(ibin+1,hySR.GetBinContent(med-ibin)+hySR.GetBinContent(med+ibin+1))
	hySRabs.SetBinError(ibin+1,quad(hySR.GetBinError(med-ibin),hySR.GetBinError(med+ibin+1)))
	#print med-ibin, med+ibin+1, hySR.GetBinContent(med-ibin), hySR.GetBinContent(med+ibin+1), hySR.GetBinContent(med-ibin)+hySR.GetBinContent(med+ibin+1)

med = int(hyB.GetXaxis().GetNbins()/2)
hyBabs = r.TH1D('dely2_RECO', 'dely2_RECO', med, 0, 6)
for ibin in range(med):
	hyBabs.SetBinContent(ibin+1,hyB.GetBinContent(med-ibin)+hyB.GetBinContent(med+ibin+1))
	hyBabs.SetBinError(ibin+1,quad(hyB.GetBinError(med-ibin),hyB.GetBinError(med+ibin+1)))
	#print med-ibin, med+ibin+1, hyB.GetBinContent(med-ibin), hyB.GetBinContent(med+ibin+1), hyB.GetBinContent(med-ibin)+hyB.GetBinContent(med+ibin+1)

med = int(hyC.GetXaxis().GetNbins()/2)
hyCabs = r.TH1D('dely3_RECO', 'dely3_RECO', med, 0, 6)
for ibin in range(med):
	hyCabs.SetBinContent(ibin+1,hyC.GetBinContent(med-ibin)+hyC.GetBinContent(med+ibin+1))
	hyCabs.SetBinError(ibin+1,quad(hyC.GetBinError(med-ibin),hyC.GetBinError(med+ibin+1)))
	#print med-ibin, med+ibin+1, hyC.GetBinContent(med-ibin), hyC.GetBinContent(med+ibin+1), hyC.GetBinContent(med-ibin)+hyC.GetBinContent(med+ibin+1)

med = int(hyA.GetXaxis().GetNbins()/2)
hyAabs = r.TH1D('dely1_RECO', 'dely1_RECO', med, 0, 6)
for ibin in range(med):
	hyAabs.SetBinContent(ibin+1,hyA.GetBinContent(med-ibin)+hyA.GetBinContent(med+ibin+1))
	hyAabs.SetBinError(ibin+1,quad(hyA.GetBinError(med-ibin),hyA.GetBinError(med+ibin+1)))
	#print med-ibin, med+ibin+1, hyA.GetBinContent(med-ibin), hyA.GetBinContent(med+ibin+1), hyA.GetBinContent(med-ibin)+hyA.GetBinContent(med+ibin+1)


histList = [hxSR,hySR,hySRabs,hxA,hyA,hyAabs,hxB,hyB,hyBabs,hxC,hyC,hyCabs]
for hist in histList:
	hist.Scale(1./hist.Integral())

#hySR.SetLineColor(2)
#hyB.SetLineColor(4)
#hySR.Draw()
#hyB.Draw("same")

hxsr = hxSR if var == 'mtt' else (hySR if var == 'dely' else hySRabs)
h3 = hxC if var == 'mtt' else (hyC if var == 'dely' else hyCabs)
h2 = hxB if var == 'mtt' else (hyB if var == 'dely' else hyBabs)
h1 = hxA if var == 'mtt' else (hyA if var == 'dely' else hyAabs)

outputFile = r.TFile('./rootfiles/MCVnJets_%s.root'%njets,'RECREATE')
h1.Write()
h2.Write()
h3.Write()

c2srRatio = h3.Clone("C2SA_Ratio")
c2srRatio.Divide(hxsr)
c2srRatio.Write()
b2srRatio = h2.Clone("B2SR_Ratio")
b2srRatio.Divide(hxsr)
b2srRatio.Write()
a2srRatio = h1.Clone("A2SR_Ratio")
a2srRatio.Divide(hxsr)
a2srRatio.Write()

a2bRatio = h1.Clone("A2B_Ratio")
a2bRatio.Divide(h2)
a2bRatio.Write()
a2cRatio = h1.Clone("A2C_Ratio")
a2cRatio.Divide(h3)
a2cRatio.Write()
b2cRatio = h2.Clone("B2C_Ratio")
b2cRatio.Divide(h3)
b2cRatio.Write()


#if not os.path.exists(os.path.abspath(dirName)):
#	os.makedirs(dirName)
histList = [a2srRatio,b2srRatio,c2srRatio, a2bRatio,a2cRatio,b2cRatio]
for hist in histList:
	hist.SetStats(0)
	hist.GetYaxis().SetRangeUser(0.,3.)

a2srRatio.GetYaxis().SetTitleOffset(1.3)
a2srRatio.GetXaxis().SetTitle('M(t#bar{t})' if var == 'mtt' else ('#Deltay' if var == 'dely' else '|#Deltay|'))
a2srRatio.GetYaxis().SetTitle('shape comp A[0-0.3] to SR')
b2srRatio.GetYaxis().SetTitleOffset(1.3)
b2srRatio.GetXaxis().SetTitle('M(t#bar{t})' if var == 'mtt' else ('#Deltay' if var == 'dely' else '|#Deltay|'))
b2srRatio.GetYaxis().SetTitle('shape comp B[0.3-0.6] to SR')
c2srRatio.GetYaxis().SetTitleOffset(1.3)
c2srRatio.GetXaxis().SetTitle('M(t#bar{t})' if var == 'mtt' else ('#Deltay' if var == 'dely' else '|#Deltay|'))
c2srRatio.GetYaxis().SetTitle('shape comp C[0.6-0.8] to SR')

a2bRatio.GetYaxis().SetTitleOffset(1.3)
a2bRatio.GetXaxis().SetTitle('M(t#bar{t})' if var == 'mtt' else ('#Deltay' if var == 'dely' else '|#Deltay|'))
a2bRatio.GetYaxis().SetTitle('shape comp A[0-0.3] to B[0.3-0.6]')
a2cRatio.GetYaxis().SetTitleOffset(1.3)
a2cRatio.GetXaxis().SetTitle('M(t#bar{t})' if var == 'mtt' else ('#Deltay' if var == 'dely' else '|#Deltay|'))
a2cRatio.GetYaxis().SetTitle('shape comp A[0-0.3] to C[0.6-0.8]')
b2cRatio.GetYaxis().SetTitleOffset(1.3)
b2cRatio.GetXaxis().SetTitle('M(t#bar{t})' if var == 'mtt' else ('#Deltay' if var == 'dely' else '|#Deltay|'))
b2cRatio.GetYaxis().SetTitle('shape comp B[0.3-0.6] to C[0.6-0.8]')


c = r.TCanvas('c1', 'c1', 1100, 800)
c.Divide(3, 2)
for i, h in enumerate(histList):
	c.cd(i+1)
	print i
	if option.fitFunc == "linear":
		h.Fit("pol1")
		h.Draw()
	elif option.fitFunc == "orthPoly":
		fitFunc,orthPolyFunc = fitOrthPoly(b2srRatio,h1)
		b2srRatio.Draw()
		orthPolyFunc.Draw("same")

	if option.fitFunc == "linear":
		h.Fit("pol1")
		fitFunc = h.GetFunction("pol1")
		print "chi2/nof for fit: ", fitFunc.GetChisquare()/fitFunc.GetNDF()
		print "p0 parameter: ", fitFunc.GetParameter(0)," pm ", fitFunc.GetParError(0)
		print "p1 parameter: ", fitFunc.GetParameter(1)," pm ", fitFunc.GetParError(1)
		text = r.TLatex()
		text.SetTextSize(0.04)
		text.SetNDC()
		text.DrawLatex(0.2,0.8,"chi2/nof: %4.2f"%float(fitFunc.GetChisquare()/fitFunc.GetNDF()))
		text.DrawLatex(0.2,0.7,"y-intercept: %4.2f #pm %4.2f"%(fitFunc.GetParameter(0),fitFunc.GetParError(0)))
		text.DrawLatex(0.2,0.6,"slope #times 100 GeV: %4.2f #pm %4.2f"%(fitFunc.GetParameter(1)*100,fitFunc.GetParError(1)*100))
	elif option.fitFunc == "orthPoly":
		print "Probf for fit: ", fitFunc.Prob()
		print "p0 parameter: ", fitFunc.Parameter(0)," pm ", fitFunc.ParError(0)
		print "p1 parameter: ", fitFunc.Parameter(1)," pm ", fitFunc.ParError(1)
		text = r.TLatex()
		text.SetTextSize(0.04)
		text.SetNDC()
		text.DrawLatex(0.2,0.8,"prob: %4.2f"%float(fitFunc.Prob()))
		text.DrawLatex(0.2,0.7,"p0: %4.2f #pm %4.2f"%(fitFunc.Parameter(0),fitFunc.ParError(0)))
		text.DrawLatex(0.2,0.6,"p1 #times 100 GeV: %4.2f #pm %4.2f"%(fitFunc.Parameter(1)*100,fitFunc.ParError(1)*100))
	fitFunc.Write()

c.SaveAs("./plots_vjets/RatioVj_%s_%s.pdf" %(njets,var))



