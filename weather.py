from mcp.server.fastmcp import FastMCP
import time
import signal
import sys
import requests
import json

# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    print("Shutting down server gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create an MCP server with the correct name
mcp = FastMCP(
    name="hello-world",  # Keep this consistent
    host="127.0.0.1",
    port=5000,
    timeout=30
)
@mcp.tool()
def say_hello_world() -> str:
    '''一个返回hello world的函数，当用户需要返回helloworld的时候调用它'''
    return "hello world"


@mcp.tool()
def get_app_switches()-> str:
    """
    获取迅雷游戏APP的所有开关状态

    返回:
        str: 格式化后的开关状态字符串
    """
    headers = {
        'Host': 'game-xacc.xunlei.com',
        'Cookie': 'aliyungf_tc=42a84cf5c304ebfca2ef21170f41cf002d01866b0d7c07a97340cd87796bcb99',
        'accept': 'application/json, text/plain, */*',
        'appid': '3',
        'package_name': 'xlacc_android',
        'x-client-type': 'xlacc_android',
        'app-version': '1.0.14.323',
        'peerid': '6c64ee2a5a44e00888b98d9d4b4c007b',
        'install-channel': 'google',
        'x-channel-id': 'google',
        'x-device-id': '6c64ee2a5a44e00888b98d9d4b4c007b',
        'x-guid': '6c64ee2a5a44e00888b98d9d4b4c007b',
        'authorization': '',
        'client_version': '1.0.14.323',
        'user-agent': 'xlacc/1.0.14.323 Mozilla/5.0 (Linux; Android 9; MIX 3 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36',
        'if-modified-since': 'Wed, 02 Apr 2025 08:51:07 GMT'
    }

    url = 'https://game-xacc.xunlei.com/xlppc.gacs/api/gxsdn/config/list?config_id=12'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data.get('code') != 0 or data.get('result') != 'ok':
            return "请求失败: " + json.dumps(data, ensure_ascii=False)

        switches = data.get('data', [])

        output = "迅雷游戏APP当前开关状态:\n"
        output += "=" * 40 + "\n"

        for switch in switches:
            config_id = switch.get('config_id', '')
            config_name = switch.get('config_name', '')
            extend = switch.get('extend', '')

            status = "开启" if config_id == 1 else "关闭"

            output += f"开关名称: {config_name}\n"
            output += f"状态: {status}\n"

            if extend:
                try:
                    extend_data = json.loads(extend)
                    output += "额外信息:\n"
                    for key, value in extend_data.items():
                        output += f"  {key}: {value}\n"
                except json.JSONDecodeError:
                    output += f"额外信息: {extend}\n"

            output += "-" * 40 + "\n"

        return output

    except requests.exceptions.RequestException as e:
        return f"请求发生错误: {str(e)}"
    except json.JSONDecodeError:
        return "解析响应数据失败"


# 调用方法并打印结果
switches_info = get_app_switches()
print(switches_info)
if __name__ == "__main__":
    try:
        print(f"Starting MCP server 'hello-world'...")
        mcp.run()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)