import os
import pkg_resources
import subprocess
import sys

def get_package_size(package_name):
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', '-f', package_name],
            capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore'
        )
        lines = result.stdout.splitlines()
        file_section = False
        size = 0
        files = []
        location = None
        for line in lines:
            if line.startswith('Location:'):
                location = line.split(':', 1)[1].strip()
            if line.startswith('Files'):
                file_section = True
                continue
            if file_section:
                if line.strip() == '':
                    break
                files.append(line.strip())
        
        if location is None:
            print(f"Warning: No location found for package {package_name}")
            return size
        
        for file_path in files:
            full_path = os.path.join(location, file_path)
            if os.path.exists(full_path):
                size += os.path.getsize(full_path)
            else:
                # Suppressing the warning for a cleaner output
                # print(f"Warning: File not found {full_path}")
                pass
        
        return size
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving package information for {package_name}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred for {package_name}: {e}")
        return None

def list_installed_packages():
    installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}
    max_package_len = max(len(package_name) for package_name in installed_packages.keys())
    max_version_len = max(len(version) for version in installed_packages.values())
    
    print("Package Name".ljust(max_package_len + 4) + "Version".ljust(max_version_len + 4) + "Size")
    print("-" * (max_package_len + max_version_len + 12))
    
    for package_name, version in installed_packages.items():
        size = get_package_size(package_name)
        if size is not None:
            print(package_name.ljust(max_package_len + 4) + version.ljust(max_version_len + 4) + f"{size / (1024 ** 2):.2f} MB")

if __name__ == "__main__":
    list_installed_packages()
