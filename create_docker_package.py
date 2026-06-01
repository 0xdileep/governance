import os
import shutil
import zipfile
import logging
import subprocess

# --- Configuration ---
# Make sure your requirements file is named 'requirements.txt'
REQUIREMENTS_FILE = "requirements.txt"
DOCKER_IMAGE_NAME = "ai-governance-builder"
PACKAGE_DIR = "package"
ZIP_FILE_NAME = "lambda_deployment_package.zip"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_docker():
    """Checks if Docker is running."""
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        logger.info("✅ Docker is running.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("❌ Docker is not running. Please start Docker Desktop and try again.")
        return False

def main():
    if not check_docker():
        return

    logger.info("--- Step 1: Building Linux dependencies inside Docker ---")

    # Clean up previous build artifacts
    if os.path.exists(PACKAGE_DIR):
        shutil.rmtree(PACKAGE_DIR)
    if os.path.exists(ZIP_FILE_NAME):
        os.remove(ZIP_FILE_NAME)

    try:
        # Build the Docker image
        logger.info(f"Building Docker image '{DOCKER_IMAGE_NAME}'...")
        subprocess.run(
            ["docker", "build", "-t", DOCKER_IMAGE_NAME, "."],
            check=True, capture_output=True
        )

        # Create a container from the image to copy files from
        logger.info("Creating temporary container to extract packages...")
        container_id = subprocess.check_output(
            ["docker", "create", DOCKER_IMAGE_NAME]
        ).decode('utf-8').strip()

        # Copy the 'package' directory from the container to the local filesystem
        logger.info(f"Copying dependencies from container '{container_id[:12]}'")
        subprocess.run(
            ["docker", "cp", f"{container_id}:/var/task/package", "."],
            check=True, capture_output=True
        )

    finally:
        # Clean up the temporary container
        if 'container_id' in locals():
            logger.info("Cleaning up temporary container...")
            subprocess.run(
                ["docker", "rm", "-v", container_id],
                check=True, capture_output=True
            )

    logger.info("--- Step 2: Packaging application source code ---")

    # Copy your application source code into the 'package' directory
    logger.info("Copying application source code...")
    excluded_files = {
        'create_package.py',
        'create_package_docker.py',
        'deploy_lambda.py',
        ZIP_FILE_NAME,
        '.gitignore',
        'README.md',
        'Dockerfile'
    }
    excluded_dirs = {'.git', '__pycache__', '.vscode', '.idea'}

    for item in os.listdir('.'):
        if item in excluded_files or item in excluded_dirs or item == PACKAGE_DIR:
            continue
        source_path = os.path.join('.', item)
        dest_path = os.path.join(PACKAGE_DIR, item)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path, ignore=shutil.ignore_patterns('*pycache*'))
        else:
            shutil.copy2(source_path, dest_path)

    # Zip the final package
    logger.info(f"Creating final deployment package: '{ZIP_FILE_NAME}'...")
    with zipfile.ZipFile(ZIP_FILE_NAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(PACKAGE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, PACKAGE_DIR)
                zf.write(file_path, archive_name)

    logger.info("🎉 Success! Your Lambda package is ready for upload.")

if __name__ == "__main__":
    # Rename your requirements file if needed
    if not os.path.exists(REQUIREMENTS_FILE):
        if os.path.exists("requirements-ultra-minimal.txt"):
            os.rename("requirements-ultra-minimal.txt", REQUIREMENTS_FILE)
        else:
            logger.error(f"'{REQUIREMENTS_FILE}' not found. Please create it.")
    else:
        main()