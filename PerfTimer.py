import time

class PerfTimer():
  def __init__(self) -> None:
    self.timer = []
  def init(self):
    self.timer.append(time.perf_counter())
  def log(self, title = 'log'):
    print(title + ':', time.perf_counter() - self.timer.pop())