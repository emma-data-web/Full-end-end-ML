import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name, log_file,level=logging.DEBUG):
  logger = logging.getLogger(name)
  logger.setLevel(level=logging.DEBUG)

  if not logger.hasHandlers():
    file_handler = TimedRotatingFileHandler(
      filename=log_file,
              when='H',     
              interval=10,          
              backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

  return logger 
