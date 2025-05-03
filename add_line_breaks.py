import os
import re
import glob

def process_markdown_files(directory='/Users/sabrinazhang/Dropbox/1_PublishReady'):
    """
    处理指定目录及其所有子目录下状态为PublishReady的Markdown文件，
    在每行末尾添加两个空格和换行符
    
    Args:
        directory: 要处理的目录，默认为指定的PublishReady目录
    """
    # 确保目录存在
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return
        
    # 查找目录及其所有子目录中的.md文件
    md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
    
    # 修改正则表达式，同时支持原始格式和转换后的格式
    # 可以匹配以下两种情况:
    # 1. Status: PublishReady
    # 2. custom: ... Status: PublishReady
    status_pattern = re.compile(r'(Status:|custom:[\s\S]*?Status:)\s*PublishReady', re.IGNORECASE)
    
    processed_count = 0
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 检查文件是否包含Status: PublishReady
        if status_pattern.search(content):
            print(f"处理文件: {file_path}")
            
            # 检查文件是否已经处理过
            already_processed = True
            lines = content.splitlines()
            for line in lines:
                if not line.endswith('  ') and line.strip():  # 不以两个空格结尾且不是空行
                    already_processed = False
                    break
            
            if already_processed:
                print(f"已跳过 (文件已处理): {file_path}")
                continue
            
            # 处理每一行：在行尾添加两个空格和换行符
            modified_lines = []
            for line in lines:
                if line.strip():  # 非空行
                    if not line.endswith('  '):  # 如果不以两个空格结尾
                        modified_lines.append(line + '  ')
                    else:
                        modified_lines.append(line)  # 已经有空格，保持不变
                else:
                    modified_lines.append(line)  # 空行保持不变
            
            modified_content = '\n'.join(modified_lines)
            
            # 保存修改后的内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            
            print(f"已完成: {file_path}")
            processed_count += 1
        else:
            print(f"跳过 (非PublishReady): {file_path}")
    
    print(f"处理完成: 共处理了 {processed_count} 个文件")

if __name__ == "__main__":
    # 允许用户指定目录路径
    default_dir = '/Users/sabrinazhang/Dropbox/1_PublishReady'
    custom_dir = input(f"请输入要处理的目录路径 (直接回车使用默认路径: {default_dir}): ")
    
    # 如果用户输入为空，使用默认目录
    directory_to_process = custom_dir if custom_dir.strip() else default_dir
    
    # 在指定目录及其所有子目录中处理Markdown文件
    process_markdown_files(directory_to_process)