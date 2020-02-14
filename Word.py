class Word():
  """docstring for Word"""
  def __init__(self, text: str, start_time: float, end_time: float):
    assert isinstance(text, str), "text should be string."
    assert isinstance(start_time, float) and isinstance(end_time, float), "Start time and end time should be float values."
    
    self.text = text
    self.start_time = start_time
    self.end_time = end_time 

  def __str__(self):
    return "Word(text='{}', start_time={}s, end_time={}s)".format(self.text, self.start_time, self.end_time)

  def __len__(self):
    return self.end_time - self.start_time