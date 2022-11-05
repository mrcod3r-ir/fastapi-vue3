## redis

```sh
set "visit_num" 1
```

```sh
set "request_num" 1
```

> Github <font color="red">Public</font> repository details see API: https://api.github.com/repos/user/repo/languages
> For example: https://api.github.com/repos/zxiaosi/Vue3-FastAPI/languages

```sh
rpush "language_details" {"title": "Python", "percentage": 45.4, "color": "#f1e05a"}

rpush "language_details" {"title":"Vue","percentage":44.3,"color":"#42b983"}

rpush "language_details" {"title": "JavaScript", "percentage": 8.7, "color": "#409EFF"}

rpush "language_details" {"title": "\u5176\u4ed6", "percentage": 1.6, "color": "#f56c6c"}
```

```sh
rpush "todo_list" {"title": "\u54e5\u65af\u62c9", "status": true}

rpush "todo_list" {"title": "\u725b\u7684", "status": true}

rpush "todo_list" {"title": "555", "status": true}

rpush "todo_list" {"title": "111", "status": true}
```

## nginx

```sh
server {
    listen 8001;
    server_name localhost;

    location / {
        root /usr/share/nginx/html/dist;
        index index.html index.htm;
        try_files $uri $uri/ /index.html; # Prevent page refresh 404
    }

    #error_page 404 /404.html;

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}

server {
    listen 8000;
    server_name localhost;

    location /api {
        client_max_body_size 5m;
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Specify the methods that allow cross-domain, * represents all
        add_header Access-Control-Allow-Methods *;

        # Cache of preflight commands, if not cached, two requests will be sent each time
        add_header Access-Control-Max-Age 3600;
        # Requests with cookies need to add this field and set it to true
        add_header Access-Control-Allow-Credentials true;

        # Indicates that this domain is allowed to call cross-domain (the domain name and port where the client sends the request)
        # $http_origin dynamically obtains the domain requested by the client. The reason for not using * is that requests with cookies do not support *
        add_header Access-Control-Allow-Origin $http_origin;

        # Represents the fields of the request header dynamically obtained
        add_header Access-Control-Allow-Headers
        $http_access_control_request_headers;

        # OPTIONS Preflight command, the request is sent only when the preflight command passes
        # Check if the request type is a preflight command
        if ($request_method = OPTIONS){
            return 200;
        }
    }
}
```
