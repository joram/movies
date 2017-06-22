import gevent
import datetime
import time

class BaseTask(gevent.Greenlet):

  SECONDS = 5

  def __init__(self):
    gevent.Greenlet.__init__(self)
 
  def __str__(self):
    return 'BaseTask'
  
  def _run(self):

    while True:
      start = datetime.datetime.now()
      self.do()
      end = datetime.datetime.now()

      next_tick = start+datetime.timedelta(seconds=self.SECONDS)
      if end < next_tick:
        remaining = next_tick - end
        gevent.sleep(remaining.total_seconds())

  def do(self):
    print "tick for {} at {}".format(self.__str__(), datetime.datetime.now())

