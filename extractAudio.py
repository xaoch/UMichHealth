import moviepy.editor as mp
import sys
import getopt

def extract(video,output):
   my_clip = mp.VideoFileClip(video)
   my_clip.audio.write_audiofile(output,codec='pcm_s16le')
   print("Finished")


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   extract(inputfile,outputfile)

if __name__ == '__main__':
    main(sys.argv[1:])