#! /usr/bin/python3
import os
import time
import subprocess

combos = []
release_version = "None"
is_clean = True
is_ota = True
thread_count = 24
is_save_log = True
log_file_name = "Build-" + time.strftime("%Y%m%d", time.localtime()) + ".log"
git_branch = "None"
release_dir = "release_version"
device_platform = "None"
device_platform_list = []
command_list = []

BLACK = '\033[0;30m'
DARK_GRAY = '\033[1;30m'
LIGHT_GRAY = '\033[0;37m'
BLUE = '\033[0;34m'
LIGHT_BLUE = '\033[1;34m'
GREEN = '\033[0;32m'
LIGHT_GREEN = '\033[1;32m'
CYAN = '\033[0;36m'
LIGHT_CYAN = '\033[1;36m'
RED = '\033[0;31m'
LIGHT_RED = '\033[1;31m'
PURPLE = '\033[0;35m'
LIGHT_PURPLE = '\033[1;35m'
BROWN = '\033[0;33m'
YELLOW = '\033[1;33m'
WHITE = '\033[1;37m'
DEFAULT_COLOR = '\033[00m'
RED_BOLD = '\033[01;31m'
ENDC = '\033[0m'


def init_config():
    fise_device_path = "./device/fise/"
    add_lunch_combo = "add_lunch_combo"
    dirlist = os.listdir(fise_device_path)
    for dir in dirlist:
        if dir.startswith("mz"):
            device_platform_list.append(dir)
            for line in open(fise_device_path + dir + "/vendorsetup.sh").readlines():
                if line.startswith(add_lunch_combo):
                    combo = line.replace(add_lunch_combo, "").strip()
                    combos.append(combo)
                    if combo.endswith("user"):
                        global release_version
                        global device_platform
                        release_version = combo
                        device_platform = dir
    git_branches = os.popen("git branch")
    for branch in git_branches.readlines():
        if branch.strip().startswith("*"):
            global git_branch
            global release_dir
            git_branch = branch.replace("*", "").strip()
            build_type = (release_version.split())[-1]
            release_dir = "release_" + build_type + "_" + git_branch.upper()
    git_branches.close()
    print(coloring(LIGHT_GREEN,
                   "%s\n默认配置为：\n\n编译平台：%s\n编译版本：%s\n编译分支：%s\n执行Clean：%r\n编译OTA包：%r\n编译线程数：%d\n是否保存日志副本：%r\n日志副本文件名：%s\n释放版本文件夹：%s\n%s" % (
                       "=" * 50, device_platform, release_version, git_branch, is_clean, is_ota, thread_count,
                       is_save_log,
                       log_file_name, release_dir, "=" * 50)))


def custom_config():
    print(coloring(YELLOW, "\n\n请输入编译版本序号[1 - %d]" % len(combos)) + coloring(LIGHT_BLUE,
                                                                             "（其他输入将默认为%s）：" % release_version))
    i = 0
    while i < len(combos):
        print("%d . %s" % (i + 1, combos[i]))
        i += 1
    version_input_str = input("序号：").strip()
    global release_version
    try:
        if 0 < int(version_input_str) <= len(combos):
            release_version = combos[int(version_input_str) - 1]
    except ValueError:
        print(coloring(RED, "格式错误，保持默认"))
    for platform in device_platform_list:
        if platform in release_version:
            global device_platform
            device_platform = platform
    print(coloring(LIGHT_GREEN, "现编译版本为：%s\n%s" % (release_version, "-" * 50)))

    global is_clean
    is_clean_input_str = input(
        coloring(YELLOW, "\n\n请输入Y或N选择是否执行Clean") + coloring(LIGHT_BLUE, "（其他输入则为则为默认%r）：" % is_clean)).strip()
    if is_clean_input_str.upper() == "Y":
        is_clean = True
    elif is_clean_input_str.upper() == "N":
        is_clean = False
    print(coloring(LIGHT_GREEN, "现执行Clean：：%r\n%s" % (is_clean, "-" * 50)))

    global is_ota
    is_ota_input_str = input(
        coloring(YELLOW, "\n\n请输入Y或N选择是否编译OTA包") + coloring(LIGHT_BLUE, "（其他输入则为则为默认%r）：" % is_ota)).strip()
    if is_ota_input_str.upper() == "Y":
        is_ota = True
    elif is_ota_input_str.upper() == "N":
        is_ota = False
    print(coloring(LIGHT_GREEN, "现是否编译OTA包：%r\n%s" % (is_ota, "-" * 50)))

    global thread_count
    thread_count_input_str = input(
        coloring(YELLOW, "\n\n请输入编译线程数") + coloring(LIGHT_BLUE, "（输入非整数则为默认%d）：" % thread_count)).strip()
    try:
        if 0 < int(thread_count_input_str):
            thread_count = int(thread_count_input_str)
    except ValueError:
        print(coloring(RED, "格式错误，保持默认"))
    print(coloring(LIGHT_GREEN, "编译线程数：%d\n%s" % (thread_count, "-" * 50)))

    global is_save_log
    is_save_log_input_str = input(coloring(YELLOW, "\n\n请输入Y或N选择是否保存日志副本") + coloring(LIGHT_BLUE,
                                                                                      "（不输入则为默认%r，其他输入将会作为日志文件名且保存日志副本）：" % is_save_log)).strip()
    if is_save_log_input_str.upper() == "Y":
        is_save_log = True
    elif is_save_log_input_str.upper() == "N":
        is_save_log = False
    elif len(is_save_log_input_str) > 0:
        is_save_log = True
        global log_file_name
        log_file_name = is_save_log_input_str
    print(coloring(LIGHT_GREEN, "现是否保存日志副本：%r\n日志文件名为%s\n%s" % (is_save_log, log_file_name, "-" * 50)))

    confirm = input(coloring(LIGHT_GREEN, "\n\n%s\n默认配置为：\n\n编译平台：%s\n编译版本：%s\n执行Clean：%r\n编译OTA包：%r\n编译线程数：%d\n"
                                          "是否保存日志副本：%r\n日志副本文件名：%s\n%s\n（确认配置请回车，其他输入则重新配置）" % (
                                 "=" * 50, device_platform, release_version, is_clean, is_ota, thread_count,
                                 is_save_log,
                                 log_file_name,
                                 "=" * 50)))
    if len(confirm) > 0:
        custom_config()


