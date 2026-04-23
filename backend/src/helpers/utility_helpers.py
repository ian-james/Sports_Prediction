import time
import random


def random_sleep(min_sec=1.5, max_sec=4.0):
    """Sleeps for a random interval to mimic human behavior."""
    time.sleep(random.uniform(min_sec, max_sec))
