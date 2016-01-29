项目部署方法（后台）

后台使用python语言，django框架书写，需要环境：linux，django，redis，mysql，nginx

python 依赖的软件包

    Django==1.8
    django-mysqlpool==0.1.post9
    django-redis==3.8.3
    django-redis-cache==0.13.1
    django-redis-sessions==0.4.0
    MySQL-python==1.2.5
    redis==2.10.3
    requests==2.6.2
    SQLAlchemy==1.0.2
    uWSGI==2.0.10
    xlwt==1.0.0

建议安装python 虚拟环境，并制定python版本为python2.7，并安装pip

通过pip install -r requirement.txt安装所有包

并从https://github.com/wang125309/pet.git clone 下前端代码 通过nginx进行部署

通过uwsgi启动python程序，指令如make file所写

make start-uwsgi 启动uwsgi

make reload-uwsgi 重启uwsgi

make stop-uwsgi 关闭uwsgi

uwsgi监听端口8123（可以按照需求自己指定）

-------------------------------------------------------------------------

nginx 参考配置文件

    server {
        listen 80;
        gzip on;
        gzip_buffers 4 16k;
        gzip_types       text/plain application/x-javascript text/css application/xml;
        server_name 127.0.0.1;
        location /static {
            alias /data/pet/static;
            break;
        }
        location /data {
            alias /data/pet-backend/data;
            break;
        }
        location /pet {
            uwsgi_pass 127.0.0.1:8123;
            uwsgi_param Host $host;
            uwsgi_param X-Real-IP $remote_addr;
            uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
            uwsgi_param X-Forwarded-Proto $http_x_forwarded_proto;
            include uwsgi_params;
        }

        location /portal {
            uwsgi_pass 127.0.0.1:8123;
            uwsgi_param Host $host;
            uwsgi_param X-Real-IP $remote_addr;
            uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
            uwsgi_param X-Forwarded-Proto $http_x_forwarded_proto;
            include uwsgi_params;
        }
	    location / {
	        alias /data/pet/template/;
            index index.html;
            break;
        }
    }

----------------------------------------------------------------------

访问域名即可

报名表导出：http://xxxx/pet/export/

access-token刷新

http://xxxx/portal/upload_access_token/

关于分享

部署的时候需要修改后台的appId和access token，appId 和 access_token 均由微信公众号提供，在微信公众平台官方网站的首页位置，拿到appId和access_token并写到/portal/views.py的两个变量定义中

且修改/portal/plugin.py中，最后一个方法中的地址为部署线上域名地址

注意修改微信公众平台的js安全域名，添加现有域名（一级域名即可）到js安全域名列表

同时更新access-token(此为微信分享实用的token，不同以上)
