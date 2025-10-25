#!/usr/bin/env python3

'''
实现一个安全的删除操作
同时兼容rm的操作习惯 如果-rf选项

在rm命令时，如果没有指定-r, 它会提示 
rm: cannot remove 'sss': Is a directory

在以下情况下，-f选项会起作用：
1.删除不存在的文件或目录时，-f选项会让rm命令不提示错误信息，而是直接退出。
2.删除只读文件或目录时，-f选项会忽略文件或目录的只读属性，直接删除。
3.删除受保护的文件或目录时，-f选项会忽略文件或目录的保护属性，直接删除。


如果指定的-f参数，不提示空目录或不可删除的文件
如果指定了-r参数，直接删除目录，并返回true， 否则提示错误，返回false

'''

import shutil 
import os 
import time 
import sys

def print_version():
    print("v0.1 - 20230605")
    sys.exit(0)

def print_usage():
    usage = '''Usage: srm [OPTION] ... [FILE] ...
Remove (unlink) the FILE(s).
  -f, --force              ignore nonexistent files and arguments, never prompt
  -r, -R, --recursive      remove directories and their contents recursively
  -h, --help               display the help and exit
  -v, --version            output the version and exit
'''
    print(usage)
    sys.exit(0)



# 定义回收站路径
trash_dir = os.path.expanduser("~") + "/.trash"

# 如果回收站不存在，则创建回收站目录
if not os.path.exists(trash_dir):
    os.mkdir(trash_dir)


def move_file(src, dst)->bool:
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        print(e)
        return False

def remove_link(file)->bool:
    try:
        os.remove(file)
        return True 
    except Exception as e:
        print(e)
        return False

def delete_file(path, opt_force = False, opt_recursive = False)-> bool:
    # 删除目录的后缀
    while len(path) and path.endswith('/'):
        path = path[0:-1]

    # 获取文件名
    file_name = os.path.basename(path)
    
    # 获取当前时间，并将其格式化为年月日时分秒的形式
    timestamp = time.strftime("%Y%m%d%H%M%S")
    
    # 构造回收站中的文件名
    trash_file = os.path.join(trash_dir, timestamp + "-" + file_name)

    # 如果是链接文件，直接删除
    if os.path.islink(path):
        if not remove_link(path):
            return False
        print("rm: remove link '%s'" % path)
    elif os.path.isfile(path):
        # 复制文件到回收站        
        if not move_file(path, trash_file):
            return False
        print("rm: move '%s' -> '%s'" % (path, trash_file))
    elif os.path.isdir(path):        
        if not opt_recursive:            
            print("rm: cannot remove '%s': Is a directory" % path)    
            return False
        if not move_file(path, trash_file):
            return False
        print("rm: move '%s' -> '%s'" % (path, trash_file))
    else:
        if not opt_force:
            print("rm: cannot remove '%s': No such file or directory" % path)
            return False
    ## 默认返回真
    return True

## 先循环一次，分开所有的参数和文件
files = []
args = []

for v in sys.argv[1:]:
    if v.startswith('-'):
        args.append(v)
    else :
        files.append(v)    

## 看看有没有-r选项，或-rf 或-fr 或-f选项

options_force = ['-f', '--force', '-rf', '-fr', '-fR', '-Rf']
options_recursive = ['--recursive', '-r', '-R', '-rf', '-fr', '-fR', '-Rf']
options_help = ['-h', '--help']
options_version = ['-v', '--version']

with_recuresive = False
with_force = False

# 先看看有没有帮助或版本需求
for opt in args:
    if opt in options_help:
        print_usage()
    if opt in options_version:
        print_version()

# 处理其他选项
for opt in args:
    if opt in options_force:
        with_force = True 
    if opt in options_recursive:
        with_recuresive = True 

failed_count = 0
for n in files:
    if not delete_file(n, with_force, with_recuresive):
        failed_count += 1

if failed_count > 0:
    sys.exit(1)
else:
    sys.exit(0)
