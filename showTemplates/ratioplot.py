from ROOT import TCanvas, TColor, TGaxis, TH1D, TPad

def createH(f, component):
	print f
	h = f.Get(component)
	h.SetLineColor(TColor.kBlack)
	h.SetLineWidth(2)
	h.GetYaxis().SetTitleSize(20)
	h.GetYaxis().SetTitleFont(43)
	h.GetYaxis().SetTitleOffset(1.55)
	h.SetStats(0)

	y = h.GetYaxis()
	y.SetTitle("Events")
	y.SetNdivisions(505)
	y.SetTitleSize(20)
	y.SetTitleFont(43)
	y.SetTitleOffset(2.695)
	y.SetLabelFont(43)
	y.SetLabelSize(18)

	return h


def createHUp(f, component, sys, color):
	h = f.Get('%s_%sUp' %(component, sys))
	h.SetLineColor(color)
	h.SetLineWidth(2)
	return h

def createHDw(f, component, sys, color):
	h = f.Get('%s_%sDown' %(component, sys))
	h.SetLineColor(color)
	h.SetLineWidth(2)
	return h

def createHthUnc(f, fEW, gt, colorUp, colorDw):
	h = f.Get('ttsig')
	hrsfsUp = f.Get('ttsig_rsfsUp')
	hrsfsDw = f.Get('ttsig_rsfsDown')
	hEW = fEW.Get('mtt_dely_RECO_%s' %gt)
	print h, hrsfsUp, hrsfsDw, hEW

	hthUncUp = TH1D('ttsig_thUncUp_%s' %gt, 'ttsig_thUncUp', h.GetXaxis().GetNbins(), 0, h.GetXaxis().GetNbins())
	hthUncDw = TH1D('ttsig_thUncDw_%s' %gt, 'ttsig_thUncDw', h.GetXaxis().GetNbins(), 0, h.GetXaxis().GetNbins())
	for ibin in range(h.GetXaxis().GetNbins()):
		mean = h.GetBinContent(ibin+1)
		rsfsUp = hrsfsUp.GetBinContent(ibin+1)
		rsfsDw = hrsfsDw.GetBinContent(ibin+1)
		EW = hEW.GetBinContent(ibin+1)
		#thUncUp = (rsfsUp/mean)* (EW/mean) *mean
		thUncUp = (1+(rsfsUp/mean-1)* (EW/mean-1)) *mean
		thUncDw = (1+(rsfsDw/mean-1)* (EW/mean-1)) *mean
		print thUncUp/mean, thUncDw/mean
		hthUncUp.SetBinContent(ibin+1, thUncUp)
		hthUncDw.SetBinContent(ibin+1, thUncDw)
		hthUncUp.SetBinError(ibin+1, 0)
		hthUncDw.SetBinError(ibin+1, 0)
	hthUncUp.SetLineColor(colorUp)
	hthUncDw.SetLineColor(colorDw)
	hthUncUp.SetLineWidth(2)
	hthUncDw.SetLineWidth(2)
	hthUncUp.SetMarkerStyle(3001)
	hthUncDw.SetMarkerStyle(3001)
	return hthUncUp, hthUncDw

def createRatio(hup, hm, color, name):
    hr = hup.Clone()
    hr.SetLineColor(color)
    hr.SetMarkerStyle(21)
    hr.SetMarkerSize(0.8)
    hr.SetTitle("")
    # Set up plot for markers and errors
    hr.Sumw2()
    hr.SetStats(0)
    hr.Add(hm, -1)
    hr.Divide(hm)

    # Adjust y-axis settings
    y = hr.GetYaxis()
    y.SetTitle("rel unc %s" %name)
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(2.695)
    y.SetLabelFont(43)
    y.SetLabelSize(18)

    # Adjust x-axis settings
    x = hr.GetXaxis()
    x.SetTitle("m_{t#bar{t}} [GeV/c^{2}]")
    x.SetTitleSize(20)
    x.SetTitleFont(43)
    x.SetTitleOffset(11.7) #was set at 11.7 #set 13.1 if three rel unc
    x.SetLabelFont(43)
    x.SetLabelSize(18)

    return hr


