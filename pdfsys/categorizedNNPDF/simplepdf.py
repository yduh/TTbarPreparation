import ROOT
from ROOT import TFile, TH2D, TH2D, TCanvas, TH1D
from math import sqrt
import sys

def hhdist(ha, hb, hc):
	pro = 0.
	la = 0.
	lb = 0.
	for b in range(1, ha.GetNbinsX()+1):
#		pro+=((ha.GetBinContent(b)-hb.GetBinContent(b))/(ha.GetBinContent(b)+hb.GetBinContent(b)))**2
#	return pro
		c = hc.GetBinContent(b)**0
		#if c == 0: continue
		pro+=ha.GetBinContent(b)*hb.GetBinContent(b)/c
		la+=ha.GetBinContent(b)**2/c
		lb+=hb.GetBinContent(b)**2/c

	return pro/sqrt(la*lb)



#njets = sys.argv[1]
NFinal = int(sys.argv[1])
wa = 10
wb = 110
sqrtN = sqrt(wb-wa)


tf = TFile('3456j/skim_pdf_noEW.root')
hcentral = tf.Get('cen')
ofb = hcentral.GetNbinsX()+1
htotal = TH1D(hcentral)
htotal.Reset()
hists = []

outfile3456j = TFile('3456j/n%s/skim_pdf.root' %NFinal, 'RECREATE')

for w in range(wa, wb):
	hists.append(tf.Get('replica_'+str(w)))
	hists[-1].SetBinContent(0, 1.)
	l = 0.
	for b in range(1, ofb):
		hists[-1].SetBinContent(b, (hists[-1].GetBinContent(b)-hcentral.GetBinContent(b)))
		htotal.SetBinContent(b, sqrt(hists[-1].GetBinContent(b)**2 + htotal.GetBinContent(b)**2))

		l+= hists[-1].GetBinContent(b)**2
	hists[-1].SetBinContent(ofb, l)


while(True):
	dmax = 0.
	nhamin = -1
	nhbmin = -1
	for nha in range(0, len(hists)):
		ha = hists[nha]
		for nhb in range(0, nha):
			hb = hists[nhb]
			d = hhdist(ha, hb, hcentral)
#new version considering the sign
			if abs(d) > abs(dmax):
				dmax = d
				nhamin = nha
				nhbmin = nhb
	#print len(hists), dmax
	if dmax < 0:
		hists[nhbmin].SetBinContent(0, -1.*hists[nhbmin].GetBinContent(0))
		hists[nhbmin].SetBinContent(ofb, -1.*hists[nhbmin].GetBinContent(ofb))
		hists[nhamin].Add(hists[nhbmin], -1)
	else:
		hists[nhamin].Add(hists[nhbmin])


#old version without considering the sign
#			if d > dmax:
#				dmax = d
#				nhamin = nha
#				nhbmin = nhb
#	#print len(hists), dmax
#	hists[nhamin].Add(hists[nhbmin])
###	hists[nhamin].Scale(0.5)
###	hists[nhamin].SetBinContent(0, 2*hists[nhamin].GetBinContent(0))
###	hists[nhamin].SetBinContent(ofb, 2*hists[nhamin].GetBinContent(ofb))

	del hists[nhbmin]
	if len(hists) == NFinal: break

hredtotal = TH1D(hcentral)
hredtotal.Reset()
for hist in hists:
	l=0.
	for b in range(1, hcentral.GetNbinsX()+1):
		l+=hist.GetBinContent(b)**2
	norm = sqrt(hist.GetBinContent(ofb)/l)
	#print norm
	for b in range(1, hcentral.GetNbinsX()+1):
		hist.SetBinContent(b, hist.GetBinContent(b)*norm/sqrtN)
		hist.SetBinError(b, 0)
		hredtotal.SetBinContent(b, sqrt(hist.GetBinContent(b)**2 + hredtotal.GetBinContent(b)**2))
		hist.SetBinContent(b, hist.GetBinContent(b)/hcentral.GetBinContent(b))


c=2
dopt = ''
for hist in hists:
	#print hist.GetBinContent(0), sqrt(hist.GetBinContent(ofb))
	hist.SetLineColor(c)
	hist.SetLineWidth(2)
	hist.GetYaxis().SetRangeUser(-0.05, 0.05)
	hist.Draw(dopt)
	c+=1
	dopt ='same'
	hist.Write() #save the choosen PDF subsets after running the algorithm

#======================================================================================================#
# Otto's algorithm finished here
#======================================================================================================#
#remove some small PDF subsets (if no bins having relative uncertainty larger than 0.1%)
for i, hist in enumerate(hists):
	relUnc = []
	tooSmall = False
	for b in range(hist.GetNbinsX()):
		relUnc.append(hist.GetBinContent(b+1))
	#if hist.Integral() < 1E-3: del hists[i]
	if all(s <1E-3 for s in relUnc): del hists[i]


#======================================================================================================#
# Really end of the algorithm, check out some general info
#======================================================================================================#
#canb = TCanvas()
#comparing the total variation of the chosen subsets and the original 100 subsets
htotal.Scale(1./sqrtN)
for b in range(1, htotal.GetNbinsX()+1):
		htotal.SetBinContent(b, htotal.GetBinContent(b)/hcentral.GetBinContent(b))
		hredtotal.SetBinContent(b, hredtotal.GetBinContent(b)/hcentral.GetBinContent(b))

htotal.GetYaxis().SetRangeUser(0, 0.03)
htotal.Draw()
hredtotal.SetLineColor(2)
hredtotal.Draw('same')
#hcentral.Draw('same')
htotal.Write('original')
hredtotal.Write('newPDFcombined')

