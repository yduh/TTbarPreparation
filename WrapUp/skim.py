#!/usr/bin/python
import math, sys, os
import string
from array import array
import ROOT as r
from SCALE import *
import ScaleBook
from vararg import Varargs

folderskimroot = "skimroot"
if sys.argv[1][2:6] == 'Tbck':
	#if 'comp' in sys.argv[-1] or 'CSV' in sys.argv[-1]:
	if 'noEW' not in sys.argv[-1]:
		folderskimroot = 'skimrootSB_'+sys.argv[-1]
	else:
		folderskimroot = 'skimrootSB'
else:
	if sys.argv[-1] == 'noEW' or sys.argv[-1] == 'nnlopT' or '.0y' in sys.argv[-1]:
		folderskimroot = 'skimroot'
	else:
		folderskimroot = 'skimroot_'+sys.argv[-1]

print 'root files read from the folder: ~/eos/results/'+sys.argv[1]+"/"+sys.argv[-1]
print 'save skim files in the folder:', folderskimroot

if(sys.argv[2] == 'DATA'):
	path = "/uscms/home/yiting11/eos/results/"+sys.argv[1]+"/"+sys.argv[-1]
	os.system("hadd -f "+path+"/DATA.root "+path+"/DATAEL.root "+path+"/DATAMU.root")

f = r.TFile('/uscms/home/yiting11/eos/results/'+sys.argv[1]+'/'+sys.argv[-1]+'/'+sys.argv[2]+'.root')

Hists = []

varargs = Varargs().DefaultVarDict
varargs.update(Varargs().AddVarDict)

for i in range(len(sys.argv[3:-1])):
	for histname, info in varargs.iteritems():
		histname = '3j'+histname if '3j' in sys.argv[1] else 'yukawa'+histname
		his = f.Get(sys.argv[3+i]+'/'+histname)
		if len(sys.argv[3:-1]) == 1:
			his.SetName(info.saveName)
		else:
			his.SetName(info.saveName+'_'+sys.argv[3+i].split('_')[-1])
		if info.getHistDim() == 1:
			his.Rebin(*info.rebinFactors)
		elif info.getHistDim() == 2:
			his.Rebin2D(*info.rebinFactors)

		if(sys.argv[2][0:3] == 'QCD' or sys.argv[2].split("/")[-1][0:3] == 'QCD'):
			if(len(sys.argv[2].split("/")) == 2):
				qcdscale = eval(sys.argv[2].split("/")[-1]+'scale')
				print "norm qcd scale", str(sys.argv[2].aplit("/")[-1]+'scale'), qcdscale, histname
			else:
				qcdscale = eval(sys.argv[2]+'scale')
				print "norm qcd scale", str(sys.argv[2]+'scale'), qcdscale, histname
			his.Scale(qcdscale)
			Hists.append(his)
		else:
			if sys.argv[-1] == 'nnlopT':
				his.Scale(ttpowheg)
				his.Scale(0.966289105862) #this value is the ratio of inclusive XS of NLO/NNLO QCD calculation printing out by pt_check/NNLO/spectrum.py
				print "norm nnlopT scale 0.966289105862", histname
			else:
				his.Scale(float(ScaleBook.MappingScales[sys.argv[2].split("/")[-1]]))
				print "norm all oters scale", sys.argv[2].split("/")[-1], float(ScaleBook.MappingScales[sys.argv[2].split("/")[-1]]), histname

			if info.getHistDim() == 1:
				for ibin in range(his.GetXaxis().GetNbins()):
					if his.GetBinContent(ibin+1)< 0:
						his.SetBinContent(ibin+1, 0)
					his.SetBinContent(0, 0) #under flow
					his.SetBinContent(his.GetXaxis().GetNbins()+1, 0) #upper flow
				Hists.append(his)
			elif info.getHistDim() ==2:
				for ibinx in range(his.GetXaxis().GetNbins()):
					for ibiny in range(his.GetYaxis().GetNbins()):
						if his.GetBinContent(ibinx+1, ibiny+1)< 0:
							his.SetBinContent(ibinx+1, ibiny+1, 0)
						his.SetBinContent(0, 0, 0)
						his.SetBinContent(his.GetXaxis().GetNbins()+1, his.GetYaxis().GetNbins()+1, 0)
				Hists.append(his)


os.system("mkdir -p "+sys.argv[1][0:2]+"/"+folderskimroot)
if(sys.argv[2] == 'tt_PowhegP8'):
	skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/skim_"+sys.argv[2]+"_"+sys.argv[-1]+".root", "RECREATE")
	#skimroot.mkdir(sys.argv[-1])
	#skimroot.cd(sys.argv[-1])
#elif(sys.argv[2].split("/")[-1] == 'tt_PowhegP8' or sys.argv[2].split("/")[-1] == 'tt_mtop1755_PowhegP8' or sys.argv[2].split("/")[-1] == 'tt_mtop1695_PowhegP8'):
#	skimroot = r.TFile(sys.argv[1]+"/"+folderskimroot+"/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+".root", "RECREATE")
elif(len(sys.argv[2].split("/")) == 2): #this only happens for the systematics
        os.system("mkdir -p "+sys.argv[1][0:2]+"/"+folderskimroot+"/sys")
	if(sys.argv[2].split("/")[0] == 'MCs'): #this is the one with dedicated MC samples
		skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/sys/skim_"+sys.argv[2].split("/")[-1].split("_")[1]+"_tt_PowhegP8_"+sys.argv[-1]+".root", "RECREATE")
	elif(sys.argv[2].split("/")[0] == 'STuncs'):
		skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/sys/skim_"+sys.argv[2].split("/")[-1].split("_")[-1]+"_"+sys.argv[2].split("/")[-1].rsplit("_",1)[0]+".root", "RECREATE")
	else:
		if "PowhegP8" not in sys.argv[2].split("/")[-1]: #this is for bck sys
			skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/sys/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+".root", "RECREATE")
		else:
			skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/sys/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+"_"+sys.argv[-1]+".root", "RECREATE")
else:
	skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/skim_"+sys.argv[2]+".root", "RECREATE")


#elif(sys.argv[2].split("/")[1]):
#	skimroot = r.TFile(sys.argv[1]+"/"+folderskimroot+"/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+".root", "RECREATE")
#else:
#	skimroot = r.TFile(sys.argv[1]+"/"+folderskimroot+"/skim_"+sys.argv[2]+".root", "RECREATE")

print Hists
if len(sys.argv[3:-1]) == 1:
	for h in range(len(Hists)):
		Hists[h].Write(Hists[h].GetName()+"_"+sys.argv[3].split("_")[-1])
else:
	for h in range(len(Hists)):
		Hists[h].Write()

skimroot.Close()



