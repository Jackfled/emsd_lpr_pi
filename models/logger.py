'''
Logger Module Created by Aaron 210811
支持多进程
Support multi process
'''

import logging
from logging import handlers
import platform
import os


from time import time
import time

import codecs

from logging.handlers import BaseRotatingHandler


class MultiProcessSafeDailyRotatingFileHandler(BaseRotatingHandler):
    """Similar with `logging.TimedRotatingFileHandler`, while this one is
    - Multi process safe
    - Rotate at midnight only
    - Utc not supported
    """
    def __init__(self, filename, encoding=None, delay=False, utc=False, **kwargs):
        self.utc = utc
        self.suffix = "%Y-%m-%d"
        self.baseFilename = filename
        self.currentFileName = self._compute_fn()

        BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)
 
    def shouldRollover(self, record):
        if self.currentFileName != self._compute_fn():
            return True
        return False
 
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.currentFileName = self._compute_fn()
 
    def _compute_fn(self):
        path, filename = os.path.split(self.baseFilename)
        path = os.path.join(path, time.strftime(self.suffix, time.localtime()))

        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, filename)
 
    def _open(self):
        if self.encoding is None:
            stream = open(self.currentFileName, self.mode)
        else:
            stream = codecs.open(self.currentFileName, self.mode, self.encoding)
        # simulate file name structure of `logging.TimedRotatingFileHandler`
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(self.currentFileName, self.baseFilename)
        except OSError:
            pass
        return stream

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    } #日志级别关系映射
 
    def __init__(self,filename,level='info',when='MIDNIGHT',backCount=3,fmt='【%(asctime)s】[%(lineno)d] - %(levelname)s: %(message)s'):

        file = filename
        if platform.system().lower() == 'windows':
            root = os.path.abspath('.')[:3]
            file = os.path.join(root, filename)
            file = file.replace("/", "\\")
            # print("Logfilename=%s" % file)

    
        self.logger = logging.getLogger(file)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式

        
        # self.th = handlers.TimedRotatingFileHandler(filename=file,when=when,backupCount=backCount,encoding='utf-8')

        self.th = MultiProcessSafeDailyRotatingFileHandler(filename=file, encoding='utf-8') #handlers.TimedRotatingFileHandler(filename=file,when=when,backupCount=backCount,encoding='utf-8')

        #往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        self.th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(self.th)

        # Create a "blank line" handler
        # self.blank_handler = handlers.TimedRotatingFileHandler(filename=file,when=when,backupCount=backCount,encoding='utf-8')
        # self.blank_handler.setLevel(logging.DEBUG)
        # self.blank_handler.setFormatter(logging.Formatter(fmt=''))

        self.logger.newline = self.log_newline

    def log_newline(self, how_many_lines=1):
        # Switch handler, output a blank line
        fmt = self.th.formatter

        self.th.setFormatter(logging.Formatter(fmt=''))

        # self.logger.removeHandler(self.th)
        # self.logger.addHandler(self.blank_handler)
        for i in range(how_many_lines):
            self.logger.info('')

        self.th.setFormatter(fmt)
        # Switch back
        # self.logger.removeHandler(self.blank_handler)
        # self.logger.addHandler(self.th)


def logtest1():
    log = Logger('test.log',level='debug').logger
    for i in range(100):
        log.info("logtest3汉字 %d" % i)
        time.sleep(1)

def logtest2():
    log = Logger('test.log',level='debug').logger
    for i in range(100):
        log.debug("汉字logtest4 %d" % i)
        time.sleep(1)

if __name__ == '__main__':
    # import threading
    import multiprocessing
    # log = Logger('all.log',level='info')
    # log.logger.debug('debug')
    # log.logger.info('info')
    # log.logger.warning('警告')
    # log.logger.error('报错')
    # log.logger.critical('严重')
    # Logger('error.log', level='error').logger.error('error')

    t1 = multiprocessing.Process(target=logtest1, daemon=True)
    t1.name = "T_SMAPI_1"
    t1.start()    

    t2 = multiprocessing.Process(target=logtest2, daemon=True)
    t2.name = "T_SMAPI_2"
    t2.start()   

    t1.join()

    t2.join()