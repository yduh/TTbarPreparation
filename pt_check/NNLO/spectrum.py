#!/usr/bin/python

from array import array
import ROOT as r
import sys
#from math import abs

#r.gStyle.SetOptTitle(0)

mttList_precise = []
mttList = []
XSList_precise = []
XSList = []
XSerrdList_precise = []
XSerruList_precise = []

filePath_precise = "txt/LHC13-PTavt-nnlo-MT2-NNPDF30.txt"
textFile_precise = open(filePath_precise, "r")
lines_precise = textFile_precise.readlines()
for line in lines_precise:
	mtt, xs, rsfsSSd, rsfsSSu, rsd, fsd, rsu, fsu, binsize = line.split()
	diffList = [float(x)-float(xs) for x in line.split()[2:-1]]
	print diffList
	mttList_precise.append(float(mtt))
	XSList_precise.append(float(xs)/float(binsize))
	XSerrdList_precise.append((float(min(diffList))+float(xs))/float(binsize))
	XSerruList_precise.append((float(max(diffList))+float(xs))/float(binsize))

filePath = "txt/LHC13-PTavt-nlo-MT2-NNPDF30.txt"
textFile = open(filePath, "r")
lines = textFile.readlines()
for line in lines:
	mtt, xs, rsfsSSd, rsfeSSu, rsd, fsd, rsu, fsu, binsize = line.split()
	mttList.append(float(mtt))
	XSList.append(float(xs)/float(binsize))

print sum(XSList), sum(XSList_precise), 1/(sum(XSList)/sum(XSList_precise))
if set(mttList_precise) != set(mttList):
	print "NOTICE!"

c = r.TCanvas("c2", "c2", 600, 400)
c.SetGrid()

ratioList = [x/y for x, y in zip(XSList_precise, XSList)]
ratiouList = [x/y for x, y in zip(XSerruList_precise, XSList)]
ratiodList = [x/y for x, y in zip(XSerrdList_precise, XSList)]

gr_ratio = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", ratioList))
gr_ratiou = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", ratiouList))
gr_ratiod = r.TGraph(len(mttList_precise), array("d", mttList_precise), array("d", ratiodList))
gr_ratio.GetXaxis().SetRangeUser(0, 1000)
gr_ratio.GetYaxis().SetRangeUser(0.9, 1.1)
gr_ratio.GetXaxis().SetTitleOffset(1.25)
gr_ratio.GetYaxis().SetTitleOffset(1.25)
#gr_ratio.GetXaxis().SetTitleSize(3)
#gr_ratio.GetYaxis().SetTitleSize(3)
gr_ratio.GetXaxis().SetTitle("p_{T,ave}")
gr_ratio.GetYaxis().SetTitle("NNLO/NLO")
gr_ratio.SetTitle("d#sigma/dp_{T,ave}")
gr_ratio.Draw("AL*")
gr_ratiou.SetLineStyle(2)
gr_ratiod.SetLineStyle(2)
gr_ratiou.SetLineColor(6)
gr_ratiod.SetLineColor(8)
gr_ratiou.SetMarkerColor(6)
gr_ratiod.SetMarkerColor(8)
gr_ratiou.Draw("L*SAME")
gr_ratiod.Draw("L*SAME")

#gr_ratio.SetTitle('k-factor')
#gr_ratiou.SetTitle('k-factor scale up')
#gr_ratiod.SetTitle('k-factor scale dwon')
#c.BuildLegend()
c.SaveAs("NNLO_NLO.png")


##########################################################
weightList = []
weightuList = []
weightdList = []
fweight = r.TFile("nnloweight.root", "RECREATE")
hweight = r.TH1D("nnloweight", "nnlo", 500, 0, 1000)
hweightup = r.TH1D("nnloweightup", "nnlo", 500, 0, 1000)
hweightdw = r.TH1D("nnloweightdw", "nnlo", 500, 0, 1000)

for i in range(0, 1000+2, 2):
	weightList.append(gr_ratio.Eval(i))
	weightuList.append(gr_ratiou.Eval(i))
	weightdList.append(gr_ratiod.Eval(i))
for i in range(len(weightList)):
	hweight.SetBinContent(i+1, weightList[i])
	hweightup.SetBinContent(i+1, weightuList[i])
	hweightdw.SetBinContent(i+1, weightdList[i])

hweight.Write()
hweightup.Write()
hweightdw.Write()
fweight.Close()



##########################################################



