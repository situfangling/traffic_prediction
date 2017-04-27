from django.test import TestCase
from traffic_prediction.settings import BASE_DIR
import os
# Create your tests here.
#print(BASE_DIR)

'''file_dir = os.path.join(BASE_DIR, "../20130304/").replace("\\","/")
file_path = os.path.join(file_dir, "filelist.txt")
print(file_path)'''


#text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')