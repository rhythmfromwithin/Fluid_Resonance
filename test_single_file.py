import os
import re

def process_single_file(file_path):
    """
    处理单个Markdown文件，在每行末尾添加两个空格和换行符
    
    Args:
        file_path: 要处理的Markdown文件路径
    """
    # 确保文件存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        return
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 用于匹配Status: PublishReady的正则表达式
    status_pattern = re.compile(r'Status:\s*PublishReady', re.IGNORECASE)
    
    # 检查文件是否包含Status: PublishReady
    if status_pattern.search(content):
        print(f"处理文件: {file_path}")
        
        # 处理每一行：在行尾添加两个空格和换行符
        lines = content.splitlines()
        modified_lines = [line + '  ' for line in lines]
        modified_content = '\n'.join(modified_lines)
        
        # 创建备份文件
        backup_path = file_path + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"原文件已备份到: {backup_path}")
        
        # 保存修改后的内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"已完成: {file_path}")
        return True
    else:
        print(f"跳过 (非PublishReady): {file_path}")
        return False

if __name__ == "__main__":
    # 指定要测试的单个文件路径
    test_file = input("请输入要测试的Markdown文件的完整路径: ")
    process_single_file(test_file)