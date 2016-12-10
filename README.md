python 2.7.12<br/>
tornado 4.4.2<br/>
redis_version:3.0.6

pip install tornado<br/>
pip install torndb<br/>
pip install xlrd<br/>
pip install xlwt<br/>
pip install redis<br/>
sudo apt-get install redis-server supervisor nginx<br/>

#
# 上传题库和用户
python updata.py

#
# 运行程序
python manage.py

#
# 开始考试
http://IP/

#
# 查看成绩
http://IP/score


#
# 加入nginx和supervisor
1. 复制conf/nginx.conf到/etc/nginx/nginx.conf
2. 复制conf/tornado.conf /etc/supervisor/conf.d/
3. 检查supervisor是否成功运行
   sudo supervisorctl
4. 检查nginx是否成功运行
   http://IP
