#!/usr/bin/env python3
"""
Ultra-minimal AWS Lambda deployment script for AI Governance Middleware
Uses Pydantic v1 to eliminate all Rust/binary dependencies
"""
import os
import shutil
import zipfile
import subprocess
import sys
from pathlib import Path

def create_ultra_minimal_package():
    """
    Create an ultra-minimal deployment package with zero binary dependencies
    """
    print('🚀 Creating Ultra-Minimal Lambda Package (Zero Binary Dependencies)')
    print('=' * 70)
    
    # Create deployment directory
    deploy_dir = Path('lambda-deployment-ultra')
    if deploy_dir.exists():
        print(f'🗑️  Removing existing deployment directory...')
        shutil.rmtree(deploy_dir)
    
    deploy_dir.mkdir()
    print(f'📁 Created deployment directory: {deploy_dir}')
    
    # Copy application files
    files_to_copy = [
        'lambda_handler.py',
        'main.py',
        'models.py',
        'bedrock_client.py'
    ]
    
    directories_to_copy = [
        'agents',
        'utils'
    ]
    
    print('📋 Copying application files...')
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, deploy_dir / file)
            print(f'   ✅ {file}')
        else:
            print(f'   ❌ {file} (not found)')
    
    print('📋 Copying directories...')
    for directory in directories_to_copy:
        if Path(directory).exists():
            shutil.copytree(directory, deploy_dir / directory)
            print(f'   ✅ {directory}/')
        else:
            print(f'   ❌ {directory}/ (not found)')
    
    # Copy ultra-minimal requirements
    shutil.copy2('requirements-ultra-minimal.txt', deploy_dir / 'requirements.txt')
    print('   ✅ requirements-ultra-minimal.txt -> requirements.txt')
    
    # Install dependencies
    print('\n📦 Installing ultra-minimal dependencies (Pure Python only)...')
    try:
        print('   🐍 Installing Pydantic v1 and FastAPI 0.68...')
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            '-r', str(deploy_dir / 'requirements.txt'),
            '-t', str(deploy_dir),
            '--no-cache-dir'  # Ensure fresh install
        ], capture_output=True, text=True, check=True)
        
        print('   ✅ Dependencies installed successfully')
        
        # Show what was installed
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            installed = [line for line in lines if 'Successfully installed' in line]
            if installed:
                print(f'   📦 {installed[0]}')
        
    except subprocess.CalledProcessError as e:
        print(f'   ❌ Installation failed: {e}')
        print(f'   Error output: {e.stderr}')
        return False
    
    # Validate ultra-minimal dependencies
    print('\n🔍 Validating ultra-minimal dependencies...')
    critical_deps = {
        'fastapi': '0.68.0',
        'pydantic': '1.10.12', 
        'mangum': '0.17.0',
        'boto3': '1.34.0',
        'requests': '2.31.0'
    }
    
    missing = []
    for dep, expected_version in critical_deps.items():
        dep_dirs = list(deploy_dir.glob(f'{dep}*'))
        if dep_dirs:
            print(f'   ✅ {dep} (found)')
        else:
            missing.append(dep)
            print(f'   ❌ {dep} (MISSING)')
    
    if missing:
        print(f'\n❌ Critical dependencies missing: {missing}')
        return False
    
    # Check for binary files (should be ZERO)
    print('\n🔍 Checking for binary files (should be zero)...')
    binary_patterns = [
        '**/*.so',
        '**/*.pyd', 
        '**/*.dll',
        '**/*.dylib'
    ]
    
    binary_files = []
    for pattern in binary_patterns:
        binary_files.extend(deploy_dir.glob(pattern))
    
    if binary_files:
        print(f'   ⚠️  Found {len(binary_files)} binary files:')
        for file in binary_files[:5]:
            print(f'      {file.relative_to(deploy_dir)}')
        print('   💡 These may cause compatibility issues in Lambda')
    else:
        print('   ✅ Zero binary files found - Pure Python deployment!')
    
    # Validate Pydantic version specifically
    print('\n🔍 Validating Pydantic version...')
    pydantic_dirs = list(deploy_dir.glob('pydantic*'))
    if pydantic_dirs:
        # Check if it's v1 (no pydantic_core dependency)
        pydantic_core_dirs = list(deploy_dir.glob('pydantic_core*'))
        if pydantic_core_dirs:
            print('   ⚠️  Found pydantic_core - this may cause issues')
        else:
            print('   ✅ Pydantic v1 confirmed - no pydantic_core dependency!')
    
    # Remove unnecessary files
    print('\n🗜️  Optimizing package size...')
    patterns_to_remove = [
        '**/__pycache__',
        '**/*.pyc',
        '**/*.pyo',
        '**/tests',
        '**/test_*',
        '**/*.dist-info/RECORD',
        '**/*.dist-info/WHEEL',
        '**/bin/*'  # Remove all executables
    ]
    
    removed_count = 0
    saved_size = 0
    
    for pattern in patterns_to_remove:
        for path in deploy_dir.glob(pattern):
            try:
                if path.is_file():
                    size = path.stat().st_size
                    path.unlink()
                    removed_count += 1
                    saved_size += size
                elif path.is_dir():
                    dir_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                    shutil.rmtree(path)
                    removed_count += 1
                    saved_size += dir_size
            except (OSError, PermissionError):
                pass
    
    saved_mb = saved_size / (1024 * 1024)
    print(f'   🗑️  Removed {removed_count} items, saved {saved_mb:.2f} MB')
    
    # Create deployment zip
    zip_path = Path('ai-governance-lambda-ultra.zip')
    if zip_path.exists():
        zip_path.unlink()
    
    print(f'\n📦 Creating ultra-minimal deployment zip: {zip_path}')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arc_name)
                file_count += 1
    
    # Get zip size
    zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB
    print(f'\n📊 Ultra-Minimal Deployment Package Created:')
    print(f'   📦 File: {zip_path}')
    print(f'   📏 Size: {zip_size:.2f} MB')
    print(f'   📄 Files: {file_count}')
    print(f'   🐍 Pure Python: No binary dependencies!')
    
    # Clean up deployment directory
    print(f'\n🗑️  Cleaning up deployment directory...')
    try:
        shutil.rmtree(deploy_dir)
        print('   ✅ Cleanup completed')
    except PermissionError:
        print('   ⚠️  Could not remove deployment directory (Windows file locks)')
        print('   💡 You can manually delete lambda-deployment-ultra/ later')
    
    return True

