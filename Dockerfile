FROM ubuntu

MAINTAINER Sugare/30733705@qq.com

RUN apt-get -y update \
	&& apt-get install -y \
	python python-tornado python-xlrd python-xlwt python-redis \
	redis-server \
	nginx \
	supervisor \
	git

WORKDIR /var/www/

RUN git clone git://github.com/sugare/tornado_dangke_redis.git

RUN cp -a tornado_dangke_redis/* . \
	&& rm -rf tornado_dangke_redis \
	&& cp conf/tornado.conf /etc/supervisor/conf.d \
	&& mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.ori \
	&& cp conf/nginx.conf /etc/nginx/nginx.conf \
	&& mv /etc/redis/redis.conf /etc/redis/redis.conf.ori \
	&& cp conf/redis.conf /etc/redis/ \
	&& chown -R www-data /var/www \
	&& /etc/init.d/redis-server start \
	&& python updata.py \

EXPOSE 80

CMD /etc/init.d/supervisor start && /etc/init.d/redis-server start && nginx -g "daemon off;"
