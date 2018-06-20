#!/usr/bin/python
import math, sys, os
import string
from array import array
import ROOT as r
from SCALE import *
import ScaleBook
from vararg import Varargs

nominal = sys.argv[-1]
folderskimroot = "skimroot"
if sys.argv[1][2:6] == 'Tbck':
	#if 'comp' in sys.argv[-1] or 'CSV' in sys.argv[-1]:
	if 'noEW' not in sys.argv[-1]:
		folderskimroot = 'skimrootSB_'+sys.argv[-1]
	else:
		folderskimroot = 'skimrootSB'
else:
	if sys.argv[-1] == 'noEW' or sys.argv[-1] == 'nnlopt' or '.0y' in sys.argv[-1]:
		folderskimroot = 'skimroot'
	else:
		folderskimroot = 'skimroot_'+sys.argv[-1]

print 'root files read from the folder: ~/eos/results/'+sys.argv[1]+"/"+sys.argv[-1]
print 'save skim files in the folder:', folderskimroot, ', ', sys.argv[2]

if('DATA' in sys.argv[2]):
	path = "/uscms/home/yiting11/eos/results/"+sys.argv[1]+"/"+sys.argv[-1]+"/"+sys.argv[2].split('/')[0] if 'unc' in sys.argv[1] else "/uscms/home/yiting11/eos/results/"+sys.argv[1]+"/"+sys.argv[-1]
	os.system("hadd -f "+path+"/DATA.root "+path+"/DATAEL.root "+path+"/DATAMU.root")

if sys.argv[-1] == 'nnlopt':
	f = r.TFile('/uscms/home/yiting11/eos/results/'+sys.argv[1]+'/noEW/'+sys.argv[2]+'.root')
else:
	f = r.TFile('/uscms/home/yiting11/eos/results/'+sys.argv[1]+'/'+sys.argv[-1]+'/'+sys.argv[2]+'.root')

Hists = []

varargs = Varargs().DefaultVarDict
#varargs.update(Varargs().AddVarDict)
varargs.update(Varargs().AddVarDictCRplot)

for i in range(len(sys.argv[3:-1])):
	for histname, info in varargs.iteritems():
		histname = '3j'+histname if '3j' in sys.argv[1] else 'yukawa'+histname
		his = f.Get(sys.argv[3+i]+'/'+histname)

		#his = f.Get('RECO/all_'+info.saveName) if sys.agrv[1] != '3j' and (info.saveName == 'MET' or info.saveName == 'lep_eta' or info.saveName == 'tt_pt') else f.Get(sys.argv[3+i]+'/'+histname)
		#if '3j' not in sys.argv[1] and (info.saveName == 'MET' or info.saveName == 'lep_eta' or info.saveName == 'tt_pt' or info.saveName == 'tt_y'):
		#	his = f.Get('RECO/all_'+info.saveName)
		#if sys.argv[1] != '3j' and (info.saveName == 'met' or info.saveName == 'lepeta' or info.saveName == 'ttpt'):
		#	continue

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
				print "norm qcd scale", str(sys.argv[2].split("/")[-1]+'scale'), qcdscale, histname
			else:
				qcdscale = eval(sys.argv[2]+'scale')
				print "norm qcd scale", str(sys.argv[2]+'scale'), qcdscale, histname
			his.Scale(qcdscale)
			Hists.append(his)
		else:
			if sys.argv[-1] == 'nnlopt':
				his.Scale(ttpowheg)
				his.Scale(0.966289105862) #this value is the ratio of inclusive XS of NLO/NNLO QCD calculation printing out by pt_check/NNLO/spectrum.py
				print "norm nnlopt scale 0.966289105862", histname
			else:
				his.Scale(float(ScaleBook.MappingScales[sys.argv[2].split("/")[-1]]))
				print "norm all oters scale", sys.argv[2].split("/")[-1], float(ScaleBook.MappingScales[sys.argv[2].split("/")[-1]]), histname

			if info.getHistDim() == 1:
				for ibin in range(his.GetXaxis().GetNbins()):
					if his.GetBinContent(ibin+1)< 0:
						his.SetBinContent(ibin+1, 0)
						his.SetBinError(ibin+1, his.GetBinError(ibin+1))
					his.SetBinContent(0, 0) #under flow
					his.SetBinError(0, his.GetBinError(0))
					his.SetBinContent(his.GetXaxis().GetNbins()+1, 0) #upper flow
					his.SetBinError(his.GetXaxis().GetNbins()+1, his.GetBinError(his.GetXaxis().GetNbins()+1))
				Hists.append(his)
			elif info.getHistDim() ==2:
				for ibinx in range(his.GetXaxis().GetNbins()):
					for ibiny in range(his.GetYaxis().GetNbins()):
						if his.GetBinContent(ibinx+1, ibiny+1)< 0:
							his.SetBinContent(ibinx+1, ibiny+1, 0)
							his.SetBinError(ibinx+1, ibiny+1, his.GetBinError(ibinx+1,ibiny+1))
						his.SetBinContent(0, 0, 0)
						his.SetBinError(0, 0, his.GetBinError(0,0))
						his.SetBinContent(his.GetXaxis().GetNbins()+1, his.GetYaxis().GetNbins()+1, 0)
						his.SetBinError(his.GetXaxis().GetNbins()+1, his.GetYaxis().GetNbins()+1, his.GetBinError(his.GetXaxis().GetNbins()+1,his.GetYaxis().GetNbins()+1))
				Hists.append(his)


os.system("mkdir -p "+sys.argv[1][0:2]+"/"+folderskimroot)

if(sys.argv[2] == 'tt_PowhegP8'):
	skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"/skim_"+sys.argv[2]+"_"+sys.argv[-1]+".root", "RECREATE")

elif(len(sys.argv[2].split("/")) == 2): #this only happens for the systematics
    os.system("mkdir -p "+sys.argv[1][0:2]+"/"+folderskimroot+"SYS/"+sys.argv[2].split("/")[0])
    if(sys.argv[2].split("/")[0] == 'MCs'): #this is the one with dedicated MC samples
		skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"SYS/"+sys.argv[2].split("/")[0]+"/skim_"+sys.argv[2].split("/")[-1].split("_")[1]+"_tt_PowhegP8_"+sys.argv[-1]+".root", "RECREATE")
	#elif(sys.argv[2].split("/")[0] == 'STuncs'):
	#	skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"SYS/"+sys.argv[2].split("/")[0]+"/skim_"+sys.argv[2].split("/")[-1].split("_")[-1]+"_"+sys.argv[2].split("/")[-1].rsplit("_",1)[0]+".root", "RECREATE")
    else:
		if "PowhegP8" not in sys.argv[2].split("/")[-1]: #this is for bck sys
			skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"SYS/"+sys.argv[2].split("/")[0]+"/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+".root", "RECREATE")
		else:
			if sys.argv[-1] == 'nnlopt':
				skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"SYS/"+sys.argv[2].split("/")[0]+"/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+"_noEW.root", "RECREATE")
			else:
				skimroot = r.TFile(sys.argv[1][0:2]+"/"+folderskimroot+"SYS/"+sys.argv[2].split("/")[0]+"/skim_"+sys.argv[2].split("/")[0]+"_"+sys.argv[2].split("/")[-1]+"_"+sys.argv[-1]+".root", "RECREATE")

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



