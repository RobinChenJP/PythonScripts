import urllib.parse
import urllib.request
import threading
import json
import time
import ChangeNetInfo


def http_post():
    url = 'http://1.1.1.3/ac_portal/login.php'
    # Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0)'
    }
    # Post传值
    values = {
        'opr': 'pwdLogin',
        'userName': 'chenjp',
        'pwd': 'Fise123',
        'rememberPwd': '1'
    }
    data = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request(url, data, headers)
    result_json = urllib.request.urlopen(request).read().decode('utf-8')
    return result_json.replace("'", "\"")


def login_thread():
    countdown = 3
    for x in range(countdown):
        try:
            result = json.loads(http_post())
            break
        except urllib.error.URLError:
            print("连接错误，第%d次尝试重新连接" % (x + 1))
            result['msg'] = "连接错误"
            time.sleep(2)
    print("登录结果：", result['msg'])
    for x in range(countdown):
        print(countdown - x, "秒后自动关闭")
        time.sleep(1)


if __name__ == "__main__":
    print("正在准备切换网络......")
    ChangeNetInfo.change_net_config("192.168.11.254", "255.255.255.0", "192.168.11.1")
    print("正在准备登录沸石网络......")
    thread = threading.Thread(target=login_thread)
    thread.start()
    thread.join()
    print("结束操作，正在退出......")
    exit()
