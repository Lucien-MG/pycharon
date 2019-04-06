#!/usr/bin/python3.6

import sys

def printprogress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()

def calculatechunk(filesize):
    chunksizes = [4096, 8192, 16358, 32768, 65536, 131072]
    size_test = 1000000
    choice = 0

    for i in range(len(chunksizes)):
        if filesize / size_test > 1:
            size_test *= 10
            choice += 1
        else:
            break

    return chunksizes[choice]


