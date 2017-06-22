#!/usr/bin/env python

from tasks.add_movie import GetMovieMetadata, GetMovieRecommendations
import gevent
import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)

TASKS = [
    GetMovieRecommendations,
    GetMovieMetadata,
]


def run_tasks():
    for task_class in TASKS:
        task = task_class()
        task.start()

if __name__ == "__main__":
    run_tasks()
    while True:
        gevent.sleep(30)