#print out the RMS (without/with weights) to know the precision of the algorithm
res = 0
resweight = 0
for ibin in range(htotal.GetXaxis().GetNbins()):
	der = (hredtotal.GetBinContent(ibin+1) - htotal.GetBinContent(ibin+1))* hcentral.GetBinContent(ibin+1)
	w = hcentral.GetBinContent(ibin+1)/hcentral.Integral()
	res = res + w*der**2
	resweight = resweight + der**2
print "NFinal=",NFinal,", Remains=",len(hists),", RMS=",sqrt(resweight/htotal.GetXaxis().GetNbins()),", RMS(weight)=",sqrt(res)

outfile3456j.Close()
#======================================================================================================#
# Allocate the chosen PDF subsets into single channels, prepare the templates for use
#======================================================================================================#
#The PDF templates are decided using 3456j channels all together,
#but the drawer only prepared the templates one-by-one for each channel
#3j: 23 bins, 4j: 17 bins, 5j: 11 bins, 6j: 6 bins

def drawT(njets):
	bointer = 0
	if njets == '4j':
		bointer = 23
	elif njets == '5j':
		bointer = 23+17
	elif njets == '6j':
		bointer = 23+17+11

	ttsigf = TFile('../../%s/packroot/ch%s.root' %(njets,njets))
	stf = TFile('../../%s/packroot/ch%s.root' %(njets,njets))

	histsSingleChannel = []

	for hist in hists:
		h = TH1D(hist.GetName()+'%s' %njets, hist.GetName()+'%s' %njets, ttsigf.Get('ttsig').GetNbinsX(), 0, ttsigf.Get('ttsig').GetNbinsX())
		for b in range(ttsigf.Get('ttsig').GetNbinsX()):
			h.SetBinContent(b+1, hist.GetBinContent(b+1+ bointer))
		histsSingleChannel.append(h)

	outfile = TFile('./%s/n%s/skim_pdf.root' %(njets, NFinal), 'RECREATE')


	for i, hist in enumerate(histsSingleChannel):
		templateUp_ttsig = TH1D('ttsig_pdf%sUp'%str(i+1), 'Up', hist.GetNbinsX(), 0, hist.GetNbinsX())
		templateDown_ttsig = TH1D('ttsig_pdf%sDown'%str(i+1), 'Down', hist.GetNbinsX(), 0, hist.GetNbinsX())
		templateUp_st = TH1D('st_pdf%sUp'%str(i+1), 'Up', hist.GetNbinsX(), 0, hist.GetNbinsX())
		templateDown_st = TH1D('st_pdf%sDown'%str(i+1), 'Down', hist.GetNbinsX(), 0, hist.GetNbinsX())
		for b in range(hist.GetNbinsX()):
			tUp = ttsigf.Get('ttsig').GetBinContent(b+1)*(hist.GetBinContent(b+1) +1)
			tDown = (1- hist.GetBinContent(b+1))*ttsigf.Get('ttsig').GetBinContent(b+1)
			templateUp_ttsig.SetBinContent(b+1, tUp)
			templateDown_ttsig.SetBinContent(b+1, tDown)
			tUp = stf.Get('st').GetBinContent(b+1)*(hist.GetBinContent(b+1) +1)
			tDown = (1- hist.GetBinContent(b+1))*stf.Get('st').GetBinContent(b+1)
			templateUp_st.SetBinContent(b+1, tUp)
			templateDown_st.SetBinContent(b+1, tDown)
		templateUp_ttsig.Write('ttsig_pdf%sUp' %str(i+1))
		templateDown_ttsig.Write('ttsig_pdf%sDown' %str(i+1))
		templateUp_st.Write('st_pdf%sUp' %str(i+1))
		templateDown_st.Write('st_pdf%sDown' %str(i+1))

	'''
	tsumUp_ttsig = TH1D('ttsig_pdfsumUp', 'Up', htotal.GetNbinsX(), 0, htotal.GetNbinsX())
	tsumDown_ttsig = TH1D('ttsig_pdfsumDown', 'Down', htotal.GetNbinsX(), 0, htotal.GetNbinsX())
	tsumUp_st = TH1D('st_pdfsumUp', 'Up', htotal.GetNbinsX(), 0, htotal.GetNbinsX())
	tsumDown_st = TH1D('st_pdfsumDown', 'Down', htotal.GetNbinsX(), 0, htotal.GetNbinsX())
	for b in range(htotal.GetNbinsX()):
		tUp = ttsigf.Get('ttsig').GetBinContent(b+1)*(htotal.GetBinContent(b+1) +1)
		tDown = (1- htotal.GetBinContent(b+1))*ttsigf.Get('ttsig').GetBinContent(b+1)
		tsumUp_ttsig.SetBinContent(b+1, tUp)
		tsumDown_ttsig.SetBinContent(b+1, tDown)
		tUp = stf.Get('st').GetBinContent(b+1)*(htotal.GetBinContent(b+1) +1)
		tDown = (1- htotal.GetBinContent(b+1))*stf.Get('st').GetBinContent(b+1)
		tsumUp_st.SetBinContent(b+1, tUp)
		tsumDown_st.SetBinContent(b+1, tDown)
	tsumUp_ttsig.Write('ttsig_pdfsumUp')
	tsumDown_ttsig.Write('ttsig_pdfsumDown')
	tsumUp_st.Write('st_pdfsumUp')
	tsumDown_st.Write('st_pdfsumDown')
	'''


	outfile.Close()

drawT('3j')
drawT('4j')
drawT('5j')
drawT('6j')
