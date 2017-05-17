from django.test import TestCase
from prediction_new.settings import BASE_DIR
import os
# Create your tests here.
#print(BASE_DIR)

'''file_dir = os.path.join(BASE_DIR, "../20130304/").replace("\\","/")
file_path = os.path.join(file_dir, "filelist.txt")
print(file_path)'''


#text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
from multiprocessing import Process
import os

'''
# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.') '''

import datetime
tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))

'''utc_time = datetime.datetime(2017,4,1,0,0,0,tzinfo=tz_utc_8)
utc_time_str = utc_time.strftime("%Y-%m-%d %H:%M:%S")
print(utc_time_str)'''


query_time_str = "2017-04-01 18:20:00"
query_time_dt = datetime.datetime.strptime(query_time_str, "%Y-%m-%d %H:%M:%S")
print(query_time_dt)