import math, sys, re
from ROOT import TH1D, TGraphErrors, TGraphAsymmErrors, TFile, TCanvas, TLatex, TLegend, TF1, TMath, TPad
import ROOT
from array import array

#njets = '3j'
njets = sys.argv[3]

def settitle(title = '35.8 fb^{-1} (13 TeV)'):
	xpos = 1. - ROOT.gPad.GetRightMargin()
	ypos = 1. - ROOT.gPad.GetTopMargin()
	lxtitle = TLatex(0., 0., 'Z')
	lxtitle.SetNDC(True)
	lxtitle.SetTextFont(43)
	lxtitle.SetTextSize(30)
	lxtitle.SetTextAlign(31)
	lxtitle.DrawLatex(xpos, ypos+0.02, title)

#def setchannel(title = '#splitline{l+jets %n}' %njets):
def setchannel(title = 'l+jets, %s jets reconstruction' %njets):
	xpos = 1. - ROOT.gPad.GetRightMargin()
	ypos = 1. - ROOT.gPad.GetTopMargin()
	lxtitle = TLatex(0., 0., 'Z')
	lxtitle.SetNDC(True)
	lxtitle.SetTextFont(63)
	lxtitle.SetTextSize(25)
	lxtitle.SetTextAlign(13)
	lxtitle.DrawLatex(0.04, ypos-0.03, title)

def cmstext(add = ''):
	xpos = ROOT.gPad.GetLeftMargin()
	ypos = 1.-ROOT.gPad.GetTopMargin()
	lx = TLatex(0., 0., 'Z')
	lx.SetNDC(True)
	lx.SetTextFont(63)
	lx.SetTextSize(30)
	lx.SetTextAlign(13)
	lx.DrawLatex(xpos+0.06, ypos+0.02, 'CMS')
	lx2 = TLatex(0., 0., 'Z')
	lx2.SetNDC(True)
	lx2.SetTextFont(53)
	lx2.SetTextSize(25)
	lx2.SetTextAlign(13)
	#lx2.DrawLatex(xpos+0.04, ypos-0.08, '#it{Preliminary}')
	lx2.DrawLatex(xpos+0.08, ypos+0.02, '#it{Preliminary}')

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


