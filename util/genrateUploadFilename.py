import os
import time


def generate_filename_for_s3(filename):
    split_filename = filename.split('.')
    title = split_filename[0]
    ext = split_filename[-1]
    milli = str(round(time.time() * 1000))
    file_name_for_upload = f'{title}_{milli}.{ext}'

    return file_name_for_upload
