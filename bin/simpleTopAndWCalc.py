#! /usr/bin/env python
import os
import glob
import math

from optparse import OptionParser

parser = OptionParser()


############################################
#            Job steering                  #
############################################

# Input inputFiles to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
parser.add_option('--inputFiles', metavar='F', type='string', action='store',
                  dest='inputFiles',
                  help='Input files')

parser.add_option('--txtfiles', metavar='F', type='string', action='store',
                  default = "",
                  dest='txtfiles',
                  help='Input txt files')

parser.add_option("--onDcache", action='store_true',
                  default=True,
                  dest="onDcache",
                  help="onDcache(1), onDcache(0)")

# Output name to use. 
parser.add_option('--outputFile', metavar='F', type='string', action='store',
                  default='shyft_fwlite.root',
                  dest='outputFile',
                  help='output file name')

# Sample name
parser.add_option('--sampleName', metavar='F', type='string', action='store',
                  default='Top',
                  dest='sampleName',
                  help='output name')

# Using MC info or not. For MC, truth information is accessed.
parser.add_option('--doMC', metavar='F', action='store_true',
                  default=False,
                  dest='doMC',
                  help='Check MC Information')

# Which lepton type to use
parser.add_option('--lepType', metavar='F', type='int', action='store',
                  default=0,
                  dest='lepType',
                  help='Lepton type. Options are 0 = muons, 1 = electrons')



