from array import array
import ROOT as r
import math

def quad(*xs):
	return math.sqrt(sum(x*x for x in xs))

def Absy(histogram, histoName, bin_arrayx, absbin_arrayy):
	new_histo = r.TH2D(histoName, histogram.GetTitle()+"abs", len(bin_arrayx)-1, array("d", bin_arrayx), len(absbin_arrayy)-1, array("d", absbin_arrayy))
	for x in range(new_histo.GetXaxis().GetNbins()):
		for absy in range(new_histo.GetYaxis().GetNbins()):
			yup = new_histo.GetYaxis().GetBinCenter(absy+1)
			ydown = - yup
			new_histo.SetBinContent(x+1, absy+1, histogram.GetBinContent(x+1, histogram.GetYaxis().FindFixBin(yup)) + histogram.GetBinContent(x+1, histogram.GetYaxis().FindFixBin(ydown)))
			#err = histogram.GetBinError(x+1, histogram.GetYaxis().FindFixBin(yup))**2 + histogram.GetBinError(x+1, histogram.GetYaxis().FindFixBin(ydown))**2
			#new_histo.SetBinError(x+1, absy+1, math.sqrt(err))
			new_histo.SetBinError(x+1, absy+1, quad(histogram.GetBinError(x+1,histogram.GetYaxis().FindFixBin(yup)),histogram.GetBinError(x+1,histogram.GetYaxis().FindFixBin(ydown))))
			#print yup, ydown
	return new_histo

def newRebin2D(histogram, histoName, bin_arrayx, bin_arrayy):
    'Rebin 2D histo with irregular bin size'
    #old binning
    oldbinx = [float(histogram.GetXaxis().GetBinLowEdge(1))]
    oldbiny = [float(histogram.GetYaxis().GetBinLowEdge(1))]
    oldbinx.extend(float(histogram.GetXaxis().GetBinUpEdge(x)) for x in xrange(1, histogram.GetNbinsX()+1))
    oldbiny.extend(float(histogram.GetYaxis().GetBinUpEdge(y)) for y in xrange(1, histogram.GetNbinsY()+1))

    #if new binninf is just one number and int, use it to rebin rather than as edges
    if len(bin_arrayx) == 1 and isinstance(bin_arrayx[0], int):
        nrebin = bin_arrayx[0]
        bin_arrayx = [j for i, j in enumerate(oldbinx) if i % nrebin == 0]
    if len(bin_arrayy) == 1 and isinstance(bin_arrayy[0], int):
        nrebin = bin_arrayy[0]
        bin_arrayy = [j for i, j in enumerate(oldbiny) if i % nrebin == 0]

    #create a clone with proper binning
    # from pdb import set_trace; set_trace()
    new_histo = r.TH2D(histoName, histogram.GetTitle(),
		len(bin_arrayx)-1, array("d", bin_arrayx),
		len(bin_arrayy)-1, array("d", bin_arrayy),
    )

    #check that new bins don't overlap on old edges
    for x in bin_arrayx:
        if x==0:
            if not any( abs((oldx)) < 10**-8 for oldx in oldbinx ):
                raise Exception('New bin edge in x axis %s does not match any old bin edge, operation not permitted' % x)
        else:
            if not any( abs((oldx / x)-1.) < 10**-8 for oldx in oldbinx ):
                raise Exception('New bin edge in x axis %s does not match any old bin edge, operation not permitted' % x)
    for y in bin_arrayy:
        if y ==0:
            if not any( abs((oldy) )< 10**-8 for oldy in oldbiny ):
                raise Exception('New bin edge in y axis %s does not match any old bin edge, operation not permitted' % y)
        else:
            if not any( abs((oldy / y)-1.) < 10**-8 for oldy in oldbiny ):
                raise Exception('New bin edge in y axis %s does not match any old bin edge, operation not permitted' % y)

    #fill the new histogram
    for x in xrange(0, histogram.GetNbinsX()+2 ):
        for y in xrange(0, histogram.GetNbinsY()+2 ):
            new_bin_x = new_histo.GetXaxis().FindFixBin(
                histogram.GetXaxis().GetBinCenter(x)
                )
            new_bin_y = new_histo.GetYaxis().FindFixBin(
                histogram.GetYaxis().GetBinCenter(y)
                )
            new_histo.SetBinContent(
                new_bin_x, new_bin_y,
                histogram.GetBinContent(x,y) +
                new_histo.GetBinContent(new_bin_x, new_bin_y)
                )
            new_histo.SetBinError(
                new_bin_x, new_bin_y,
                quad(
                    histogram.GetBinError(x,y),
                    new_histo.GetBinError(new_bin_x, new_bin_y)
                    )
                )
            #new_histo.Fill(
            #    histogram.GetXaxis().GetBinCenter(x),
            #    histogram.GetYaxis().GetBinCenter(y),
            #    histogram.GetBinContent(x,y)
            #    )

    new_histo.SetEntries( histogram.GetEntries() )
    return new_histo
