import os
import subprocess
import shutil
import re
import datetime
import sys

# This script should be placed in the 2_Publishing folder
base_dir = os.path.dirname(os.path.abspath(__file__))  # 2_Publishing folder
archive_dir = os.path.join(os.path.dirname(base_dir), '9_Archive')

# Create log file
log_file = os.path.join(base_dir, f'publish_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

def log_message(message, also_print=True):
    """Log message to file and optionally print"""
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        if also_print:
            print(message)
    except Exception as e:
        print(f"Cannot write to log: {e}")
        print(f"Original message: {message}")

def run_script(script_name, filepath):
    """Run a Python script on a file"""
    script_path = os.path.join(base_dir, script_name)
    
    if not os.path.exists(script_path):
        log_message(f"Error: Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_path, filepath], 
                              capture_output=True, text=True, check=True)
        log_message(f"Successfully ran {script_name} on {os.path.basename(filepath)}")
        if result.stdout:
            log_message(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Error running {script_name}: {e}")
        if e.stderr:
            log_message(f"Error output: {e.stderr}")
        return False

def git_push_file(filepath, filename):
    """Push file to GitHub"""
    try:
        # Add file to git
        subprocess.run(['git', 'add', filepath], check=True, capture_output=True, text=True)
        
        # Commit file
        commit_message = f"Publish: {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True, text=True)
        
        # Push to remote repository
        subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)
        
        log_message(f"Successfully pushed to GitHub: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Git operation failed: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            log_message(f"Error output: {e.stderr}")
        return False

def update_status_to_published(filepath):
    """Update status to Published in the file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to update both old and new format
        # Old format
        if re.search(r'^Status:\s*.+?$', content, re.MULTILINE):
            content = re.sub(r'^Status:\s*.+?$', 'Status: Published', content, flags=re.MULTILINE)
        # New format (in custom section)
        elif re.search(r'custom:[\s\S]*?Status:\s*.+?(?:\n|$)', content):
            content = re.sub(r'(custom:[\s\S]*?)Status:\s*.+?(?=\n)', r'\1Status: Published', content)
        else:
            log_message(f"Warning: No Status field found in {filepath}")
            return False
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        log_message(f"Updated status to Published: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        log_message(f"Error updating status: {e}")
        return False

def move_to_archive(filepath):
    """Move file to archive folder"""
    try:
        # Get relative path from publishing folder
        relative_path = os.path.relpath(os.path.dirname(filepath), base_dir)
        filename = os.path.basename(filepath)
        
        # Create archive directory structure
        archive_path = os.path.join(archive_dir, relative_path)
        os.makedirs(archive_path, exist_ok=True)
        
        # Move file
        dest_file = os.path.join(archive_path, filename)
        if os.path.exists(dest_file):
            os.remove(dest_file)
        
        shutil.move(filepath, dest_file)
        log_message(f"Moved to archive: {dest_file}")
        return True
    except Exception as e:
        log_message(f"Error moving to archive: {e}")
        return False

def publish_file(filepath):
    """Complete publishing workflow for a single file"""
    filename = os.path.basename(filepath)
    log_message(f"\n=== Publishing {filename} ===")
    
    # Step 1: Run add_line_breaks.py
    if not run_script('add_line_breaks.py', filepath):
        log_message(f"Failed at step 1 (add_line_breaks) for {filename}")
        return False
    
    # Step 2: Run convert_frontmatter.py
    if not run_script('convert_frontmatter.py', filepath):
        log_message(f"Failed at step 2 (convert_frontmatter) for {filename}")
        return False
    
    # Step 3: Push to GitHub
    if not git_push_file(filepath, filename):
        log_message(f"Failed at step 3 (git push) for {filename}")
        return False
    
    # Step 4: Change Status to Published
    if not update_status_to_published(filepath):
        log_message(f"Failed at step 4 (update status) for {filename}")
        return False
    
    # Step 5: Move to Archive
    if not move_to_archive(filepath):
        log_message(f"Failed at step 5 (move to archive) for {filename}")
        return False
    
    log_message(f"Successfully published: {filename}")
    return True

def publish_all_files():
    """Process all markdown files in the publishing folder"""
    log_message("Starting publishing workflow...")
    
    success_count = 0
    fail_count = 0
    
    # Find all markdown files in the publishing folder
    for root, dirs, files in os.walk(base_dir):
        # Skip the archive directory if it's somehow inside publishing
        if '9_Archive' in root:
            continue
            
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                
                if publish_file(filepath):
                    success_count += 1
                else:
                    fail_count += 1
    
    log_message(f"\nPublishing complete: {success_count} succeeded, {fail_count} failed")
    return success_count, fail_count

if __name__ == "__main__":
    print("Publishing Workflow Script")
    print(f"Publishing directory: {base_dir}")
    print(f"Archive directory: {archive_dir}")
    print("="*50)
    
    # Check if the required scripts exist
    required_scripts = ['add_line_breaks.py', 'convert_frontmatter.py']
    missing_scripts = []
    
    for script in required_scripts:
        script_path = os.path.join(base_dir, script)
        if not os.path.exists(script_path):
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"Error: Missing required scripts: {', '.join(missing_scripts)}")
        print("Please ensure these scripts are in the publishing folder.")
        sys.exit(1)
    
    # Check git status
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository")
        sys.exit(1)
    
    # Process all files
    success, fail = publish_all_files()
    
    print(f"\nDone! Published {success} files, {fail} failures")
    print(f"Log file: {log_file}")