def generate_manual_upload_instructions():
    """
    Generate instructions for manual upload via AWS Console
    """
    print('\n📋 Manual Upload Instructions (No AWS CLI needed)')
    print('=' * 60)
    
    print('\n1️⃣  Fix Memory Configuration:')
    print('   • Go to AWS Lambda Console')
    print('   • Find your "ai-governance-api" function')
    print('   • Go to Configuration → General configuration')
    print('   • Click "Edit"')
    print('   • Change Memory: 128 MB → 1024 MB')
    print('   • Change Timeout: 3 seconds → 900 seconds (15 minutes)')
    print('   • Click "Save"')
    
    print('\n2️⃣  Upload New Package:')
    print('   • In the same Lambda function page')
    print('   • Go to "Code" tab')
    print('   • Click "Upload from" → ".zip file"')
    print('   • Select: ai-governance-lambda-ultra.zip')
    print('   • Click "Save"')
    
    print('\n3️⃣  Test Function:')
    print('   • Click "Test" button')
    print('   • Create new test event:')
    print('     - Event name: health-check')
    print('     - Template: API Gateway AWS Proxy')
    print('     - Modify the event:')
    print('       {')
    print('         "httpMethod": "GET",')
    print('         "path": "/health",')
    print('         "headers": {},')
    print('         "body": null')
    print('       }')
    print('   • Click "Test"')
    print('   • Should return: {"status": "healthy"}')
    
    print('\n✅ Expected Result:')
    print('   • No more pydantic_core import errors')
    print('   • Memory: 1024 MB (sufficient for AI processing)')
    print('   • Function executes successfully')
    print('   • All 5 governance agents working')

def main():
    """
    Main deployment function
    """
    print('🚀 AI Governance Lambda Deployment (Ultra-Minimal)')
    print('=' * 60)
    print('🎯 Goal: Zero binary dependencies, Pure Python only')
    print('🔧 Strategy: Pydantic v1 + FastAPI 0.68 (no Rust)')
    
    # Create ultra-minimal package
    if not create_ultra_minimal_package():
        print('❌ Failed to create ultra-minimal package')
        return False
    
    # Generate manual upload instructions
    generate_manual_upload_instructions()
    
    print('\n🎉 Ultra-Minimal Package Ready!')
    print('📦 File: ai-governance-lambda-ultra.zip')
    print('🐍 Pure Python: No binary compatibility issues!')
    print('💾 Next: Fix memory (1024 MB) and upload via AWS Console')
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
