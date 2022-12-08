from nemo.collections.asr.parts.utils.speaker_utils import rttm_to_labels, labels_to_pyannote_object
import nemo.collections.asr as nemo_asr
import numpy as np
import os
from omegaconf import OmegaConf
from nemo.collections.asr.parts.utils.decoder_timestamps_utils import ASR_TIMESTAMPS
from nemo.collections.asr.parts.utils.diarization_utils import ASR_DIAR_OFFLINE
import sys
import getopt
import json
import nemo.collections.asr.parts.utils.decoder_timestamps_utils as decoder_timestamps_utils
from nemo.collections.asr.models import ClusteringDiarizer


def extract(inputfile, outputdirectory, rttmfile,speakers):

    data_dir=outputdirectory
    os.makedirs(data_dir, exist_ok=True)

    AUDIO_FILENAME = inputfile
    print("Audio File: ",AUDIO_FILENAME)
    RTTM_FILENAME = rttmfile
    print("RTTM File: ", RTTM_FILENAME)

    CONFIG = "/home/xao1/Code/UMichHealth/conf/oracle.yaml"
    cfg = OmegaConf.load(CONFIG)

    meta = {
        'audio_filepath': AUDIO_FILENAME,
        'offset': 0,
        'duration':None,
        'label': 'infer',
        'text': '-',
        'num_speakers': speakers,
        'rttm_filepath': RTTM_FILENAME,
        'uem_filepath' : None
    }
    with open(os.path.join(data_dir,'input_manifest.json'),'w') as fp:
        json.dump(meta,fp)
        fp.write('\n')
    cfg.diarizer.manifest_filepath = os.path.join(data_dir,'input_manifest.json')

    pretrained_speaker_model = 'titanet_large'
    cfg.diarizer.manifest_filepath = cfg.diarizer.manifest_filepath
    cfg.diarizer.out_dir = data_dir  # Directory to store intermediate files and prediction outputs
    cfg.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
    cfg.diarizer.oracle_vad = True  # ----> ORACLE VAD
    cfg.diarizer.clustering.parameters.oracle_num_speakers = False

    oracle_vad_clusdiar_model = ClusteringDiarizer(cfg=cfg)

    # And lets diarize
    oracle_vad_clusdiar_model.diarize()


def main(argv):
   inputfile = ''
   outputfile = ''
   speakers=5
   try:
      opts, args = getopt.getopt(argv,"hi:o:r:s:",["ifile=","ofile=","rttm=","speakers="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile> -s <speakers>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -o <outputfile> -s <speakers>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-r", "--rttm"):
         rttmfile = arg
      elif opt in ("-s", "--speakers"):
         speakers = arg
   print("Arguments: ",inputfile,outputfile,rttmfile,speakers)
   extract(inputfile,outputfile,rttmfile,speakers)

if __name__ == '__main__':
    main(sys.argv[1:])