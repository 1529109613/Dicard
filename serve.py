#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import socket


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/' or path == '/ad':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('ad_page.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/test' or path == '/test/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('test_page.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/result' or path == '/result/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('result_page.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()


def get_network_ips():
    """获取本机所有网络IP地址（无需netifaces）"""
    ips = []

    try:
        # 方法1：通过UDP连接获取本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        try:
            # 连接到公共DNS服务器但不发送数据
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            ips.append(local_ip)
        except:
            pass
        finally:
            s.close()

        # 方法2：获取所有网络接口的IP
        try:
            hostname = socket.gethostname()
            # 获取主机名对应的所有IP地址
            addrs = socket.getaddrinfo(hostname, None)
            for addr in addrs:
                ip = addr[4][0]  # 获取IP地址部分
                if ip != '127.0.0.1' and ip not in ips and not ip.startswith('169.254'):
                    ips.append(ip)
        except:
            pass

    except Exception as e:
        print(f"获取IP时出错: {e}")

    # 如果还是没有获取到IP，尝试使用socket.gethostbyname_ex
    if not ips:
        try:
            hostname = socket.gethostname()
            _, _, ip_list = socket.gethostbyname_ex(hostname)
            for ip in ip_list:
                if ip != '127.0.0.1' and not ip.startswith('169.254'):
                    ips.append(ip)
        except:
            pass

    return ips


def run_server(port=8000):
    # 关键修改：使用 0.0.0.0 绑定到所有网络接口
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, RequestHandler)

    print(f"🚀 三页连环服务器已启动！")
    print(f"   1. 广告入口页: http://localhost:{port}/")
    print(f"   2. 测试页面:   http://localhost:{port}/test")
    print(f"   3. 结果页面:   http://localhost:{port}/result")

    # 显示所有可能的访问地址
    print(f"\n📱 手机访问地址（选一个试试）:")

    # 尝试获取网络IP
    network_ips = get_network_ips()

    if network_ips:
        for ip in network_ips:
            print(f"   • http://{ip}:{port}")
    else:
        print(f"   ⚠️  无法自动获取IP地址，请手动检查:")
        print(f"     1. 打开命令提示符")
        print(f"     2. 输入: ipconfig")
        print(f"     3. 查找 '无线局域网适配器 WLAN' 或 '以太网适配器' 下的IPv4地址")
        print(f"     4. 在手机浏览器输入: http://[找到的IP]:{port}")

    print(f"\n💡 连接提示:")
    print(f"   - 确保电脑和手机连接同一WiFi")
    print(f"   - 如果连接不上，尝试关闭防火墙或杀毒软件")
    print(f"   - 也可以尝试重启电脑/手机")

    try:
        print(f"\n✅ 服务器运行中，按 Ctrl+C 停止...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器停止。")


if __name__ == '__main__':
    run_server(port=8000)
