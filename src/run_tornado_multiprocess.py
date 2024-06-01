import multiprocessing
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.netutil
import tornado.wsgi
from app import create_app

def start_server(sockets):
    flask_app = create_app()
    app = tornado.wsgi.WSGIContainer(flask_app)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    port = 8000
    num_processes = 16  # 启动16个进程

    # 在主进程中绑定端口
    sockets = tornado.netutil.bind_sockets(port)

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=start_server, args=(sockets,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()