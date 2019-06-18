# aliyun_monitor_switch
功能：
阿里云监控大盘自动切换页面，配合监控大屏(电视、显示器)使用。
通过selenium自动登录阿里云监控，批量打开监控大盘页面，自动切换chrome标签

# 参数说明
使用阿里云-RAM用户登录 https://signin.aliyun.com/login.htm 监控子账号分配只读权限
- URLS:
  自定义监控大盘的url

- SWITCHTIME:
  切换标签的间隔时间

- USERNAME:
  用户名

- PASSWORD:
  密码

# 安装依赖
```
pip install selenium
pip install retry
```
# 使用
```
python monitor.py
```
