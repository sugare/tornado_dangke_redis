#
#软件及版本
```
python 2.7.12
tornado 4.4.2
redis_version:3.0.6
```

#
#下载软件
```
git clone git@github.com:sugare/tornado_dangke_redis.git

```
#
#安装需要包及库
```
sudo pip install tornado
sudo pip install xlrd
sudo pip install xlwt
sudo apt-get install redis-server supervisor nginx
```
#
#测试
1 运行程序
```
python manage.py
```

2 开始考试
```
http://IP/
```

3 查看成绩
```
http://IP/score
```

#
#加入nginx和supervisor

1 复制conf/nginx.conf到/etc/nginx/nginx.conf
```Bash
sudo cp conf/nginx.conf /etc/nginx/
```

2 复制conf/tornado.conf /etc/supervisor/conf.d/
```Bash
sudp cp conf/tornado.conf /etc/supervisor/conf.d/
```

3 复制程序文件到/var/www目录下
sudo cp -a .* /var/www/html

4 检查supervisor是否成功运行
```Bash
$ sudo supervisorctl 
tornadoes:tornado-8000           RUNNING   pid 6268, uptime 2:17:43
tornadoes:tornado-8001           RUNNING   pid 6269, uptime 2:17:43
tornadoes:tornado-8002           RUNNING   pid 6270, uptime 2:17:43
tornadoes:tornado-8003           RUNNING   pid 6271, uptime 2:17:43
```

5 给予/var/www目录权限
```Bash
chown -R www-data /var/www 
```

6 检查nginx是否成功运行
```
http://IP
```
