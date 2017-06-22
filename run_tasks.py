#!/usr/bin/env python

from tasks.add_movie import AddMovies
import gevent

TASKS = [
  AddMovies,
]

for task_class in TASKS:
  task = task_class()
  task.start()

while True:
  gevent.sleep(30)

