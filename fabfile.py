#
# Usage: fab localhost menu
#
from fabric.operations import local, run, prompt
from fabric.api import task
from fabric.state import env

@task
def localhost():
    env.run = local
    env.hosts = ['localhost']

@task
def menu():
    s = (
        "[1] rsync toolchain 64bit\n"
        "[2] Import thirdpartyfiles for OS build\n"
        "[3] Import thirdpartyfiles not included in the list\n"
        "[z] Quit\n"
        "Choose: \n"
    )
    t = prompt(s) 
    if t == '1':
        rsync_toolchain_64()
    elif t == '2':
        import_thirdpartyfiles_foroakosbuild()
    elif t == '3':
        import_thirdpartyfiles_notincludedinthelist()

@task
def rsync_toolchain_32():
    cmd = (
        "rsync -rl "
        "rsync://ukdev-devserver1.rusclabs.cisco.com/tandberg-system/toolchain/"
        "x86_gcc-4.8.2_eglibc-2.18-r25100_i686-host-linux-gnu-3/* "
        "/tandberg/system/toolchain/"
        "x86_gcc-4.8.2_eglibc-2.18-r25100_i686-host-linux-gnu-3/"
    )
    env.run(cmd)

@task
def rsync_toolchain_64():
    cmd = (
        "rsync -rl "
        "rsync://ukdev-devserver1.rusclabs.cisco.com/tandberg-system/toolchain/"
        "x86_64_gcc-4.8.2_eglibc-2.18-r25100_i686-host-linux-gnu-3/* "
        "/tandberg/system/toolchain/"
        "x86_64_gcc-4.8.2_eglibc-2.18-r25100_i686-host-linux-gnu-3/"
    )
    env.run(cmd)

@task
def rsync_thirdparty(filename):
    cmd = (
        "rsync -rl "
        "rsync://ukdev-devserver1.rusclabs.cisco.com/tandberg-system/thirdparty/"
        "%s "
        "/tandberg/system/thirdparty/"
        "%s"
    ) % (filename, filename)
    env.run(cmd)

@task
def import_thirdpartyfiles_foroakosbuild():
    list_name = 'osbuild_thirdpartyfilelist.txt'
    list_file = open(list_name, 'r')
    prefix_length = len('/tandberg/system/thirdparty/')
    for line in list_file:
        filename = line[prefix_length:].strip()
        rsync_thirdparty(filename)

@task
def import_thirdpartyfiles_notincludedinthelist():
    list_file = [
        "/tandberg/system/thirdparty/schedutils_1.5.0-1.diff",
        "/tandberg/system/thirdparty/suds-0.4.tar.gz",
        "/tandberg/system/thirdparty/python-suds-0.4.tar.gz",
        #"/tandberg/system/thirdparty/sqlite3_3.8.7.4.orig.tar.bz2",
        #"/tandberg/system/thirdparty/libffi-3.2.1.tar.gz",
        #"/tandberg/system/thirdparty/enum34-1.0.4.tar.gz",
        #"/tandberg/system/thirdparty/setuptools-14.3.1.tar.gz",
        #"/tandberg/system/thirdparty/ciscossl-1.0.1m.4.10.tar.gz",
        #"/tandberg/system/thirdparty/util-linux-2.26.1.tar.xz",
        #"/tandberg/system/thirdparty/httpd-2.4.12.tar.bz2",
    ]
    prefix_length = len('/tandberg/system/thirdparty/')
    for fname in list_file:
        filename = fname[prefix_length:].strip()
        rsync_thirdparty(filename)

