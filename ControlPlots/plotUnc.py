import math, sys, re
from ROOT import TH1D, TGraphErrors, TFile, TCanvas, TLatex, TLegend, TF1, TMath, TPad, TLine
import ROOT

njets = '3j'

def settitle(title = '2.3 fb^{-1} (13 TeV)'):
	xpos = 1. - ROOT.gPad.GetRightMargin()
	ypos = 1. - ROOT.gPad.GetTopMargin()
	lxtitle = TLatex(0., 0., 'Z')
	lxtitle.SetNDC(True)
	lxtitle.SetTextFont(43)
	lxtitle.SetTextSize(30)
	lxtitle.SetTextAlign(31)
	lxtitle.DrawLatex(xpos, ypos+0.02, title)

def setchannel(title = '#splitline{l+jets parton}{%s}' %njets):
	xpos = 1. - ROOT.gPad.GetRightMargin()
	ypos = 1. - ROOT.gPad.GetTopMargin()
	lxtitle = TLatex(0., 0., 'Z')
	lxtitle.SetNDC(True)
	lxtitle.SetTextFont(63)
	lxtitle.SetTextSize(25)
	lxtitle.SetTextAlign(13)
	lxtitle.DrawLatex(0.35, ypos-0.03, title)

def cmstext(add = ''):
	xpos = ROOT.gPad.GetLeftMargin()
	ypos = 1.-ROOT.gPad.GetTopMargin()
	lx = TLatex(0., 0., 'Z')
	lx.SetNDC(True)
	lx.SetTextFont(63)
	lx.SetTextSize(30)
	lx.SetTextAlign(13)
	lx.DrawLatex(xpos+0.04, ypos-0.02, 'CMS')
	lx2 = TLatex(0., 0., 'Z')
	lx2.SetNDC(True)
	lx2.SetTextFont(53)
	lx2.SetTextSize(25)
	lx2.SetTextAlign(13)
	lx2.DrawLatex(xpos+0.04, ypos-0.08, add)

def legend(title = ''):
    lg = TLegend(0.65, 0.55, 0.95, 0.90, title)
    lg.SetFillColor(0)
    lg.SetFillStyle(0);
    lg.SetLineColor(0);
    lg.SetLineStyle(0);
    lg.SetBorderSize(0);
    lg.SetShadowColor(0);
    lg.SetTextFont(42);
    lg.SetTextSize(0.06);
    return lg


