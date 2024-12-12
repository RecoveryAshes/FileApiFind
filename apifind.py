import os
import re
from datetime import datetime
import argparse

def wr(file_path, content):
    with open(file_path, 'a') as f:
        f.write(content)

def scan_directory(directory, output_name=None):
    if not output_name:
        timestamp = int(datetime.now().timestamp())
        output_name = f'{timestamp}'

    apilist = []
    api_file_path = f'api-{output_name}.txt'
    path_file_path = f'pwd-{output_name}.txt'

    api_pattern = re.compile(r"""(['"]\/[^][^>< \)\(\{\}]*?['"])""")

    """递归扫描指定目录下的 .js 文件，并匹配其中的 API 接口"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = api_pattern.findall(content)
                    if matches:
                        for match in matches:
                            wr(path_file_path, f'{file_path} ==> {match.strip()[1:-1]}\n')
                            print(f'{file_path} ==> {match.strip()[1:-1]}')
                            apilist.append(match.strip()[1:-1])
    apilist = list(dict.fromkeys(apilist))
    for item in apilist:
        wr(api_file_path, f'{item}\n')
        print(item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan a directory.')
    
    parser.add_argument('-r', '--path', type=str, help='需扫描的路径')
    parser.add_argument('-o', '--output', type=str, help='输出文件的名称（不含扩展名）')

    args = parser.parse_args()

    if args.path:
        scan_directory(args.path, args.output)
    else:
        print("Please provide a directory path with the '-r' or '--path' argument.")
