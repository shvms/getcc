import subprocess
import os

'''
To RAW PCM s16e audio format.
ffmpeg -f s16le -acodec pcm_s16le -ar 16000 -ac 1 -i <input_file> <output_file>
Returns a tuple an AudioFile object & temp_status if successfull else raise an exception
temp_status is True when temp directory is created during the execution of this function 
and didn't exist previously.
'''
def to_raw_audio(input_file, output_file, log=False):
  TEMP = 'temp'
  
  if not (len(output_file) >= 4 and output_file[-4:] == '.raw'):
    output_file += '.raw'

  BASE_TEMP = os.path.join(os.path.dirname(os.path.realpath(__file__)), TEMP)
  SAMPLE_RATE = 16000
  NUMBER_OF_CHANNELS = 1
  FORMAT = 's16le'
  CODEC = 'pcm_s16le'

  input_file_full_path = os.path.realpath(input_file)
  output_file_full_path = os.path.join(BASE_TEMP, output_file)

  COMMAND = ['ffmpeg',
             '-y',
             '-i', input_file_full_path,
             '-f', FORMAT, 
             '-acodec', CODEC, 
             '-ar', str(SAMPLE_RATE), 
             '-ac', str(NUMBER_OF_CHANNELS),
             output_file_full_path]

  if not os.path.exists(BASE_TEMP):         # if temp folder doesn't exist then make one
    os.makedirs(TEMP)
    temp_status = True
  else:
    temp_status = False

  if not os.path.exists(input_file_full_path):
    raise FileNotFoundError(f"{input_file} not found.")

  try:
    output = subprocess.check_output(COMMAND, stderr=subprocess.STDOUT, universal_newlines=True)
    if log:
      print(output)
  except subprocess.CalledProcessError as err:
    raise Exception("Couldn't fetch raw audio. {}, {}".format(err.returncode, err.output))

  return (AudioFile(output_file_full_path, SAMPLE_RATE, NUMBER_OF_CHANNELS), temp_status)

'''
Gives conversion status as well as the path to the output file
'''
class AudioFile():
  def __init__(self, file_path: str, sample_rate: int, nchannel: int):
    assert isinstance(file_path, str), "file_path should be a string."
    assert isinstance(sample_rate, int), "sample_rate should be an integer."
    assert isinstance(nchannel, int), "number of channels should be an integer."

    self.file_path = file_path      # output_file designated.
    self.sample_rate = sample_rate
    self.nchannel = nchannel

  def __str__(self):
    return "AudioFile(file_path = '{}', sample_rate = {}, nchannel = {})".format(
      self.file_path, self.sample_rate, self.nchannel)

  def delete(self, temp_status: bool):
    os.remove(self.file_path)
    if (temp_status):
      os.rmdir(os.path.dirname(self.file_path))
    self.file_path = None

if __name__ == "__main__":
  audio, temp_status = to_raw_audio('privacy_cut.webm', 'privacy_cut')
  print(audio, temp_status)