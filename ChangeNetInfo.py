# -*- coding: utf-8 -*-
import wmi
import time
def change_net_config(ip,mask,gateway):
    wmiService = wmi.WMI()
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
    # for objNicConfig in colNicConfigs:
    #     # print objNicConfig.Index
    #     # print objNicConfig.SettingID
    #     # print objNicConfig.Description.encode("cp936")
    #     print(objNicConfig.IPAddress)
    #     # print objNicConfig.IPSubnet
    #     print(objNicConfig.DefaultIPGateway)
    #     print(objNicConfig.DNSServerSearchOrder)
    if len(colNicConfigs) < 1:
        print('没有找到可用的网络适配器')
        exit()
    objNicConfig = colNicConfigs[2]
    if ip in objNicConfig.IPAddress[0]:
        print("目前IP已经是%s\n无需切换"%ip)
        return
    #for method_name in objNicConfig.methods:
    #    method = getattr(objNicConfig, method_name)
    #    print method
    print('正在修改IP,请稍候...')
    arrIPAddresses = [ip]
    arrSubnetMasks = [mask]
    arrDefaultGateways = [gateway]
    arrGatewayCostMetrics = [1]
    intReboot = 0
    returnValue = objNicConfig.EnableStatic(IPAddress = arrIPAddresses, SubnetMask = arrSubnetMasks)
    if returnValue[0] == 0:
        print('设置IP成功')
    elif returnValue[0] == 1:
        print('设置IP成功')
        intReboot += 1
    else:
        print('修改IP失败: IP设置发生错误')
        exit()
    returnValue = objNicConfig.SetGateways(DefaultIPGateway = arrDefaultGateways, GatewayCostMetric = arrGatewayCostMetrics)
    if returnValue[0] == 0:
        print('设置网关成功')
    elif returnValue[0] == 1:
        print('设置网关成功')
        intReboot += 1
    else:
        print('修改IP失败: 网关设置发生错误')
        exit()

    if intReboot > 0:
        print('需要重新启动计算机')
    else:
        print('')
        print('修改后的配置为：')
        print('IP: ', ':'.join(objNicConfig.IPAddress))
        print('掩码: ', ':'.join(objNicConfig.IPSubnet))
        print('网关: ', ':'.join(objNicConfig.DefaultIPGateway[0]))
    print('修改IP结束')
    time.sleep(1)
if __name__ == "__main__":
    print("正在准备切换IP：192.168.1.138")
    IPAddresses = '192.168.1.138'
    SubnetMasks = '255.255.255.0'
    DefaultGateways = '192.168.1.1'
    change_net_config(IPAddresses,SubnetMasks,DefaultGateways)

