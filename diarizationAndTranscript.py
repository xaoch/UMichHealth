from pydub import AudioSegment
from pyannote.audio import Pipeline

spacermilli = 2000
spacer = AudioSegment.silent(duration=spacermilli)


audio = AudioSegment.from_wav("/scratch/xao1/UMichHealth/KEMK18/KEMK18_1.wav") #lecun1.wav

audio = spacer.append(audio, crossfade=0)

audio.export('audio.wav', format='wav')

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

DEMO_FILE = {'uri': 'blabla', 'audio': 'audio.wav'}
dz = pipeline(DEMO_FILE)
with open("diarization.txt", "w") as text_file:
    text_file.write(str(dz))

def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
  return s


import re

dzs = open('diarization.txt').read().splitlines()

groups = []
g = []
lastend = 0

for d in dzs:
    if g and (g[0].split()[-1] != d.split()[-1]):  # same speaker
        groups.append(g)
        g = []

    g.append(d)

    end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
    end = millisec(end)
    if (lastend > end):  # segment engulfed by a previous segment
        groups.append(g)
        g = []
    else:
        lastend = end
if g:
    groups.append(g)
print(*groups, sep='\n')

audio = AudioSegment.from_wav("audio.wav")
gidx = -1
for g in groups:
  start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
  end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
  start = millisec(start) #- spacermilli
  end = millisec(end)  #- spacermilli
  print(start, end)
  gidx += 1
  audio[start:end].export(str(gidx) + '.wav', format='wav')
import os

for i in range(gidx+1):
  os.system("whisper {str(i) + '.wav'} --language en --model large")