class plotTogether:
	tfiles = {}
	lgx = 0.65
	lgy = 0.4

	def __init__(self):
		self.unctitle = ''
		self.MCplots = []
		self.DAplots = []
		self.NOplots = []
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

	njetstr = sys.argv[3][0]+' jets' if '6' not in sys.argv[3] and 'up' not in sys.argv[3] else '#geq'+sys.argv[3][0]+' jets'
	def setchannel(self, title = 'e/#mu+jets, '+njetstr):
	#def setchannel(self, title = 'e/#mu+jets, %s jets' %njets[0]):
	#def setchannel(self, title = 'e/#mu+jets, #geq%s jets' %njets[0]):
	#def setchannel(self, title = 'e/#mu+jets, #geq%s jets in SB' %njets[0]):
	#def setchannel(self, title = 'l+jets'):
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
		self.lx.DrawLatex(xpos+0.04, ypos-0.03, 'CMS')
		self.lx2 = TLatex(0., 0., 'Z')
		self.lx2.SetNDC(True)
		self.lx2.SetTextFont(52)
		self.lx2.SetTextSize(0.05)
		self.lx2.SetTextAlign(13)
		self.lx2.DrawLatex(xpos+0.04, ypos-0.10, 'Preliminary')

	def settitle(self, title):
		xpos = 1. - ROOT.gPad.GetRightMargin()
		ypos = 1. - ROOT.gPad.GetTopMargin()
		self.lxtitle = TLatex(0., 0., 'Z')
		self.lxtitle.SetNDC(True)
		self.lxtitle.SetTextFont(42)
		self.lxtitle.SetTextSize(0.07)
		self.lxtitle.SetTextAlign(31)
		self.lxtitle.DrawLatex(xpos, ypos+0.02, title)

	def printLatexYieldTable(self, fname='yield_table.tex'):
	        ''' This function will print a table based on how the addMCplot and addDAplot functions were called.
	        It will sum over all files that have no title, and assing them to the previous title. So for example:
	           plot[p].addMCplot(DYfile, p, 'V+Jets', DYscale, ROOT.kGreen+2, projection = pro)
	           plot[p].addMCplot(Wfile, p, '', Wscale, ROOT.kGreen+2, projection = pro)
	        will create a category 'V+Jets' that includes DY and W+jets events stored in DYfile and Wfile.
	        A call to this function should be added just after a call to drawAddWithRatio for that particular histogram, and then, for example:
	           can = plot[p].drawAddWithRatio( .......
	           if (p == "RECO/all_njets"):
	                 plot[p].printLatexYieldTable('totyield_table.tex'
	        '''
		MCtot = 0.
		MCtot_err = 0.
		category_yield = []
		category_err = []
		category_title = []
		cat_yield = 0.
		cat_err = 0.
		for index, hist in enumerate(self.MCplots):
			if hist.GetTitle() != '':
			     category_title.append(hist.GetTitle())
			     cat_yield = 0.
			     cat_err = 0.
			err = ROOT.Double(0)
			# Make sure you run this over a histogram with known under- and overflows!
			# For example number of jets, or MET, anything that hasn't been initialized to -9
			events = hist.IntegralAndError(0,hist.GetNbinsX()+1,err)
			#events = hist.Integral()
			cat_yield += events
			cat_err = math.sqrt(cat_err*cat_err + err*err)
			if len(self.MCplots) == index+1 or self.MCplots[index+1].GetTitle() != ''  :
			      category_yield.append(cat_yield)
			      category_err.append(cat_err)
			MCtot += events
			MCtot_err = math.sqrt(MCtot_err*MCtot_err+err*err)

		# Ready to print the numbers, first open the latex file:
		latexfile = open(fname, "w")
		latexfile.write("\\begin{tabular}{l|r@{$\\pm$}l} \\hline \n")     # r@{$\pm$}l
                latexfile.write("%-12s & %20s \\\\ \\hline \n" % ('Source','\multicolumn{2}{c}{Yield}'))
		for i in range(len(category_title)):
		     print "%-12s %5.1f +- %4.1f" % (category_title[i],category_yield[i],category_err[i])
		     latexfile.write("%-12s & %5.1f & %4.1f \\\\ \n" % (category_title[i],category_yield[i],category_err[i]))

		print "%-12s %5.1f +- %4.1f" % ('BKG SUM ', MCtot, MCtot_err)
		latexfile.write("%-12s & %5.1f & %4.1f\\\\ \\hline \n" % ('BKG SUM ', MCtot, MCtot_err))

		DAtot=0.
		for hist in self.DAplots:
		        DAtot +=  hist.Integral()
		print "%-12s %5i" % ('Data ', DAtot)
	        latexfile.write("%-12s & \multicolumn{2}{c}{%5i} \\\\ \n" % ('Data ', DAtot))
	        latexfile.write("\\end{tabular} \n")
                latexfile.close()
                print "Wrote LaTeX table with yields in: ", fname
                print "The errors are obtained from ROOT::TH1::IntegralAndError() and added in quadrature per category"
		return [DAtot, MCtot, MCtot_err]

	def addMCplot(self, filename, histpath, title, scale, color, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
			print "little fox", self.tfiles[filename], histpath
		if projection == 'Y':
			self.MCplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.MCplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.MCplots.append(TH1D(self.tfiles[filename].Get(histpath)))
			print "fox"
		self.MCplots[-1].SetFillColor(color)
		self.MCplots[-1].SetLineColor(color)
		#self.MCplots[-1].Scale(scale, 'width')
		self.MCplots[-1].Scale(scale)
		self.MCplots[-1].SetTitle(title)

	def setUncTitle(self, unctitle):
		self.unctitle = unctitle

	def addUncerHist(self, fcentral, datascale, datascaledw, datascaleup, ferrdown, ferrup, hist, scaleUnc, projection = '', Norm = False, AsymmetricError = False):
		if self.unc == False:
			self.herr = TH1D(self.DAplots[-1])
			self.herr.Reset()
			self.herr.SetName('err')
			if AsymmetricError:
				self.herrup = TH1D(self.DAplots[-1])
				self.herrup.Reset()
				self.herrup.SetName('errup')
				self.herrdw = TH1D(self.DAplots[-1])
				self.herrdw.Reset()
				self.herrdw.SetName('errdw')
			self.unc = True
		if fcentral not in self.tfiles:
			self.tfiles[fcentral] = TFile(fcentral, 'read')
		if ferrdown not in self.tfiles:
			self.tfiles[ferrdown] = TFile(ferrdown, 'read')
		if ferrup not in self.tfiles:
			self.tfiles[ferrup] = TFile(ferrup, 'read')

		hcen = self.tfiles[fcentral].Get(hist)
		hdown = self.tfiles[ferrdown].Get(hist)
		hup = self.tfiles[ferrup].Get(hist)
		print "normalization precheck:", hcen.Integral(), hdown.Integral(), hup.Integral(), datascale, datascaleup, datascaledw
		if Norm and (hup.Integral() != 0. and hdown.Integral() != 0.):
			hcen.Scale(datascale)
			hup.Scale(datascaleup)
			hdown.Scale(datascaledw)
			hup.Scale(hcen.Integral()/hup.Integral())
			hdown.Scale(hcen.Integral()/hdown.Integral())
		else:
			hcen.Scale(datascale)
			hup.Scale(datascaleup)
			hdown.Scale(datascaledw)
		print "normalization check:", hcen.Integral(), hdown.Integral(), hup.Integral()
		if projection == 'Y':
			hcen = TH1D(hcen.ProjectionY())
			hdown = TH1D(hdown.ProjectionY())
			hup = TH1D(hup.ProjectionY())
		if projection == 'X':
			hcen = TH1D(hcen.ProjectionX())
			hdown = TH1D(hdown.ProjectionX())
			hup = TH1D(hup.ProjectionX())

		self.cumaddhist = []
		self.cumaddhist.append(TH1D(self.MCplots[0]))
		for hist in self.MCplots[1:]:
			self.cumaddhist.append(TH1D(self.cumaddhist[-1]))
			self.cumaddhist[-1].Add(hist)

		for b in range(1, 1+self.herr.GetNbinsX()):
			cen = hcen.GetBinContent(b)
			tot = self.cumaddhist[-1].GetBinContent(b)
			if cen == 0 or tot == 0:
				continue
			up = hup.GetBinContent(b)
			down = hdown.GetBinContent(b)
			old = self.herr.GetBinContent(b)

			errA = (up-cen)*scaleUnc/cen
			errB = (down-cen)*scaleUnc/cen
			err = (abs(errA) + abs(errB))/2.
			#err = max(abs(errA), abs(errB))
			compWeight = cen/tot

			self.herr.SetBinContent(b, math.sqrt(old**2 + err**2*compWeight**2))
			#self.herr.SetBinContent(b, math.sqrt(old**2 + err**2))
			#print scaleUnc

			if AsymmetricError:
				old = self.herrup.GetBinContent(b)
				self.herrup.SetBinContent(b, math.sqrt(old**2 + errA**2*compWeight**2))
				old = self.herrdw.GetBinContent(b)
				self.herrdw.SetBinContent(b, math.sqrt(old**2 + errB**2*compWeight**2))

		#Those are important !!!
		hcen.Scale(1/datascale)
		hup.Scale(1/datascaleup)
		hdown.Scale(1/datascaledw)
		if Norm and (hup.Integral() != 0 and hdown.Integral() != 0):
			hup.Scale(1/(hcen.Integral()/hup.Integral()))
			hdown.Scale(1/(hcen.Integral()/hdown.Integral()))


	def addUncerVal(self, val):
		if self.unc == False:
			self.herr = TH1D(self.DAplots[-1])
			self.herr.Reset()
			self.herr.SetName('err')
			self.unc = True
		for b in range(1, 1+self.herr.GetNbinsX()):
			old = self.herr.GetBinContent(b)
			self.herr.SetBinContent(b, math.sqrt(old**2 + val**2))

	def addUncerValBins(self, valist):
		if self.unc == False:
			self.herr = TH1D(self.DAplots[-1])
			self.herr.Reset()
			self.herr.SetName('err')
			self.unc = True
		for b in range(len(valist)):
			old = self.herr.GetBinContent(b+4)
			print old, valist[b], math.sqrt(old**2 + valist[b]**2), b+1
			self.herr.SetBinContent(b+4, math.sqrt(old**2 + valist[b]**2))

	#def addDAplot(self, filename, histpath, title, projection = '', scale = 1.):#close box
	def addDAplot(self, filename, histpath, title, scale, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.DAplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.DAplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.DAplots.append(TH1D(self.tfiles[filename].Get(histpath)))
		self.DAplots[-1].SetTitle(title)
		self.DAplots[-1].Scale(scale)
		#self.DAplots[-1].Scale(1., 'width')
		self.DAplots[-1].Scale(1.)#//close box

	def addOtherplot(self, filename, histpath, title, scale, color, style=1, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.Otherplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.Otherplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.Otherplots.append(TH1D(self.tfiles[filename].Get(histpath)))
		#self.NOplots[-1].SetFillColor(color)
		self.Otherplots[-1].SetLineColor(color)
		self.Otherplots[-1].SetLineStyle(style)
		self.Otherplots[-1].SetTitle(title)
		self.Otherplots[-1].Scale(scale)

	def addNormplot(self, filename, histpath, title, color, projection = ''):
		if filename not in self.tfiles:
			self.tfiles[filename] = TFile(filename, 'read')
		if projection == 'Y':
			self.NOplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionY()))
		elif projection == 'X':
			self.NOplots.append(TH1D(self.tfiles[filename].Get(histpath).ProjectionX()))
		else:
			self.NOplots.append(TH1D(self.tfiles[filename].Get(histpath)))
		#self.NOplots[-1].SetFillColor(color)
		self.NOplots[-1].SetLineColor(color)
		self.NOplots[-1].SetTitle(title)

	def drawAddWithRatio(self, options = 'hist', rebin = 1, legtitle = '', title = '', ratio = False, rangemin = 0., rangemax = 0., printbinwidth = True, xtitle = '', ytitle = '', logy = False, xlabels = [], AsymmetricError = False):
		self.cumaddhist = []
		self.cumaddhist.append(TH1D(self.MCplots[0]))
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
		if len(xlabels) != 0:
			b=0
			for label in xlabels:
				b+=1
				self.cumaddhist[-1].GetXaxis().SetBinLabel(b, label)
		if ratio == True:
			self.cumaddhist[-1].GetXaxis().SetTitleOffset(5.)
			self.cumaddhist[-1].GetXaxis().SetLabelOffset(5.)


		xList, yList = array('d'), array('d')
		errleftList, errightList = array('d'), array('d')
		errupList, errdwList = array('d'), array('d')
		relupList, reldwList = array('d'), array('d')

		for hist in reversed(self.cumaddhist):
			hist.Rebin(rebin)
			hist.Draw(options)

			mymax = max(mymax, hist.GetMaximum())
			if rangemin != 0 or rangemax != 0:
				hist.GetXaxis().SetRangeUser(rangemin, rangemax)
			if 'same' not in options:
				if self.unc:
					self.herr.Rebin(rebin)
					self.herr.Scale(1./rebin)
					self.errprint = TH1D(hist)
					self.errprint.SetName('errprint')
					for b in range(1, self.errprint.GetNbinsX()+1):
						self.errprint.SetBinError(b, self.herr.GetBinContent(b)*hist.GetBinContent(b))

					self.errprint.SetFillColor(1)
					self.errprint.SetLineColor(1)
					self.errprint.SetLineWidth(0)
					self.errprint.SetFillStyle(3354)
					#self.errprint.SetFillStyle(3344)
					self.errprint.Draw('E2same')#//close box

					if AsymmetricError:
						self.herrup.Rebin(rebin)
						self.herrup.Scale(1./rebin)
						self.herrdw.Rebin(rebin)
						self.herrdw.Scale(1./rebin)
						#self.DAplots[0].Rebin(rebin)

						for b in range(1, 1+self.herr.GetNbinsX()):
							xList.append(self.cumaddhist[-1].GetBinCenter(b))
							yList.append(self.cumaddhist[-1].GetBinContent(b))
							#yList.append(self.DAplots[0].GetBinContent(b))
							errleftList.append(self.cumaddhist[-1].GetXaxis().GetBinCenter(b) - self.cumaddhist[-1].GetXaxis().GetBinLowEdge(b))
							errightList.append(self.cumaddhist[-1].GetXaxis().GetBinUpEdge(b) - self.cumaddhist[-1].GetXaxis().GetBinCenter(b))
							#errupList.append(self.herrup.GetBinContent(b)*self.cumaddhist[-1].GetBinContent(b))
							#errdwList.append(self.herrdw.GetBinContent(b)*self.cumaddhist[-1].GetBinContent(b))
							errupList.append(self.herrup.GetBinContent(b)*self.DAplots[0].GetBinContent(b))
							errdwList.append(self.herrdw.GetBinContent(b)*self.DAplots[0].GetBinContent(b))
							relupList.append(self.herrup.GetBinContent(b))
							reldwList.append(self.herrdw.GetBinContent(b))

						self.gerr = TGraphAsymmErrors(len(xList),xList,yList,errleftList,errightList,errdwList,errupList)
						self.gerr.SetName('gerr')


						self.gerr.SetFillColor(1)
						self.gerr.SetLineColor(1)
						self.gerr.SetLineWidth(0)
						self.gerr.SetFillStyle(3354)
						self.gerr.Draw('E2same')#//close box
					#else:
						#self.errprint.Draw('E2same')#//close box


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
		#if not AsymmetricError:
		#	self.errprint.Draw('E2same')#//close box

		for np in self.NOplots:
			np.Rebin(rebin)
			np.Scale(self.DAplots[0].Integral()/np.Integral())
			np.SetLineWidth(2)
			np.Draw('sameE0')#//close box
			mymax = max(mymax, np.GetMaximum())
		for op in self.Otherplots:
			op.Rebin(rebin)
			op.SetLineWidth(2)
			op.Draw('sameE0')#//close box
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
		for np in self.NOplots:
			self.lg.AddEntry(np, np.GetTitle()+' (Scaled)', 'l')
		for op in self.Otherplots:
			self.lg.AddEntry(op, op.GetTitle(), 'l')
		if len(self.unctitle) != 0: self.lg.AddEntry(self.errprint, self.unctitle, 'f')
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
			self.DIVplots.append(TH1D(self.DAplots[0]))
			if(xtitle != ''):
				self.DIVplots[-1].GetXaxis().SetTitle(xtitle)
			#self.DIVplots[-1].Divide(self.cumaddhist[-1])
			printList = []
			for b in range(1, self.DIVplots[-1].GetNbinsX()+1):
				if(self.cumaddhist[-1].GetBinContent(b) > 0.):
					divval = self.DIVplots[-1].GetBinContent(b)/self.cumaddhist[-1].GetBinContent(b)
					divvalerr = self.DIVplots[-1].GetBinError(b)/self.cumaddhist[-1].GetBinContent(b)
					printList.append(divval)
					self.DIVplots[-1].SetBinContent(b, divval)
					#self.DIVplots[-1].SetBinError(b, divvalerr)
					self.DIVplots[-1].SetBinError(b, math.sqrt(divvalerr**2 + (self.cumaddhist[-1].GetBinError(b)/self.cumaddhist[-1].GetBinContent(b))**2))
				else:
					printList.append(0)
					self.DIVplots[-1].SetBinContent(b, 0.)
					self.DIVplots[-1].SetBinError(b, 0.)
			print printList
			self.DIVplots[-1].SetMarkerSize(1.1)
			if len(xlabels) != 0:
				b=0
				for label in xlabels:
					b+=1
					self.DIVplots[-1].GetXaxis().SetBinLabel(b, label)
			self.DIVplots[-1].Draw('E1X0same');
			self.DIVplots[-1].GetXaxis().SetTitleOffset(3)
			self.DIVplots[-1].GetYaxis().SetTitle('#frac{Data}{MC}')
			self.DIVplots[-1].GetYaxis().SetTitleOffset(1.3)
			self.DIVplots[-1].GetYaxis().SetRangeUser(0.5, 1.5)
			self.DIVplots[-1].GetYaxis().SetNdivisions(105)
			if rangemin != 0 or rangemax != 0:
				self.DIVplots[-1].GetXaxis().SetRangeUser(rangemin, rangemax)
			if self.unc:
				self.errprintratio = TH1D(self.herr)
				for b in range(1, self.errprintratio.GetNbinsX()+1):
					self.errprintratio.SetBinError(b, self.herr.GetBinContent(b))
					self.errprintratio.SetBinContent(b, 1.)
				self.errprintratio.SetFillColor(1)
				#self.errprintratio.SetFillStyle(3002)
				self.errprintratio.SetFillStyle(3354)
				#self.errprintratio.Draw('E2same')#//close box

				if AsymmetricError:
					self.gerratio = TGraphAsymmErrors(len(xList),xList,array('d',[1]*len(xList)),errleftList,errightList,reldwList,relupList)
					self.gerratio.SetFillColor(1)
					self.gerratio.SetFillStyle(3354)
					self.gerratio.Draw('E2same')
				else:
					self.errprintratio.Draw('E2same')#//close box

			self.DIVplots[-1].Draw('E1X0same');
		self.Pads[-1].RedrawAxis();


		return(self.Canvases[-1])


