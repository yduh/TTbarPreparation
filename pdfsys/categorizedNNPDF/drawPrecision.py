#!/usr/bin/python
import ROOT as r
import sys
from array import array

histName = 'ttsigst'

f = r.TFile("skim_pdf.root")
outfile = r.TFile('pdfT.root', "RECREATE")

for n, r in enumerate(sys.argv[2:]):
	print n, r
	Up = f.Get('%s_pdf%sUp' %(histName,r))
	Dw = f.Get('%s_pdf%sDown' %(histName,r))
	Up.Write('%s_pdf%sUp' %(histName,str(n+1)))
	Dw.Write('%s_pdf%sDown' %(histName,str(n+1)))

sumUp = f.Get('%s_pdfsumUp' %histName)
sumDw = f.Get('%s_pdfsumDown' %histName)
sumUp.Write('%s_pdfsumUp' %histName)
sumDw.Write('%s_pdfsumDown' %histName)

outfile.Close()


NFinal = 1 ,  14.2614621212 ,  14.0893717772
NFinal = 2 ,  14.2156669499 ,  14.0194319881
NFinal = 3 ,  6.59980394178 ,  6.69165637721
NFinal = 4 ,  6.77135889091 ,  6.8474073115
NFinal = 5 ,  6.77080362106 ,  6.84733517411
NFinal = 6 ,  8.95803484485 ,  9.45277419026


NFinal = 1 ,  14.2614621212 ,  14.0893717772
1 sets of PDF are remained!
NFinal = 2 ,  14.2156669499 ,  14.0194319881
1 sets of PDF are remained!

NFinal = 3 ,  6.59980394178 ,  6.69165637721
2 sets of PDF are remained!

NFinal = 4 ,  6.77135889091 ,  6.8474073115
3 sets of PDF are remained!
NFinal = 5 ,  6.77080362106 ,  6.84733517411
3 sets of PDF are remained!

NFinal = 6 ,  8.95803484485 ,  9.45277419026
4 sets of PDF are remained!

NFinal = 7 ,  9.018272167 ,  9.50289033964
5 sets of PDF are remained!
NFinal = 8 ,  9.04345713067 ,  9.53088828809
5 sets of PDF are remained!

NFinal = 9 ,  3.2129819144 ,  3.2374290342
6 sets of PDF are remained!

NFinal = 10 ,  3.23105486091 ,  3.25317905716
7 sets of PDF are remained!
NFinal = 11 ,  2.92786682531 ,  2.97171903057
7 sets of PDF are remained!

NFinal = 12 ,  2.92909425185 ,  2.97419759301
8 sets of PDF are remained!

NFinal = 13 ,  2.80590120318 ,  2.81111147966
9 sets of PDF are remained!
NFinal = 14 ,  2.79319211683 ,  2.79947313318
9 sets of PDF are remained!
NFinal = 15 ,  2.87087833346 ,  2.87265766072
9 sets of PDF are remained!
