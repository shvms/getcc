import os
import functools
from Word import Word
from video_to_audio import AudioFile

def delete_audio_after_use(transcribe_func):
  @functools.wraps(transcribe_func)
  def wrapper(*args):
    assert isinstance(args[1], AudioFile), "Please pass the AudioFile object returned from 'to_raw_audio()'."
    assert args[1].file_path is not None, "This file already transcribed and deleted."
    assert isinstance(args[2], bool), "Please pass the temp_status returned from 'to_raw_audio()'."

    output = transcribe_func(args[0], args[1].file_path)

    # cleaning the mess
    args[1].delete(args[2])

    return output
  return wrapper

'''
Speech Recognition implemented using the recent Pocketsphinx class
RFC 5646 language tag to initialize the recognizer
'''
class SphinxRecognizer_PS():
  def __init__(self, language='en-US'):
    self.Pocketsphinx = __import__('pocketsphinx').Pocketsphinx
    self.language = language

    self.data_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pocketsphinx-data', self.language)
    self.acoustic_parameters_directory = os.path.join(self.data_directory, 'acoustic-model')
    self.language_model_directory = os.path.join(self.data_directory, 'language-model.lm.bin')
    self.phoneme_dict_directory = os.path.join(self.data_directory, 'pronounciation-dictionary.dict')

  '''
  Transcribes the give audio file
  Returns a list of Word object.
  '''
  @delete_audio_after_use
  def transcribe(self, audio_file: str) -> list:
    FPS = 100       # default frames per second
    config = {
      'hmm': os.path.join(self.data_directory, self.acoustic_parameters_directory),
      'lm': os.path.join(self.data_directory, self.language_model_directory),
      'dict': os.path.join(self.data_directory, self.phoneme_dict_directory)
    }

    ps = self.Pocketsphinx(**config)
    ps.decode(
      audio_file = os.path.join('temp', audio_file),
      no_search = False,
      full_utt = False
    )

    segments = ps.segments(detailed=True)
    if len(segments) == 0:
      raise Exception("Couldn't transcribe.")

    return [Word(w[0], w[2]/FPS, w[3]/FPS) for w in segments]