class plotUnc:
	tfiles = {}
	lgx = 0.65
	lgy = 0.4

	def __init__(self):
		self.MCplots = []
		self.MCplotsUp = []
		self.MCplotsDown = []
		self.DAplots = []
		self.Otherplots = []
		self.DIVplots = []
		self.Canvases = []
		self.Pads = []
		self.unc = False
		ROOT.gStyle.SetOptFit(0);
		ROOT.gStyle.SetOptStat(0);
		ROOT.gStyle.SetPadTickX(0);
		ROOT.gStyle.SetPadTickY(0);
		ROOT.gStyle.SetOptStat(0);
		ROOT.gStyle.SetOptStat(0);

		ROOT.gStyle.SetPadTopMargin(0.05);
		ROOT.gStyle.SetPadRightMargin(0.05);
		ROOT.gStyle.SetPadBottomMargin(0.15);
		ROOT.gStyle.SetPadLeftMargin(0.15);

		ROOT.gStyle.SetLabelFont(43,"x");
		ROOT.gStyle.SetLabelFont(43,"y");
		ROOT.gStyle.SetLabelFont(43,"z");
		ROOT.gStyle.SetLabelOffset(0.01,"x");
		ROOT.gStyle.SetLabelOffset(0.01,"y");
		ROOT.gStyle.SetLabelOffset(0.01,"z");
		ROOT.gStyle.SetLabelSize(25,"x");
		ROOT.gStyle.SetLabelSize(25,"y");
		ROOT.gStyle.SetLabelSize(25,"z");
		ROOT.gStyle.SetTitleFont(43,"x");
		ROOT.gStyle.SetTitleFont(43,"y");
		ROOT.gStyle.SetTitleFont(43,"z");
		ROOT.gStyle.SetTitleOffset(1.2,"x");
		ROOT.gStyle.SetTitleOffset(1.5,"y");
		ROOT.gStyle.SetTitleOffset(1.1,"z");
		ROOT.gStyle.SetTitleSize(30,"x");
		ROOT.gStyle.SetTitleSize(30,"y");
		ROOT.gStyle.SetTitleSize(30,"z");

	def legend(self, legtitle):
		xpos = 1. - ROOT.gPad.GetRightMargin()
		ypos = 1. - ROOT.gPad.GetTopMargin()
		#self.lg = TLegend(0.55, 0.4, xpos-0.02, ypos-0.02)
		self.lg = TLegend(self.lgx, self.lgy, xpos-0.02, ypos-0.02)
		if len(legtitle) != 0:
			self.lg.SetHeader(legtitle)
		self.lg.SetFillColor(0)
		self.lg.SetFillStyle(0);
		self.lg.SetLineColor(0);
		self.lg.SetLineStyle(0);
		self.lg.SetBorderSize(0);
		self.lg.SetShadowColor(0);
		self.lg.SetTextFont(42);
		self.lg.SetTextSize(0.07);

	def setchannel(self, title = '#splitline{l+jets parton}{%s}' %njets):
		xpos = 1. - ROOT.gPad.GetRightMargin()
		ypos = 1. - ROOT.gPad.GetTopMargin()
		lxtitle = TLatex(0., 0., 'Z')
		lxtitle.SetNDC(True)
		lxtitle.SetTextFont(63)
		lxtitle.SetTextSize(25)
		lxtitle.SetTextAlign(13)
		lxtitle.DrawLatex(0.35, ypos-0.03, title)

	def cmstext(self, add = ''):
		xpos = ROOT.gPad.GetLeftMargin()
		ypos = 1.-ROOT.gPad.GetTopMargin()
		self.lx = TLatex(0., 0., 'Z')
		self.lx.SetNDC(True)
		self.lx.SetTextFont(62)
		self.lx.SetTextSize(0.07)
		self.lx.SetTextAlign(13)
		self.lx.DrawLatex(xpos+0.04, ypos-0.02, 'CMS')
		self.lx2 = TLatex(0., 0., 'Z')
		self.lx2.SetNDC(True)
		self.lx2.SetTextFont(52)
		self.lx2.SetTextSize(0.07)
		self.lx2.SetTextAlign(13)
		self.lx2.DrawLatex(xpos+0.04, ypos-0.08, add)

	def settitle(self, title):
		xpos = 1. - ROOT.gPad.GetRightMargin()
		ypos = 1. - ROOT.gPad.GetTopMargin()
		self.lxtitle = TLatex(0., 0., 'Z')
		self.lxtitle.SetNDC(True)
		self.lxtitle.SetTextFont(42)
		self.lxtitle.SetTextSize(0.07)
		self.lxtitle.SetTextAlign(31)
		self.lxtitle.DrawLatex(xpos, ypos+0.02, title)

	def addCentralplot(self, filename, histpath, title, scale, color, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.MCplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.MCplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.MCplots.append(TH1D(self.tfiles[filename].Get(histpath)))
		#self.MCplots[-1].SetFillColor(color)
		self.MCplots[-1].SetLineColor(color)
		#self.MCplots[-1].Scale(scale, 'width')
		self.MCplots[-1].Scale(scale)
		self.MCplots[-1].SetTitle(title)
		return self.MCplots

	def addTplotUp(self, filename, histpath, title, scale, color, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.MCplotsUp.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.MCplotsUp.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.MCplotsUp.append(TH1D(self.tfiles[filename].Get(histpath)))
		self.MCplotsUp[-1].SetLineColor(color)
		self.MCplotsUp[-1].SetTitle(title)
		self.MCplotsUp[-1].Scale(scale)
		#self.MCplotsUp[-1].Scale(1., 'width')
		#self.MCplotsUp[-1].Scale(1.)//close box
		return self.MCplotsUp
	def addTplotDown(self, filename, histpath, title, scale, color, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.MCplotsDown.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.MCplotsDown.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.MCplotsDown.append(TH1D(self.tfiles[filename].Get(histpath)))
		self.MCplotsDown[-1].SetLineColor(color)
		self.MCplotsDown[-1].SetTitle(title)
		self.MCplotsDown[-1].Scale(scale)
		#self.MCplots[-1].Scale(1., 'width')
		#self.MCplots[-1].Scale(1.)//close box
		return self.MCplotsDown

	def addOtherplot(self, filename, histpath, title, scale, color, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.Otherplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.Otherplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.Otherplots.append(TH1D(self.tfiles[filename].Get(histpath)))
		self.Otherplots[-1].SetLineColor(color)
		self.Otherplots[-1].SetTitle(title)
		self.Otherplots[-1].Scale(scale)
		return self.Otherplots

	def drawAddWithRelUnc(self, options = 'hist', rebin = 1, legtitle = '', title = '', ratio = False, rangemin = 0., rangemax = 0., printbinwidth = True, xtitle = '', ytitle = '', logy = False):
		self.cumaddhist = []
		self.cumaddhist.append(TH1D(self.MCplots[0]))
		self.cumaddhist.append(TH1D(self.Otherplots[0]))
		self.cumaddhist.append(TH1D(self.Otherplots[1]))
		for hist in self.MCplots[1:]:
			self.cumaddhist.append(TH1D(self.cumaddhist[-1]))
			self.cumaddhist[-1].Add(hist)
			self.cumaddhist[-1].SetFillColor(hist.GetFillColor())
			self.cumaddhist[-1].SetLineColor(hist.GetLineColor())
			self.cumaddhist[-1].SetTitle(hist.GetTitle())


		totalevents = 0.
		for hist in self.MCplots:
			if rangemin != rangemax:
				hist.GetXaxis().SetRangeUser(rangemin, rangemax)
			totalevents += hist.Integral()
		print 'Total MC events: ', totalevents
		totalevents = 0.
		for hist in self.DAplots:
			if rangemin != rangemax:
				hist.GetXaxis().SetRangeUser(rangemin, rangemax)
			totalevents += hist.Integral()
		print 'Total DA events: ', totalevents
		mymax = 0.
		self.Canvases.append(TCanvas('CanvasAdd_' + self.cumaddhist[-1].GetName(), 'CanvasAdd_' + self.cumaddhist[-1].GetName(), 800, 600))
		if ratio == True:
			split = 0.3;
			spaceleft = 0.15;
			spaceright = 0.05;
			self.Pads.append(TPad("histpad", "histpad", 0, split, 1.,1.))
			self.Pads[-1].SetTopMargin(0.05);
			self.Pads[-1].SetBottomMargin(0.022);
			self.Pads[-1].SetLeftMargin(spaceleft);
			self.Pads[-1].SetRightMargin(spaceright);
			self.Pads[-1].Draw();
			self.Canvases[-1].cd();
			self.Pads.append(TPad("divpad", "divpad", 0, 0, 1.,split))
			self.Pads[-1].SetTopMargin(0.0);
			self.Pads[-1].SetBottomMargin(0.4);
			self.Pads[-1].SetLeftMargin(spaceleft);
			self.Pads[-1].SetRightMargin(spaceright);
			self.Pads[-1].Draw();
			self.Pads[-2].cd();

		if len(title) > 0:
			ROOT.gPad.SetTopMargin(0.1)
		self.legend(legtitle);
		if ratio == True:
			self.cumaddhist[-1].GetXaxis().SetTitleOffset(5.)
			self.cumaddhist[-1].GetXaxis().SetLabelOffset(5.)


		for hist in reversed(self.cumaddhist):
			hist.Rebin(rebin)
			hist.Draw(options)

			mymax = max(mymax, hist.GetMaximum())
			if rangemin != 0 or rangemax != 0:
				hist.GetXaxis().SetRangeUser(rangemin, rangemax)
			if 'same' not in options:
				units = re.findall('\[.*\]', hist.GetXaxis().GetTitle())
				unit = ''
				if len(units) == 1:
					unit = units[0][1:-1]
				if ytitle == '':
					if len(hist.GetYaxis().GetTitle()) == 0:
						ytitle = 'Events'
					else:
						ytitle = hist.GetYaxis().GetTitle()
						#ytitle = ytitle.lower()
				if printbinwidth == True:
					hist.GetYaxis().SetTitle(ytitle + ' / {0:g}'.format(hist.GetXaxis().GetBinWidth(1)) + ' ' + unit)
				else:
					hist.GetYaxis().SetTitle(ytitle)
				if(xtitle != ''):
					hist.GetXaxis().SetTitle(xtitle)
				options += ' same'
		for op in self.Otherplots:
			op.Rebin(rebin)
			op.SetLineWidth(2)
			#op.Draw('sameE0')//close box
			mymax = max(mymax, op.GetMaximum())
		if len(self.DAplots) == 1:
			self.DAplots[0].Rebin(rebin)
			self.DAplots[0].SetMarkerStyle(20)
			self.DAplots[0].SetMarkerSize(1.1)
			self.DAplots[0].SetLineWidth(2)
			self.DAplots[0].Draw('E1X0same')
			mymax = max(mymax, self.DAplots[0].GetMaximum())
		if len(self.DAplots) == 1:
			self.lg.AddEntry(self.DAplots[0], self.DAplots[0].GetTitle(), 'p')
		for hist in reversed(self.cumaddhist):
			if len(hist.GetTitle()) != 0:
				self.lg.AddEntry(hist, hist.GetTitle(), 'f')
		for op in self.Otherplots:
			self.lg.AddEntry(op, op.GetTitle(), 'l')
		self.lg.Draw()
		self.settitle(title)
		self.setchannel()
		self.cmstext()
		if logy == False:
			self.cumaddhist[-1].GetYaxis().SetRangeUser(0, mymax*1.5)
		if logy == True:
			self.cumaddhist[-1].GetYaxis().SetRangeUser(10, mymax*50)
			self.Pads[-2].SetLogy(True)


		self.Pads[-2].RedrawAxis();
		if ratio == True:
			self.Pads[-1].cd();
			self.Pads[-1].SetGridy()
			self.DIVplots.append(TH1D(self.Otherplots[0]))
			self.DIVplots.append(TH1D(self.Otherplots[1]))
			if(xtitle != ''):
				self.DIVplots[-1].GetXaxis().SetTitle(xtitle)
			#self.DIVplots[-1].Divide(self.cumaddhist[-1])
			for b in range(1, self.DIVplots[-1].GetNbinsX()+1):
				if(self.cumaddhist[-1].GetBinContent(b) > 0.):
					divval = self.DIVplots[-1].GetBinContent(b)/self.cumaddhist[-1].GetBinContent(b)
					divvalerr = self.DIVplots[-1].GetBinError(b)/self.cumaddhist[-1].GetBinContent(b)
					self.DIVplots[-1].SetBinContent(b, divval)
					#self.DIVplots[-1].SetBinError(b, divvalerr)
					self.DIVplots[-1].SetBinError(b, math.sqrt(divvalerr**2 + (self.cumaddhist[-1].GetBinError(b)/self.cumaddhist[-1].GetBinContent(b))**2))
				else:
					self.DIVplots[-1].SetBinContent(b, 0.)
					self.DIVplots[-1].SetBinError(b, 0.)
			self.DIVplots[-1].SetMarkerSize(1.1)
			self.DIVplots[-1].Draw('E1X0same');
			self.DIVplots[-1].GetXaxis().SetTitleOffset(3)
			self.DIVplots[-1].GetYaxis().SetTitle('relative unc')
			self.DIVplots[-1].GetYaxis().SetTitleOffset(1.3)
			self.DIVplots[-1].GetYaxis().SetRangeUser(0.5, 1.5)
			self.DIVplots[-1].GetYaxis().SetNdivisions(105)
			if rangemin != 0 or rangemax != 0:
				self.DIVplots[-1].GetXaxis().SetRangeUser(rangemin, rangemax)
			self.DIVplots[-1].Draw('E1X0same');
		self.Pads[-1].RedrawAxis();


		return(self.Canvases[-1])

