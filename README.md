

# 一、项目
**MilkTeaBrother**是使用麦克纳姆移动方式的室内服务小车，动力系统为RoboMaster M2006，文中提到的相关文件可以在下方获取。
[点击此处了解MilkTeaBrother相关信息](https://github.com/Hermanye996/MilkTeaBrother)

# 二、测试内容
测试在**Ubuntu20.04**环境下，在**ROS**中**读取电机位置或速度反馈信息**并**控制电机**，完成小车**移动控制**，通过**PID**控制算法，实现小车速度的闭环。

# 三、测试材料
## ① 优利德UNIT直流稳压电源UTP1310
UTP1310是经济型的直流稳压电源，具有过压保护、过流保护、过温保护、LED四位电压电流显示等功能。
[了解UTP1310直流稳压电源相关信息](https://github.com/Hermanye996/MilkTeaBrother/blob/main/instructions/UTP1310%E7%9B%B4%E6%B5%81%E7%A8%B3%E5%8E%8B%E7%94%B5%E6%BA%90.pdf)

## ② RoboMaster M2006 P36直流无刷减速电机
[了解M2006电机相关信息](https://www.robomaster.com/zh-CN/products/components/general/M2006)
M2006 P36电机采用三相永磁直流无刷结构，具有输出转速高、体积小、功率密度高的特点。M2006内置位置传感器，提供精确的位置反馈，以FOC矢量控制方式使电机产生连续的扭矩。减速箱减速比为36：1
电机的额定输入电压为24V，额定电流为3A

## ③ RoboMaster C610无刷电机调速器
[了解C610电调相关信息](https://www.robomaster.com/zh-CN/products/components/general/M2006)
C610电调采用32位电机驱动定制芯片，使用磁场定向控制技术（FOC），实现对电机扭矩的精确控制，与M2006电机配合使用，可选用RoboMaster Assistant调参并升级固件

## ④ RoboMaster 电调中心板 2
[了解RM2电调中心板相关信息](https://www.robomaster.com/zh-CN/products/components/detail/2495)
RoboMaster 电调中心板 2 是一款专为实现电源及 CAN Bus 通信接口扩展的转接板。中心板具有结构紧凑、接口集成度高等特性，可同时驱动 7 套动力系统；采用硅胶外壳设计提高了防护等级，保障产品可靠运行。

## ⑤ MakerbaseMKS CANable Pro V1.0 USB转CAN模块
CANable 是一款小型的、低成本的开源 USB 转 CAN 适配器。 CANable 在您的计算机上显示为虚拟串行端口，并充当 CAN 总线接口的串行线路。 使用可选的candlelight固件时，CANable 将作为 Linux 上的本机 CAN 接口被调用。
CANable Pro 是 CANable 的电隔离版本，具有增强的 ESD 保护和分离式固定孔。
[了解CANable相关信息](https://canable.io/)
[了解Makerbase商家提供的测试案例](https://blog.csdn.net/gjy_skyblue/article/details/116657721)




# 四、测试前准备
## ① 接线
开始测试前，需要首先将各部分接线如下：
### 1. 连接XT60电源线与中心板
RoboMaster Central Board 2额定输入电压为24V，额定输入电流为30A，电源输入接口为XT60

### 2. 连接中心板与XT30电源线
中心板上有七个XT30电源输出接口，额定电压为24V，额定输出电流为15A

### 3. 连接XT30电源线与C610电调
将XT30电源线正负两线，分别焊于电调的正负点位，对应焊接点在C610电调说明书中有具体描述。
C610电调额定电压为24V，最高支持10A的持续电流。

### 4. 连接中心板与CAN信号线
在中心板的顶部或侧面有多个2-Pin CAN总线接口，每个接口与板上其他CAN总线接口并联，用于CAN总线通讯。

### 5. 连接CAN信号线与C610电调
按照CAN信号线线序CAN_H、CAN_L，将CAN信号线焊接到C610电调背面对应端点，在说明书中有具体描述。
CAN总线比特率为1Mbps，M2006动力系统的CAN通信默认发送频率为1KHz

### 6. 连接C610电调与M2006电机的三相动力接头
连接时确保连线正确，在说明书中有具体说明。

### 7. 连接C610电调与M2006电机的4-Pin数据线
将M2006电机的4-Pin位置传感器数据线连接到C610电调对应端口上，在说明书中有具体描述。
**最终接线情况应如下图所示：**
![在这里插入图片描述](https://img-blog.csdnimg.cn/298fcc12d66745049dcd6010bc87191a.png)

## ② 接通电源并校准电机
### 1. 接通电源
待收到启动蜂鸣，电机与电调开始正常工作后，绿灯闪烁，此时可以开始校正电机。

### 2. 校正电机
**校准过程中须保持空载，且不可触碰电机。**
初次使用需校准电机，长按C610电调上的SET按键，直至指示灯变为绿灯高频闪烁，随后释放SET按键。此时电机将进入自动校准模式，校准完成后会自动退出校准模式。

# 五、测试
## ① 调试MakerbaseCANable USB转CAN模块
### 1. 获取CANable固件
可以从[CANable官网](https://canable.io/)下载固件。
也可查看文件夹中已经编译好的固件firmware.bin，或者是按照[candlelight项目](https://github.com/candle-usb/candleLight_fw/tree/master#building)的编译步骤获取固件文件。
### 2. 烧录
使用STM32CubeProgrammer将固件烧录到板中。
[下载STM32CubeProgrammer](https://www.st.com/zh/development-tools/stm32cubeprog.html)
将板上的boot跳线连接，开启DFU (Device Firmware Upgrade) 烧录模式，boot位置即图上红框处。
![在这里插入图片描述](https://img-blog.csdnimg.cn/fdf086f3af5e49ff81f0b8d2431e95fe.png)
打开STM32CubeProgrammer，依次点击红绿蓝三个按钮，搜索可用的STM32设备。
![在这里插入图片描述](https://img-blog.csdnimg.cn/4aec00fbc46344379591f54a77a9e81c.png)
随后按照图示顺序，加载本地的固件文件。
![在这里插入图片描述](https://img-blog.csdnimg.cn/e73043d3dff141079e0c45a579c0be42.png)
选择好本地的固件文件后，点击和上图中Read同位置的Download按钮，将固件文件载入板中。
当提示烧录成功后，断开跳线，准备开始下一步在Linux中进行测试。

## ② 在Linux中测试接收CAN总线信息
### 1. 安装测试软件包及其依赖
```bash
sudo apt-get install -y can-utils net-tools
```

### 2. 查看CAN设备是否能被发现
can设备在Linux下在ifconfig中和其他设备一同管理，图中红框所示为测试要用的CAN设备。
```bash
ifconfig -a
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/3b1892cabce246d48a796f1f2d8a89f7.png)

### 3. 启用CAN设备
以CAN设备名为can0为例，比特率为1000000，启用该设备。
```bash
sudo ip link set can0 up type can bitrate 1000000
```
### 4. 监听CAN端口
监听Can0收到的信息。

```bash
candump can0
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/f6740273346b41c4a25b5b839c206ad1.png)
此时扭动电机，可以看到can0处收到的信息在不断变化，证明能接收到CAN总线信息，可以准备下一步测试，按照协议规则，读取CAN设备传达的具体信息。

## ③ CAN通讯



要通过CAN总线收发电机的信息，首先要了解CAN本身，着重了解**数据帧**部分
[了解CAN通讯数据帧相关内容](https://zhuanlan.zhihu.com/p/268901221)
因为只涉及到应用CAN，因此对其底层的具体实现不需要全部掌握，使用[python-can](https://python-can.readthedocs.io/en/master/)在Ubuntu中开发。
python-can 库为 Python 提供控制器区域网络支持，为不同的硬件设备提供通用抽象，以及一套用于在 CAN 总线上发送和接收消息的实用程序。
[查看MilkTeaBrother的can通讯模块](https://github.com/Hermanye996/MilkTeaBrother/blob/main/src/MTB_can.py)

## ④ 控制电机
在了解完CAN通讯后，依照MilkTeaBrother的CAN模块，接收并向电机发送控制指令
[查看MilkTeaBrother的电机主程序](https://github.com/Hermanye996/MilkTeaBrother/blob/main/src/MTB_main.py)

## ⑤ 初步PID闭环调节
需要完成对电机的初步pid调节后，电机可以按照用户想要的值转动
[查看MilkTeaBrother的PID模块](https://github.com/Hermanye996/MilkTeaBrother/blob/main/src/MTB_pid.py)

## ⑥ 移植到ROS中
在ROS中调用电机的主程序，并将参数传向参数服务器，在上位机中对pid常数作优化调整






**参考资料如下：**
[广东工业大学USB2CAN项目](https://github.com/rm-controls/rm_usb2can/blob/main/README_CN.md)
[CAN通讯](https://zhuanlan.zhihu.com/p/268498263)
[python串口通信控制电机驱动](https://blog.csdn.net/zengqz123/article/details/85682039?spm=1001.2014.3001.5502)

