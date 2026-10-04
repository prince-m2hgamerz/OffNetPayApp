import os
import re
from pathlib import Path

# Paths to ignore
IGNORE_DIRS = {'.git', '.gradle', 'build', 'node_modules', '.idea', 'captures', 'gradle'}
IGNORE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.class', '.jar', '.apk', '.keystore', '.jks', '.mp4'}

def replace_in_string(content):
    # Developer names
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz \\u0026 m2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    
    # Specific harsh links or names if they stand alone might be trickier, but let's do the main ones
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content) # Might be risky, but let's assume it's just the dev
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)
    content = re.sub(r'm2hgamerz', 'm2hgamerz', content, flags=re.IGNORECASE)

    # Brand names
    content = re.sub(r'OffNetPay', 'OffNetPay', content)
    content = re.sub(r'offnetpay', 'offnetpay', content)
    content = re.sub(r'OFFNETPAY', 'OFFNETPAY', content)
    
    # URL variants
    content = re.sub(r'OffNetPayApp', 'OffNetPayApp', content, flags=re.IGNORECASE)
    
    return content

def process_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files that don't have matched extension
    
    new_content = replace_in_string(content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {path}")

def rename_path(path):
    name = path.name
    new_name = replace_in_string(name)
    if new_name != name:
        new_path = path.with_name(new_name)
        path.rename(new_path)
        print(f"Renamed {path} -> {new_path}")
        return new_path
    return path

def main(root_dir):
    root = Path(root_dir)
    
    # Rename file contents
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        for filename in filenames:
            if any(filename.endswith(ext) for ext in IGNORE_EXTS):
                continue
            filepath = Path(dirpath) / filename
            process_file(filepath)
            
    # Rename directories and files bottom-up to avoid breaking paths
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        d_path = Path(dirpath)
        if any(ignored in d_path.parts for ignored in IGNORE_DIRS):
            continue
            
        for filename in filenames:
            f_path = d_path / filename
            rename_path(f_path)
            
        rename_path(d_path)

if __name__ == '__main__':
    main('.')
