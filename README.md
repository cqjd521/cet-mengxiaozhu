# cet-mengxiaozhu
功能：主动下发四六级成绩(单线程粗糙版)

受众：接入**萌小助**教务的微信**服务号**用户们**主动下发**四六级成绩

下发方式:48h客服接口/模板信息

##原理
根据appid和appsecret取该公众号的用户openid列表，根据openid从小助调试页面取得该用户的姓名，通过免准考证查询接口查得该同学的成绩后用客服接口或者模板信息推送给指定用户

##windows用法
[安装python for win 3.4](https://www.python.org/downloads/windows/)

下载本项目解压，命令行切换到该项目

用文本编辑器修改config.py内的信息

执行 pip install -r requirements.txt

执行 python do.py

##效果图
![demo](http://7ls08n.com1.z0.glb.clouddn.com/Screenshot_2016-02-24-21-00-49.gif)
