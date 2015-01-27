import logging

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logging.getLogger('vcr.stubs').setLevel(logging.WARNING)
logging.getLogger('requests.packages.urllib3.connectionpool')\
    .setLevel(logging.WARNING)

def get_logger(*args, **kwargs):
    return logging.getLogger(*args, **kwargs)

