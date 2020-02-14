import argparse
import os

from video_to_audio import to_raw_audio
from SphinxRecognizer import SphinxRecognizer_PS
from subtitle_gen import SubtitleHandler

def getcc(input_file, output_file, language='en-US'):
  audio_output_file = "{}".format(os.path.basename(input_file) + '.raw')

  print(audio_output_file)
  print("Processing video...")
  audio, temp_status = to_raw_audio(input_file, audio_output_file)
  print(audio)
  print("temp_status = {}".format(temp_status))
  print("Processing done.")

  print("Transcribing...")
  r = SphinxRecognizer_PS(language=language)
  transcription = r.transcribe(audio, temp_status)
  print("Transcribing done.")

  print("Generating subtitles...")
  sh = SubtitleHandler(transcription)
  sh.extract_srt(output_file)
  print("Subtitles generated successfully.")


def main():
  parser = argparse.ArgumentParser(
    description="This tool lets you generate subtitles to a video."
  )
  #parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
  #  help='python getcc.py -input_file <input_file_path> -output_file <output_file_path> -lang <language>\nLangauge is optional and \'en-US\' is the default language.'
  #)
  parser.add_argument('input_file', help='Path to the input video file', type=str)
  parser.add_argument('output_file', help='Path to the output subtitle file', type=str)
  parser.add_argument('lang', help='Specify RFC 5646 langauge tag', type=str, default='en-US')
  args = parser.parse_args()

  getcc(args.input_file, args.output_file, args.lang)

if __name__ == '__main__':
  main()