def exec_order():
    if is_clean:
        add_command("rm -rf ./out", is_check_error=False)
        add_command("rm -rf ./Build-*.log", is_check_error=False)
    add_command("source build/envsetup.sh")
    add_command("lunch " + release_version)
    if is_save_log:
        add_command("make -j%d 2>&1 | tee %s" % (thread_count, log_file_name))
    else:
        add_command("make -j%d" % thread_count)
    if is_ota:
        add_command("make otapackage -j%d" % thread_count)
    add_command("rm -rf %s/" % release_dir)
    add_command("mkdir %s" % release_dir)
    add_command("cp out/target/product/%s/boot.img  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/cache.img  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/lk.bin  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/logo.bin  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/*_Android_scatter.txt  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/preloader_*.bin  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/recovery.img  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/system.img  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/secro.img  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/trustzone.bin %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/userdata.img  %s/" % (device_platform, release_dir))
    add_command("cp out/target/product/%s/obj/CGEN/APDB_MT*  %s/" % (device_platform, release_dir))
    add_command("rm %s/*_ENUM" % release_dir)
    add_command("cp out/target/product/%s/system/etc/mddb/BPLGUI* %s/" % (device_platform, release_dir))
    if is_ota:
        add_command("mkdir %s/fota" % release_dir)
        add_command("cp out/target/product/%s/target* %s/fota/" % (device_platform, release_dir))
    add_command('echo "%s">%s/branch.txt' % (git_branch, release_dir))
    commands = ""
    for command, check_error in command_list:
        commands += 'echo "%s"&&' % coloring(GREEN, "%s\n正在执行：%s\n%s\n" % ("*" * 80, command, "*" * 80))
        commands += command
        if check_error:
            commands += "&&"
        else:
            commands += ";"
    commands += 'echo "%s"' % coloring(GREEN, "\n\n\n%s\n\n全部执行完成！\n请查看目录：%s\n\n%s" % ("#" * 80, release_dir, "#" * 80))
    print(coloring(GREEN, "开始执行"))
    p = subprocess.Popen(commands, executable="/bin/bash", shell=True, env=None, stdin=subprocess.PIPE)
    try:
        p.wait()
    except KeyboardInterrupt:
        print(coloring(RED, "终止命令！"))
        p.kill()


def add_command(cmd, is_check_error=True):
    command_list.append((cmd, is_check_error))


def coloring(color, string):
    return color + string + ENDC


if __name__ == "__main__":
    try:
        init_config()
        need_config = input(coloring(YELLOW, "需要配置吗？") + coloring(LIGHT_BLUE, "（直接回车执行默认配置，其他输入将进入配置）"))
        if len(need_config) > 0:
            custom_config()
        exec_order()
    except KeyboardInterrupt:
        print(coloring(RED, "退出脚本！"))
