import os
import re
import yaml
from datetime import datetime

def process_markdown_file(file_path):
    # 确保文件路径是有效的
    file_path = os.path.normpath(file_path)
    
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    # 更改这部分，使用更灵活的正则表达式来匹配前置元数据块
    # 这个新正则表达式可以匹配以下情况:
    # 1. --- 开始和结束，中间可能有任意空白字符
    # 2. 允许前置元数据和分隔符之间存在空格
    # 3. 允许Windows风格的换行符 (\r\n)
    front_matter_pattern = r'^\s*---\s*[\r\n]+(.*?)[\r\n]+\s*---'
    match = re.search(front_matter_pattern, content, re.DOTALL)
    
    if not match:
        # 如果找不到标准格式，尝试寻找替代格式
        alt_pattern = r'^\s*---\s*(.*?)\s*---'
        match = re.search(alt_pattern, content, re.DOTALL)
        
        if not match:
            print(f"无法在文件 {file_path} 中找到前置元数据块")
            # 创建一个日志文件，记录出错的文件和内容的前100个字符
            with open("frontmatter_error_log.txt", "a", encoding="utf-8") as log:
                log.write(f"文件: {file_path}\n")
                log.write(f"内容前100个字符: {content[:100]}\n")
                log.write("-" * 50 + "\n")
            return
    
    # 提取前置元数据和正文内容
    front_matter_text = match.group(1)
    
    # 获取整个前置元数据块，包括前后的 ---
    entire_front_matter = match.group(0)
    
    # 获取前置元数据块结束后的所有内容作为正文（保持原始格式）
    body_start_index = content.find(entire_front_matter) + len(entire_front_matter)
    body_content = content[body_start_index:]
    
    # 获取前置元数据块开始前的所有内容作为前缀
    prefix_content = content[:content.find(entire_front_matter)]
    
    # 解析原始前置元数据 - 手动解析而不是用YAML库
    front_matter = {}
    lines = front_matter_text.strip().split('\n')
    for line in lines:
        # 跳过空行
        if not line.strip():
            continue
            
        # 尝试拆分每一行为键值对
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            front_matter[key] = value
    
    # 创建新的前置元数据结构
    new_front_matter = {
        "title": f'"{front_matter.get("Title", "")}"',
        "subtitle": f'"{front_matter.get("Theme", "")}"',
        "date": front_matter.get("EditingCompletion", ""),
        "custom": {
            "Status": front_matter.get("Status", ""),
            "WritingStart": front_matter.get("WritingStart", ""),
            "Completion": front_matter.get("Completion", ""),
            "EditingCompletion": front_matter.get("EditingCompletion", ""),
            "PlannedPublication": front_matter.get("PlannedPublication", ""),
            "ActualPublication": front_matter.get("ActualPublication", ""),
            "Notes": front_matter.get("Notes", "")
        }
    }
    
    # 手动构建YAML文本，确保保留格式
    new_front_matter_text = f"""title: {new_front_matter['title']}
subtitle: {new_front_matter['subtitle']}
date: {new_front_matter['date']}
custom:
  Status: {new_front_matter['custom']['Status']}
  WritingStart: {new_front_matter['custom']['WritingStart']}
  Completion: {new_front_matter['custom']['Completion']}
  EditingCompletion: {new_front_matter['custom']['EditingCompletion']}
  PlannedPublication: {new_front_matter['custom']['PlannedPublication']}
  ActualPublication: {new_front_matter['custom']['ActualPublication']}
  Notes: {new_front_matter['custom']['Notes']}"""
    
    # 关键改进：保留行尾空格
    # 使用splitlines(True)来保留每行的换行符
    body_lines = body_content.splitlines(True)
    preserved_body = ''.join(body_lines)
    
    # 创建新的内容，保留前缀内容和原始正文格式
    # 注意：确保保留正文前的换行符
    new_content = f"{prefix_content}---\n{new_front_matter_text}\n---{preserved_body}"
    
    # 输出新内容
    dir_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    base_name, ext = os.path.splitext(file_name)
    output_path = os.path.join(dir_path, f"{base_name}_converted{ext}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"已处理文件 {file_path} 并保存到 {output_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

def process_directory(directory_path):
    if not os.path.exists(directory_path):
        print(f"错误: 目录不存在: {directory_path}")
        return
    
    md_files_count = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_markdown_file(file_path)
                md_files_count += 1
    
    print(f"已处理 {md_files_count} 个 .md 文件")

def list_subdirectories(root_path='.'):
    """列出指定目录下的所有子目录"""
    subdirectories = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            subdirectories.append(item)
    return subdirectories

def preview_file_content(file_path):
    """预览文件内容的前100个字符，帮助诊断问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read(100)  # 只读取前100个字符
        print(f"\n文件 {file_path} 的前100个字符:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
        # 显示字符的ASCII/Unicode编码，帮助检测隐藏字符
        print("字符编码:")
        for i, char in enumerate(content[:30]):  # 仅显示前30个字符的编码
            print(f"位置 {i}: '{char}' - {ord(char)}")
    except Exception as e:
        print(f"预览文件时出错: {e}")

if __name__ == "__main__":
    print("YAML前置元数据转换脚本 (增强版)")
    print("============================")
    
    # 获取当前目录（脚本所在目录）
    current_dir = os.path.dirname(os.path.abspath(__file__)) or '.'
    
    # 列出子目录
    subdirectories = list_subdirectories(current_dir)
    
    if not subdirectories:
        print("当前目录中没有找到任何子目录")
        print("选项4: 输入完整文件路径进行处理")
        choice = '4'  # 默认选择选项4
    else:
        print("当前目录中的子目录:")
        for i, subdir in enumerate(subdirectories, 1):
            print(f"{i}. {subdir}")
        
        print("\n选择操作:")
        print("1. 处理单个子目录中的所有.md文件")
        print("2. 处理所有子目录中的所有.md文件")
        print("3. 处理指定的单个.md文件")
        print("4. 输入完整文件路径进行处理")
        print("5. 预览文件内容（诊断问题用）")
        
        choice = input("请选择操作 (1/2/3/4/5): ")
    
    if choice == '1':
        dir_num = int(input(f"请输入要处理的子目录编号 (1-{len(subdirectories)}): "))
        if 1 <= dir_num <= len(subdirectories):
            dir_path = os.path.join(current_dir, subdirectories[dir_num - 1])
            process_directory(dir_path)
        else:
            print("无效的目录编号")
    
    elif choice == '2':
        for subdir in subdirectories:
            dir_path = os.path.join(current_dir, subdir)
            print(f"\n处理目录: {subdir}")
            process_directory(dir_path)
    
    elif choice == '3':
        dir_num = int(input(f"请选择子目录编号 (1-{len(subdirectories)}): "))
        if 1 <= dir_num <= len(subdirectories):
            dir_path = os.path.join(current_dir, subdirectories[dir_num - 1])
            
            # 列出选定子目录中的所有.md文件
            md_files = []
            for file in os.listdir(dir_path):
                if file.endswith('.md'):
                    md_files.append(file)
            
            if not md_files:
                print(f"在 {subdirectories[dir_num - 1]} 目录中没有找到任何.md文件")
            else:
                print(f"\n在 {subdirectories[dir_num - 1]} 目录中的.md文件:")
                for i, file in enumerate(md_files, 1):
                    print(f"{i}. {file}")
                
                file_num = int(input(f"请输入要处理的文件编号 (1-{len(md_files)}): "))
                if 1 <= file_num <= len(md_files):
                    file_path = os.path.join(dir_path, md_files[file_num - 1])
                    process_markdown_file(file_path)
                else:
                    print("无效的文件编号")
        else:
            print("无效的目录编号")
    
    elif choice == '4':
        file_path = input("请输入完整的文件路径: ")
        if os.path.isfile(file_path):
            process_markdown_file(file_path)
        else:
            print(f"错误: 无效的文件路径: {file_path}")
    
    elif choice == '5':
        file_path = input("请输入要预览的文件路径: ")
        if os.path.isfile(file_path):
            preview_file_content(file_path)
        else:
            print(f"错误: 无效的文件路径: {file_path}")
    
    else:
        print("无效的选择")