#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-12-10 上午9:03
# @Author  : sugare
# @Site    : 
# @File    : manage1.py
# @Software: PyCharm
import random
import os.path
import tornado.web
import tornado.httpserver
import tornado.gen
import os, sys
import redis
from updata import upUsers, upSurvey, upQuestionChoice
from updata import downloadMask

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("redis_host", default='127.0.0.1', help="redis host")
define("redis_port", default=6379, help="redis port")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/?', LoginHandler),
            (r'/exam/?', ExamHandler),
            (r'/investigation/?', InvestigationHandler),
            (r'/score/?(.*)', ScoreHandler),
            (r'/logout/?', LogoutHandler),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'template'),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
	try:
            self.db = redis.Redis(
                host=sys.argv[1], port=options.redis_port, db=0
            )
	except IndexError:
	    self.db = redis.Redis(
                host=options.redis_host, port=options.redis_port, db=0
            )
	upUsers(self.db)
	upSurvey(self.db)
	upQuestionChoice(self.db)

class BaseHandler(tornado.web.RequestHandler):
    @property       # 将db方法变为属性
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("username")
        if not user_id:
            return None
        return user_id


class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('login.html')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        if len(self.db.hgetall(username)) == 5 and self.db.hgetall(password) == self.db.hgetall(username):
            self.set_secure_cookie("username", username)
            self.redirect('/exam')
        else:
            if len(self.db.hgetall(username)) > 5:
                self.write(u'您已经提交试卷！')
                self.finish()
            else:
                self.redirect('/')


class ExamHandler(BaseHandler):
    def quesNum(self,ty):
        if ty == 's' or ty == 'm':
            L = [ str(x) for x in range(1,61) ]
            Q = random.sample(L, 20)
        elif ty == 'j':
            L = [ str(x) for x in range(1,31) ]
            Q = random.sample(L,10)
        elif ty == 'i':
            L = [ str(x) for x in range(1,6) ]
            Q = random.sample(L,5)
        return map(lambda num: ty+num, Q)

    # @tornado.web.authenticated
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def get(self):

        s = {'rubbish':'s'}
        m = {'rubbish':'m'}
        j = {'rubbish':'j'}
        for i in (s, m, j):
            for k in self.quesNum(i.pop('rubbish')):
                i[k] = self.db.hgetall(k)

        self.render('exam1.html', user=self.current_user, s_ques=s, m_ques=m, j_ques=j)

    # @tornado.web.authenticated
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    def post(self):
        s_mask = 0
        m_mask = 0
        j_mask = 0
        total = 0

        self.request.arguments.pop('_xsrf')
        for i in self.request.arguments:
            user_rec = ''.join(self.request.arguments[i])
            answer = self.db.hget(i, 'AN')
            self.db.hset(self.get_secure_cookie('username'), i, user_rec)
            if user_rec == answer:
                if 's' in i:
                    s_mask += 2
                elif 'm' in i:
                    m_mask += 2
                else:
                    j_mask += 2
        total = s_mask + m_mask + j_mask
        self.db.hset(self.get_secure_cookie('username'), 'single', s_mask)
        self.db.hset(self.get_secure_cookie('username'), 'multi', m_mask)
        self.db.hset(self.get_secure_cookie('username'), 'judge', j_mask)
        self.db.hset(self.get_secure_cookie('username'), 'total', total)
        self.redirect('/investigation')

class InvestigationHandler(ExamHandler):
    # @tornado.gen.coroutine
    def get(self):
        i_ques = {}
        for i in self.quesNum('i'):
            i_ques[i] = self.db.hgetall(i)
        self.render('invest1.html', i_ques=i_ques)

    # @tornado.gen.coroutine
    def post(self):
        self.request.arguments.pop('_xsrf')
        for i in ('i1', 'i2' ,'i3' ,'i4', 'i5'):
            v = self.get_argument(i,'A')
            self.db.hset(i, v, int(self.db.hget(i, v)) + 1)
        self.redirect('/logout')


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.write(u'交卷成功！')
        self.redirect(self.get_argument("next", "/"), )


class ScoreHandler(ExamHandler):
    def get(self, slug=''):
        downloadMask(self.db)
        if slug:
            s = self.db.hgetall(slug)
            s.pop('user')
            s.pop('single')
            s.pop('multi')
            s.pop('judge')
            s.pop('total')
            for i in s:
                s[i] = [s[i], self.db.hget(i, 'AN')]
            self.render('score_detail1.html', s=s)
        else:

            s = {}
            for i in self.db.keys(pattern='2*'):
                s[i] = self.db.hgetall(i)
            self.render('score1.html', s=s)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