(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

#infile = open( options.inputFiles )
#infileStr = infile.read().rstrip()

#print 'Getting files from this dir: ' + infileStr

# Get the file list. 
#files = glob.glob( infileStr )

# Get the file list.
if options.inputFiles:
    files = glob.glob( options.files )
    print 'getting files', files
elif options.txtfiles:
    files = []
    with open(options.txtfiles, 'r') as input_:
        for line in input_:
            files.append(line.strip())
else:
    files = []

print 'getting files: ', files

if options.onDcache:
        files = ["dcap://" + x for x in files]
        #print 'new files', *files, sep='\n'
        #print('new files', files[0], files[1], ..., sep='\n')

fname = options.txtfiles
fileN = fname[fname.rfind('/')+1:]
print files


# Create the output file. 
f = ROOT.TFile(options.outputFile, "recreate")
f.cd()


# Make histograms
print "Creating histograms"
secvtxMassHist = ROOT.TH1F('secvtxMassHist', "Secondary Vertex Mass", 150, 0., 5.0)
secvtxMassHistB = ROOT.TH1F('secvtxMassHistB', "Secondary Vertex Mass, b jets", 150, 0., 5.0)
secvtxMassHistC = ROOT.TH1F('secvtxMassHistC', "Secondary Vertex Mass, c jets", 150, 0., 5.0)
secvtxMassHistL = ROOT.TH1F('secvtxMassHistL', "Secondary Vertex Mass, udsg jets", 150, 0., 5.0)

jetPtHist = ROOT.TH1F('jetPtHist', 'Jet p_{T}', 150, 0., 600.)


############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
jetPtMin = 30.0
leadJetPtMin = 30.0
looseMuonIsoMax = 0.2
looseElectronIsoMax = 0.2
ssvheCut = 2.74


if options.lepType == 0 :
    muonPtMin = 45.0
    electronPtMin = 20.0
    metMin = 20.0
    lepStr = 'Mu'
else:
    muonPtMin = 35.0
    electronPtMin = 45.0
    metMin = 20.0
    lepStr = 'Ele'




events = Events (files)

# Make the entirety of the handles required for the
# analysis. 
postfix = ""


jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "mass" )
jetSecvtxMassHandle         = Handle( "std::vector<float>" )
jetSecvtxMassLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "secvtxMass" )
jetSSVHEHandle         = Handle( "std::vector<float>" )
jetSSVHELabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "ssvhe" )
jetFlavorHandle         = Handle( "std::vector<float>" )
jetFlavorLabel    = ( "pfShyftTupleJets" + lepStr +  postfix,   "flavor" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons"+  postfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons"+  postfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons"+  postfix,   "phi" )
muonNhIsoHandle         = Handle( "std::vector<float>" )
muonNhIsoLabel    = ( "pfShyftTupleMuons"+  postfix,   "nhIso" )
muonChIsoHandle         = Handle( "std::vector<float>" )
muonChIsoLabel    = ( "pfShyftTupleMuons"+  postfix,   "chIso" )
muonPhIsoHandle         = Handle( "std::vector<float>" )
muonPhIsoLabel    = ( "pfShyftTupleMuons"+  postfix,   "phIso" )
muonPuIsoHandle         = Handle( "std::vector<float>" )
muonPuIsoLabel    = ( "pfShyftTupleMuons"+  postfix,   "puIso" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons"+  postfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons"+  postfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons"+  postfix,   "phi" )
electronNhIsoHandle         = Handle( "std::vector<float>" )
electronNhIsoLabel    = ( "pfShyftTupleElectrons"+  postfix,   "nhIso" )
electronChIsoHandle         = Handle( "std::vector<float>" )
electronChIsoLabel    = ( "pfShyftTupleElectrons"+  postfix,   "chIso" )
electronPhIsoHandle         = Handle( "std::vector<float>" )
electronPhIsoLabel    = ( "pfShyftTupleElectrons"+  postfix,   "phIso" )
electronPuIsoHandle         = Handle( "std::vector<float>" )
electronPuIsoLabel    = ( "pfShyftTupleElectrons"+  postfix,   "puIso" )


metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMET" + lepStr +  postfix,   "pt" )
metPhiHandle = Handle( "std::vector<float>" )
metPhiLabel = ("pfShyftTupleMET" + lepStr +  postfix,   "phi" )

# Keep some timing information
nEventsAnalyzed = 0
nEventsPassed3Jets = 0
nEventsPassed1Tag = 0
timer = ROOT.TStopwatch()
timer.Start()

pairs = []

# some lorentz vectors to use:
q1 = ROOT.TLorentzVector()
q2 = ROOT.TLorentzVector()
b1 = ROOT.TLorentzVector()
b2 = ROOT.TLorentzVector()



# loop over events
count = 0
ntotal = events.size()
percentDone = 0.0
ipercentDone = 0
ipercentDoneLast = -1
print "Start looping"
for event in events:
    nEventsAnalyzed += 1
    ipercentDone = int(percentDone)
    if ipercentDone != ipercentDoneLast :
        ipercentDoneLast = ipercentDone
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.0f}%'.format(
            count, ntotal, ipercentDone )
    count = count + 1
    percentDone = float(count) / float(ntotal) * 100.0

    ################################################
    #   Require exactly one lepton (e or mu)
    #   ------------------------------------
    #      Our ntuples have both muon and electron
    #      events, and hence we must select events
    #      based on one or the other type. 
    #      To accomplish this we check the products
    #      for the type we're currently plotting
    #      (Mu or Ele), and check if the product is
    #      present. 
    ################################################
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        muonPts = None
    else :
        muonPts = muonPtHandle.product()
    event.getByLabel (electronPtLabel, electronPtHandle)
    if not electronPtHandle.isValid():
        electronPts = None
    else :
        electronPts = electronPtHandle.product()

    # If neither muons nor electrons are found, skip
    if muonPts is None and electronPts is None :
        continue
    # If we are looking for muons but none are found, skip
    if options.lepType == 0 and muonPts is None :
        continue
    # If we are looking for electrons but none are found, skip
    if options.lepType == 1 and electronPts is None :
        continue

    # Now get the MET
    event.getByLabel( metLabel, metHandle )
    metRaw = metHandle.product()[0]

    # If the MET is lower than our cut, skip
    if metRaw < metMin :
        continue


    ################################################
    #   Retrieve the jet 4-vector and plot the
    #   secondary vertex mass for tagged jets. 
    #   ------------------------------------
    #      The jet 4-vectors are large and hence
    #      take a long time to read out. If you don't
    #      need the other products (eta,phi,mass of jet)
    #      then don't read them out. 
    ################################################
    event.getByLabel( jetPtLabel, jetPtHandle )
    jetPts = jetPtHandle.product()
    event.getByLabel( jetEtaLabel, jetEtaHandle )
    jetEtas = jetEtaHandle.product()
    event.getByLabel( jetPhiLabel, jetPhiHandle )
    jetPhis = jetPhiHandle.product()
    event.getByLabel( jetMassLabel, jetMassHandle )
    jetMasses = jetMassHandle.product()
    event.getByLabel (jetSSVHELabel, jetSSVHEHandle)
    jetSSVHEs = jetSSVHEHandle.product()
    event.getByLabel( jetSecvtxMassLabel, jetSecvtxMassHandle )
    jetSecvtxMasses = jetSecvtxMassHandle.product()
    if options.doMC :
        event.getByLabel( jetFlavorLabel, jetFlavorHandle )
        jetFlavors = jetFlavorHandle.product()


    for ijetb1 in range(0,len(jetPts)) :  # this is the 'b' jet so only continue if tagged
        if jetSSVHEs[ijetb1] <  ssvheCut  :
            continue
        for ijetb2 in range(0,len(jetPts)): # this is the second 'b' jet so only continue if tagged...
            if ijetb1 == ijetb2 : #obviously should be different than the first jet
                continue
            if jetSSVHEs[ijetb2] <  ssvheCut :
                continue
            for ijetq1 in range(0,len(jetPts)) : # first possible jet from W->qq
                if ijetb1 == ijetq1 : 
                    continue
                if ijetb2 == ijetq1 :
                    continue
                for ijetq2 in range(0,len(jetPts)): # second possible jet from W->qq
                    if ijetq2 >= ijetq1 : # the >= sign here is to avoid double-counting - again to reduce the CPU-time
                        continue
                    if ijetb1 == ijetq2 :
                        continue
                    if ijetb2 == ijetq2 :
                        continue
                    # now you have selected three unique jets - fill the lorentz vectors to so it's easy to do some mass calculations
                    b1.SetPtEtaPhiM(jetPts[ijetb1],jetEtas[ijetb1],jetPhis[ijetb1],jetMasses[ijetb1])
                    q1.SetPtEtaPhiM(jetPts[ijetq1],jetEtas[ijetq1],jetPhis[ijetq1],jetMasses[ijetq1])
                    q2.SetPtEtaPhiM(jetPts[ijetq2],jetEtas[ijetq2],jetPhis[ijetq2],jetMasses[ijetq2])
                    print(" W mass : {0:6.2f} GeV/c2").format( (q1+q2).M() )
                    print(" t mass : {0:6.2f} GeV/c2").format( (b1+q1+q2).M() )
                

# Done processing the events!


# Stop our timer
timer.Stop()

# Print out our timing information
rtime = timer.RealTime(); # Real time (or "wall time")
ctime = timer.CpuTime(); # CPU time
print("Analyzed events: {0:6d}").format(nEventsAnalyzed)
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)

# "cd" to our output file
f.cd()

# Write our histogram
f.Write()

# Close it
f.Close()
