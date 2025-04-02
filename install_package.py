import subprocess
import sys
import time


def verify_pip_installment():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        print("ERROR: pip is not installed!\nPlease install pip before running this script.\n\n\nExiting...", file=sys.stderr)
        time.sleep(5)
        sys.exit(1)


def is_package_installed(package):
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package):
    if is_package_installed(package):
        print(f"Package '{package}' is already installed. Upgrading package...\n")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "."], stderr=sys.stderr)
        if result.returncode == 0:
            print("Installation completed successfully!\n\n\nExiting...")
            time.sleep(5)
            sys.exit(0)
        else:
            print("ERROR: Installation failed!\n\n\nExiting...", file=sys.stderr)
            time.sleep(5)
            sys.exit(2)
    else:
        print("Installing package...\n")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--compile", "."], stderr=sys.stderr)

        if result.returncode == 0:
            print("Installation completed successfully!\n\n\nExiting...")
            time.sleep(5)
            sys.exit(0)
        else:
            print("ERROR: Installation failed!\n\n\nExiting...", file=sys.stderr)
            time.sleep(5)
            sys.exit(2)


if __name__ == "__main__":
    verify_pip_installment()
    install_package("gherkin-processor")
