import nemo.collections.asr as nemo_asr
import numpy as np
import librosa
import os
from omegaconf import OmegaConf
from nemo.collections.asr.parts.utils.decoder_timestamps_utils import ASR_TIMESTAMPS
from nemo.collections.asr.parts.utils.diarization_utils import ASR_DIAR_OFFLINE
import sys
import getopt
import json
import nemo.collections.asr.parts.utils.decoder_timestamps_utils as decoder_timestamps_utils


def extract(inputfile, outputdirectory, speakers):

    data_dir=outputdirectory
    os.makedirs(data_dir, exist_ok=True)

    AUDIO_FILENAME = inputfile
    print("Audio File: ",AUDIO_FILENAME)
    signal, sample_rate = librosa.load(AUDIO_FILENAME, sr=None)

    CONFIG = "/scratch/xao1/asr/offline_diarization_with_asr.yaml"
    cfg = OmegaConf.load(CONFIG)

    meta = {
        'audio_filepath': AUDIO_FILENAME,
        'offset': 0,
        'duration':None,
        'label': 'infer',
        'text': '-',
        'num_speakers': speakers,
        'rttm_filepath': None,
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
    cfg.diarizer.clustering.parameters.oracle_num_speakers = False

    # Using VAD generated from ASR timestamps
    cfg.diarizer.asr.model_path = 'QuartzNet15x5Base-En'
    cfg.diarizer.oracle_vad = False  # ----> Not using oracle VAD
    cfg.diarizer.asr.parameters.asr_based_vad = True
    cfg.diarizer.asr.parameters.threshold = 100  # ASR based VAD threshold: If 100, all silences under 1 sec are ignored.
    cfg.diarizer.asr.parameters.decoder_delay_in_sec = 0.2  # Decoder delay is compensated for 0.2 sec

    asr_ts_decoder = ASR_TIMESTAMPS(**cfg.diarizer)
    asr_model = asr_ts_decoder.set_asr_model()
    word_hyp, word_ts_hyp = asr_ts_decoder.run_ASR(asr_model)

    arpa_model_path = os.path.join('/scratch/xao1/asr/4gram_big.arpa')
    cfg.diarizer.asr.realigning_lm_parameters.arpa_language_model = arpa_model_path
    cfg.diarizer.asr.realigning_lm_parameters.logprob_diff_threshold = 1.2

    asr_diar_offline = ASR_DIAR_OFFLINE(**cfg.diarizer)
    asr_diar_offline.word_ts_anchor_offset = asr_ts_decoder.word_ts_anchor_offset

    diar_hyp, diar_score = asr_diar_offline.run_diarization(cfg, word_ts_hyp)

    asr_diar_offline.get_transcript_with_speaker_labels(diar_hyp, word_hyp, word_ts_hyp)

def main(argv):
   inputfile = ''
   outputfile = ''
   speakers=5
   try:
      opts, args = getopt.getopt(argv,"hi:o:s:",["ifile=","ofile=","speakers="])
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
      elif opt in ("-s", "--speakers"):
         speakers = arg
   print("Arguments: ",inputfile,outputfile,speakers)
   extract(inputfile,outputfile,speakers)

if __name__ == '__main__':
    main(sys.argv[1:])
#
# import nemo.collections.asr as nemo_asr
# import numpy as np
# import librosa
# import wget
# import nemo
# import glob
# import os
# from omegaconf import OmegaConf
# import shutil
# import json
# from nemo.collections.asr.parts.utils.decoder_timestamps_utils import ASR_TIMESTAMPS
# from nemo.collections.asr.parts.utils.diarization_utils import ASR_DIAR_OFFLINE
# import gzip
# import sys
# import getopt
# import importlib
# import nemo.collections.asr.parts.utils.decoder_timestamps_utils as decoder_timestamps_utils
# importlib.reload(decoder_timestamps_utils)
# import nemo.collections.asr.parts.utils.diarization_utils as diarization_utils
# importlib.reload(diarization_utils)
#
# def extract(inputfile, outputdirectory, speakers):
#     data_dir=outputdirectory
#     AUDIO_FILENAME = inputfile
#     print("Audio File: ",AUDIO_FILENAME)
#     signal, sample_rate = librosa.load(AUDIO_FILENAME, sr=None)
#     cfg = OmegaConf.load(CONFIG)
#     meta = {
#         'audio_filepath': AUDIO_FILENAME,
#         'offset': 0,
#         'duration':None,
#         'label': 'infer',
#         'text': '-',
#         'num_speakers': speakers,
#         'rttm_filepath': None,
#         'uem_filepath' : None
#     }
#     with open(os.path.join(data_dir,'input_manifest.json'),'w') as fp:
#         json.dump(meta,fp)
#         fp.write('\n')
#     cfg.diarizer.manifest_filepath = os.path.join(data_dir,'input_manifest.json')
#
#     pretrained_speaker_model='titanet_large'
#     cfg.diarizer.manifest_filepath = cfg.diarizer.manifest_filepath
#     cfg.diarizer.out_dir = data_dir #Directory to store intermediate files and prediction outputs
#     cfg.diarizer.speaker_embeddings.model_path = pretrained_speaker_model
#     cfg.diarizer.speaker_embeddings.parameters.window_length_in_sec = 1.5
#     cfg.diarizer.speaker_embeddings.parameters.shift_length_in_sec = 0.75
#     cfg.diarizer.clustering.parameters.oracle_num_speakers=False
#
#     # Using VAD generated from ASR timestamps
#     cfg.diarizer.asr.model_path = 'stt_en_conformer_ctc_large'
#     cfg.diarizer.oracle_vad = False # ----> Not using oracle VAD
#     cfg.diarizer.asr.parameters.asr_based_vad = True
#     cfg.diarizer.asr.parameters.threshold=100 # ASR based VAD threshold: If 100, all silences under 1 sec are ignored.
#     cfg.diarizer.asr.parameters.decoder_delay_in_sec=0.2 # Decoder delay is compensated for 0.2 sec
#
#     arpa_model_path = os.path.join('/scratch/xao1/asr/4gram_big.arpa')
#     cfg.diarizer.asr.ctc_decoder_parameters.pretrained_language_model = arpa_model_path
#
#     asr_ts_decoder = ASR_TIMESTAMPS(**cfg.diarizer)
#     asr_model = asr_ts_decoder.set_asr_model()
#     word_hyp, word_ts_hyp = asr_ts_decoder.run_ASR(asr_model)
#
#     cfg.diarizer.asr.realigning_lm_parameters.arpa_language_model = arpa_model_path
#     cfg.diarizer.asr.realigning_lm_parameters.logprob_diff_threshold = 1.2
#
#     # Create a new instance with realigning language model
#     asr_diar_offline = ASR_DIAR_OFFLINE(**cfg.diarizer)
#     asr_diar_offline.word_ts_anchor_offset = asr_ts_decoder.word_ts_anchor_offset
#     diar_hyp, diar_score = asr_diar_offline.run_diarization(cfg, word_ts_hyp)
#
#     asr_diar_offline.get_transcript_with_speaker_labels(diar_hyp, word_hyp, word_ts_hyp)
#
# def main(argv):
#    inputfile = ''
#    outputfile = ''
#    speakers=5
#    try:
#       opts, args = getopt.getopt(argv,"hi:o:s:",["ifile=","ofile=","speakers="])
#    except getopt.GetoptError:
#       print('test.py -i <inputfile> -o <outputfile> -s <speakers>')
#       sys.exit(2)
#    for opt, arg in opts:
#       if opt == '-h':
#          print('test.py -i <inputfile> -o <outputfile> -s <speakers>')
#          sys.exit()
#       elif opt in ("-i", "--ifile"):
#          inputfile = arg
#       elif opt in ("-o", "--ofile"):
#          outputfile = arg
#       elif opt in ("-s", "--speakers"):
#          speakers = arg
#    print("Arguments: ",inputfile,outputfile,speakers)
#    extract(inputfile,outputfile,speakers)
#
# if __name__ == '__main__':
#     main(sys.argv[1:])