#!/usr/bin/env python

import subprocess

cPath = '/pnfs/cms/WAX/11/store/user/cmsdas/2014/TopXSecLongExercise/EDMNtuples/skhalil'
eosPath = '/eos/uscms/store/user/cmsdas/2013/TopXSecLongExercise/EDMNtuples/skhalil'

options = [
   [cPath+'/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/EDMNtuples_53x/1871c98a9e831ed6f37b496e27310762',  'ttbar_skim_files_8TeV'],i
   [cPath+'/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/EDMNtuples_53x/1871c98a9e831ed6f37b496e27310762',  'wjets_skim_files_8TeV'],
   [cPath+'/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/EDMNtuples_53x/1871c98a9e831ed6f37b496e27310762',  'zjets_skim_files_8TeV'],
   [cPath+'/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/EDMNtuples_53x/1871c98a9e831ed6f37b496e27310762',  'tbar_skim_files_8TeV'],
   [cPath+'/T_t-channel_TuneZ2star_8TeV-powheg-tauola/EDMNtuples_53x/1871c98a9e831ed6f37b496e27310762',  't_skim_files_8TeV'],
   [cPath+'/ZprimeFiles/M1500GeV_W15GeV', 'zprime_M1500GeV_W15GeV_files_8TeV'],
   [cPath+'/ZprimeFiles/M1250GeV_W12p5GeV', 'zprime_M1250GeV_W12p5GeV_files_8TeV'],
   [cPath+'/ZprimeFiles/M2000GeV_W20GeV', 'zprime_M2000GeV_W20GeV_files_8TeV'],
   [eosPath+'/SingleMu/Data-Run2012A-13Jul2012-v1/7080dea0b2be3a0adb5bc6fa54bb531c', 'mu_Run2012A-13Jul2012-v1_skim_files_8TeV'],
   [eosPath+'/SingleMu/Data-Run2012A-06Aug2012-v1/7080dea0b2be3a0adb5bc6fa54bb531c', 'mu_Run2012A-06Aug2012-v1_skim_files_8TeV'],
   [eosPath+'/SingleMu/Data-Run2012C-PromptReco-v2-c/7080dea0b2be3a0adb5bc6fa54bb531c', 'mu_Run2012C-PromptReco-v2-c_skim_files_8TeV'],
   [eosPath+'/SingleMu/Data-Run2012B-13Jul2012-v1-try2/7080dea0b2be3a0adb5bc6fa54bb531c','mu_Run2012B-13Jul2012-v1_skim_files_8TeV'],
    ]
command = 'python listFiles.py --path={0:s} --outputText={1:s} '

for option in options :
    
    s = command.format(option[0], option[1])
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    
    subprocess.call( [s, ""], shell=True )
    
