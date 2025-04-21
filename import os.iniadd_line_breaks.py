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
    
    # 用于匹配Status: PublishReady的正则表达式
    status_pattern = re.compile(r'Status:\s*PublishReady', re.IGNORECASE)
    
    processed_count = 0
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 检查文件是否包含Status: PublishReady
        if status_pattern.search(content):
            print(f"处理文件: {file_path}")
            
            # 处理每一行：在行尾添加两个空格和换行符
            lines = content.splitlines()
            modified_lines = [line + '  ' for line in lines]
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
    # 在指定目录及其所有子目录中处理Markdown文件
    process_markdown_files()