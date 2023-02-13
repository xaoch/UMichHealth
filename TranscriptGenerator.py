import srt
from srt import Subtitle
import pandas as pd
from datetime import timedelta

df = pd.read_csv("D:\\Data\\UMichHealth\\HCAJ18_1.rttm",sep=" ",header=None)
df = df.iloc[:,[5,8,11]]
df = df.rename(columns={5:"Start",8:"Duration",11:"Speaker"})
print(df.head())


f = open("D:\\Data\\UMichHealth\\HCAJ18\\transcript_1\\HCAJ18_1.mp4.srt", "r")
subtitle_generator = srt.parse(f)
subtitles = list(subtitle_generator)

subtitlesIndex=0

def speakerName(speaker):
    if speaker=="speaker_0":
        return "Patient"
    elif speaker=="speaker_2":
        return "Doctor"
    elif speaker=="speaker_3":
        return "Social Worker"
    elif speaker=="speaker_4":
        return "Debriefer"
    else:
        return "Unknown"


def closeTime(reference, measured):
    if abs(reference-measured)<0.5:
        return True
    else:
        return False

def overlap(s1,e1,s2,e2):
    return max(0, min(e1, e2) - max(s1, s2))

newSubs=[]
subIndex=0
for index,row in df.iterrows():
    #print(row)
    speaker=row["Speaker"]
    start=row["Start"]
    if start>440:
        b=5+3
    duration=row["Duration"]
    end=start+duration
    if index<df.shape[0]-1:
        nextRow=df.iloc[index+1]
        startNext=nextRow["Start"]
        durationNext=nextRow["Duration"]
        endNext=startNext+durationNext

    line=subtitles[subtitlesIndex]
    startText=line.start.total_seconds()
    endText=line.end.total_seconds()
    durationText=endText-startText
    content=line.content

    if index<df.shape[0]:
        if(endText<start or (overlap(start,end,startText,endText)>0 and (overlap(start, end, startText, endText) >= overlap(startNext, endNext, startText, endText)))):
            while True:
                subIndex=subIndex+1
                newSubStart = timedelta(seconds=startText)
                newSubEnd = timedelta(seconds=endText)
                newSubs.append(Subtitle(index=subIndex, start=newSubStart, end=newSubEnd, content=speakerName(speaker)+": "+content))
                #print("{:.2f} - {:.2f} : {:.2f} - {:.2f} :: {}: {}".format(start,end,startText,endText,speaker,content))
                subtitlesIndex=subtitlesIndex+1
                if start>startNext:
                   break
                if subtitlesIndex < len(subtitles):
                    line = subtitles[subtitlesIndex]
                    startText = line.start.total_seconds()
                    endText = line.end.total_seconds()
                    durationText = endText - startText
                    content = line.content
                else:
                    break
                if not ((overlap(start, end, startText, endText) > 0) and (overlap(start, end, startText, endText) > overlap(startNext, endNext, startText, endText))):
                    break

    #print("Start {} - End {}: {}".format(row["Start"],row["Duration"],row["Speaker"]))

#for line in subtitles:
    #print(line.start.total_seconds())

newSubsText=srt.compose(newSubs)

sub_file = open("newSubs.srt", "w")
n = sub_file.write(newSubsText)
sub_file.close()