def createCanvasPads2():
    c = TCanvas("c", "canvas", 800, 900)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0.02, 0.305, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetLeftMargin(0.13)
    #pad1.SetGridx()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0.02, 0.03, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.5)
    pad2.SetLeftMargin(0.13)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    return c, pad1, pad2

def createCanvasPads3():
    c = TCanvas("c", "canvas", 800, 1200)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0.02, 0.46, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetLeftMargin(0.13)
    #pad1.SetGridx()
    pad1.Draw()
    c.cd()
    pad2 = TPad("pad2", "pad2", 0.02, 0.31, 1, 0.455)
    pad2.SetBottomMargin(0)
    pad2.SetLeftMargin(0.13)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad3 = TPad("pad3", "pad3", 0.02, 0.03, 1, 0.3)
    pad3.SetTopMargin(0)  # joins upper and lower plot
    pad3.SetBottomMargin(0.5)
    pad3.SetLeftMargin(0.13)
    pad3.SetGridx()
    pad3.SetGridy()
    pad3.Draw()
    return c, pad1, pad2, pad3

def createCanvasPads4():
    c = TCanvas("c", "canvas", 800, 1100)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0.02, 0.575, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    pad1.SetLeftMargin(0.13)
    #pad1.SetGridx()
    pad1.Draw()
    c.cd()
    pad2 = TPad("pad2", "pad2", 0.02, 0.41, 1, 0.57)
    pad2.SetBottomMargin(0)
    pad2.SetLeftMargin(0.13)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad3 = TPad("pad3", "pad3", 0.02, 0.26, 1, 0.40)
    pad3.SetTopMargin(0)  # joins upper and lower plot
    pad3.SetBottomMargin(0)
    pad3.SetLeftMargin(0.13)
    pad3.SetGridx()
    pad3.SetGridy()
    pad3.Draw()
    c.cd()
    pad4 = TPad("pad4", "pad4", 0.02, 0.03, 1, 0.25)
    pad4.SetTopMargin(0)
    pad4.SetBottomMargin(0.5)
    pad4.SetLeftMargin(0.13)
    pad4.SetGridx()
    pad4.SetGridy()
    pad4.Draw()
    return c, pad1, pad2, pad3, pad4

def createCanvasPadsgt():
	c = TCanvas("c", "canvas", 800, 1200)
	pad1 = TPad("pad1", "pad1", 0.02, 0.76, 1, 0.95)
	pad1.SetBottomMargin(0)
	pad1.SetTopMargin(0.11)
	pad1.SetLeftMargin(0.13)
	pad1.SetGridx()
	pad1.SetGridy()
	pad1.Draw()
	pad2 = TPad("pad2", "pad2", 0.02, 0.61, 1, 0.75)
	pad2.SetBottomMargin(0)
	pad2.SetTopMargin(0)
	pad2.SetLeftMargin(0.13)
	pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad3 = TPad("pad3", "pad3", 0.02, 0.46, 1, 0.60)
	pad3.SetBottomMargin(0)
	pad3.SetTopMargin(0)
	pad3.SetLeftMargin(0.13)
	pad3.SetGridx()
	pad3.SetGridy()
	pad3.Draw()
	pad4 = TPad("pad4", "pad4", 0.02, 0.30, 1, 0.45)
	pad4.SetBottomMargin(0)
	pad4.SetTopMargin(0)
	pad4.SetLeftMargin(0.13)
	pad4.SetGridx()
	pad4.SetGridy()
	pad4.Draw()
	pad5 = TPad("pad5", "pad5", 0.02, 0.011, 1, 0.29)
	pad5.SetBottomMargin(0)
	pad5.SetTopMargin(0)
	pad5.SetLeftMargin(0.13)
	pad5.SetBottomMargin(0.45)
	pad5.SetGridx()
	pad5.SetGridy()
	pad5.Draw()
	return c, pad1, pad2, pad3, pad4, pad5


