from Word import Word
from math import ceil
import os

'''
Class responsible to handle subtitles generation
'''
class SubtitleHandler():
  def __init__(self, transcription: list):
    # length of transcription is not 0
    assert isinstance(transcription, list), "transcription should be a list of Word objects."
    assert isinstance(transcription[0], Word), "Each word in transcription should be of type Word."

    self.transcription = transcription

  '''
  H: hours        2 digits
  M: minutes      2 digits
  S: seconds      2 digits
  s: milliseconds 3 digits

  Example: H:M:S,s (SRT format)
  '''
  @staticmethod
  def __format_time(time: float, format_: str) -> str:
    assert isinstance(time, float), "time should be floating number"
    assert isinstance(format_, str), "format should be string"

    milliseconds = '{:.3f}'.format(round(time - int(time), 3))[2:]
    hours = (int(time) // 60) // 60
    minutes = (int(time) // 60) - hours * 60
    seconds = int(time) - minutes * 60 - hours * 60 * 60

    format_ = format_.replace('H', '{H:02d}').replace('M', '{M:02d}').replace('S', '{S:02d}').replace('s', '{s:s}')
    return format_.format(H = hours, M = minutes, S = seconds, s = milliseconds)

  '''
  Generates an SRT subtitles in `output_file`.
  Contains specified words per frame.
  '''
  def extract_srt(self, output_file, words_per_frame = 10):
    assert isinstance(output_file, str), "output_file is a file path. Must be string."
    assert isinstance(words_per_frame, int), "words_per_frame must be integer."

    base_path = os.path.realpath(os.path.dirname(output_file))
    if not os.path.exists(base_path):
      raise FileNotFoundError("'{}' directory does not exist.".format(base_path))

    # SRT format for time and text
    FORMAT_TIME = 'H:M:S,s'
    FRAME_TEXT = '{counter:d}\n{start_time:s} --> {end_time:s}\n{frame_words}\n\n'

    subtitle_text = ""
    frame_count = 1
    number_of_words = len(self.transcription)
    for i in range(ceil(number_of_words/words_per_frame)):
      start_word = i * words_per_frame
      end_word = ((i+1)*words_per_frame) if ((i+1)*words_per_frame) < number_of_words else number_of_words
      frame_words = self.transcription[start_word : end_word]
      subtitle_text += FRAME_TEXT.format(
        counter = frame_count,
        start_time = SubtitleHandler.__format_time(frame_words[0].start_time, FORMAT_TIME),
        end_time = SubtitleHandler.__format_time(frame_words[-1].end_time, FORMAT_TIME),
        frame_words = ' '.join([w.text for w in frame_words])
      )
      frame_count += 1
    
    with open(output_file, 'w') as f:
      f.write(subtitle_text)


if __name__ == "__main__":
  transcription = [Word("Hey", 0.0, 2.0), Word("there", 2.0, 3.0),
    Word("its me", 3.0, 6.0), Word("you remember?", 6.0, 10.0),
    Word("Me Carlos, Your brother?",10.0, 17.0), Word("You remember, right?",17.0, 20.0),
    Word("All", 20.0, 21.143), Word("I", 21.143, 21.987),
    Word("have?", 21.987, 23.0), Word("are", 23.0, 26.0),
    Word("negative", 26.0, 27.0), Word("thoughts", 27.0, 30.0)]
  sub_gen = SubtitleHandler(transcription)
  sub_gen.extract_srt('temp/test.srt')