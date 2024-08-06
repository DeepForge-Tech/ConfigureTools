import platform
import os
import subprocess

delimiter = "========================================================"
current_dir = os.path.dirname(__file__)
REQUIRED_NODEJS_VERSION = 16.0
class Linux:

    def __init__(self):
        self.YUM_PACKAGES = (
            "epel-release boost-devel xterm wget make cmake gcc-c++ curl libcurl sqlite-devel openssl-devel gtest-devel gtest gmock gmock-devel nodejs postgresql libpqxx-devel postgresql-devel postgresql-libs"
        )
        self.DEB_PACKAGES = "libboost-all-dev libasio-dev xterm wget openssl libssl-dev g++ gcc build-essential cmake make curl libcurl4-openssl-dev libjsoncpp-dev libfmt-dev libsqlite3-dev libgtest-dev googletest google-mock libgmock-dev libtbb-dev libzip-dev zlib1g-dev nodejs npm libpq-dev postgresql"
        self.PACMAN_PACKAGES = "boost asio xterm wget jsoncpp gcc base-devel cmake gtest libcurl-compat libcurl-gnutls curl fmt sqlite sqlite-tcl zlib openssl libzip nodejs npm postgresql postgresql-libs"
        # self.ZYPPER_PACKAGES = "xterm wget libcurl-devel gcc-c++ cmake gtest gmock zlib-devel fmt-devel sqlite3-devel jsoncpp-devel"
        self.distribution = platform.freedesktop_os_release()["NAME"]
        self.architecture = platform.architecture()[0]
        self.PACKAGES = {
            "CentOS Linux": self.YUM_PACKAGES,
            "Red Hat Enterprise Linux Server": self.YUM_PACKAGES,
            "Fedora Linux": self.YUM_PACKAGES,
            "Ubuntu": self.DEB_PACKAGES,
            "Debian GNU/Linux": self.DEB_PACKAGES,
            "Linux Mint": self.DEB_PACKAGES,
            "Knoppix": self.DEB_PACKAGES,
            "Raspbian GNU/Linux": self.DEB_PACKAGES,
            "Manjaro Linux": self.PACMAN_PACKAGES,
            "Manjaro ARM": self.PACMAN_PACKAGES,
            "Manjaro AMD64": self.PACMAN_PACKAGES,
            "Arch Linux": self.PACMAN_PACKAGES,
            "Kali GNU/Linux": self.DEB_PACKAGES,
            # "openSUSE Leap": self.ZYPPER_PACKAGES,
            # "openSUSE Tumbleweed": self.ZYPPER_PACKAGES
        }
        self.installer = ""
        self.INSTALLERS = {
            "CentOS Linux": "yum",
            "Red Hat Enterprise Linux Server": "yum",
            "Fedora Linux": "yum",
            "Ubuntu": "apt",
            "Debian GNU/Linux": "apt",
            "Linux Mint": "apt",
            "Knoppix": "apt",
            "Raspbian GNU/Linux": "apt",
            "Manjaro Linux": "pacman",
            "Arch Linux": "pacman",
            "Kali GNU/Linux": "apt",
            "Manjaro ARM": "pacman",
            "Manjaro AMD64": "pacman",
            # "openSUSE Leap": "zypper",
            # "openSUSE Tumbleweed": "zypper"
        }

    def start(self) -> int:
        if self.distribution == "CentOS Linux":
            command = "cd /etc/yum.repos.d/ && sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*"
            os.system(command)
        if self.INSTALLERS[self.distribution] == "yum" or self.INSTALLERS[self.distribution] == "apt":
            command = self.INSTALLERS[
                self.distribution] + " install " + "sudo -y"
            os.system(command)
            command = self.INSTALLERS[self.distribution] + " update " + "-y"
            os.system(command)
        elif self.INSTALLERS[self.distribution] == "pacman":
            command = "sudo " + self.INSTALLERS[self.distribution] + " -Suy --noconfirm"
            os.system(command)
        success_installed = 0
        failed_packages = []
        packages = self.PACKAGES[self.distribution].split()
        for package in packages:
            if self.INSTALLERS[self.distribution] == "yum" or self.INSTALLERS[self.distribution] == "apt":
                command = ("sudo -s " + self.INSTALLERS[self.distribution] +
                           " install " + package + " -y")
                install_result = os.system(command)
            elif self.INSTALLERS[self.distribution] == "pacman":
                command = ("sudo -s " + self.INSTALLERS[self.distribution] +
                           " -Sy " + package + " --noconfirm")
                install_result = os.system(command)
            if install_result == 0:
                success_installed += 1
            else:
                failed_packages.append(package)
        if self.INSTALLERS[self.distribution] == "apt":
            command = "sudo apt autoremove -y"
            os.system(command)
        elif self.INSTALLERS[self.distribution] == "pacman":
            command = "sudo pacman -Scc --noconfirm"
            os.system(command)
        print(delimiter)
        print(
            f"==> Successfully installed: {success_installed} package(s)\n==> Failed to install: {len(packages) - success_installed} package(s)"
        )
        if len(failed_packages) > 0:
            print("==> Reinstall the packages:")
            i = 1
            for package in failed_packages:
                print(f"{i}.{package}")
                i += 1
        return 502


class Windows:

    def __init__(self):
        ps_script_path = os.path.join(current_dir,"InstallWinGet.ps1")
        self.architecture = platform.architecture()[0]
        self.check_functions = {
            "MSBuild":self.checkMSBuild,
            "vcpkg":self.checkVCpkg,
            "NodeJS":self.checkNodeJS
        }
        self.install_commands = {
            "WinGet": f"powershell -noprofile -executionpolicy bypass -File {ps_script_path}",
            "MSBuild": "winget install Microsoft.VisualStudio.2022.BuildTools --override \"--quiet --add Microsoft.VisualStudio.Workload.NativeDesktop\"",
            "vcpkg": "git clone https://github.com/microsoft/vcpkg && .\\vcpkg\\bootstrap-vcpkg.bat -disableMetrics",
            "CMake": "winget install -e --id Kitware.CMake",
            "Boost": "vcpkg install boost asio x64-windows-static",
            "OpenSSL": "vcpkg install openssl x64-windows-static",
            "libpqxx": "vcpkg install libpqxx x64-windows-static",
            "NodeJS": "winget install -e --id OpenJS.NodeJS"
        }

    def checkMSBuild(self) -> bool:
        distributions = ["Enterprise", "Community", "Proffesional"]
        vs_path = "C:\\Program Files\\Microsoft Visual Studio\\"
        msbuild_path = "C:\\Program Files (x86)\\Microsoft Visual Studio\\"
        if os.path.exists(vs_path):
            for obj in os.listdir(vs_path):
                if os.path.isdir(os.path.join(vs_path,obj)) and obj.startswith("20"):
                    for distribution in distributions:
                        if distribution in os.listdir(os.path.join(vs_path, obj)):
                            return len(os.listdir(os.path.join(vs_path, obj,distribution))) > 0
                        
        elif os.path.exists(msbuild_path):
            for obj in os.listdir(msbuild_path):
                if os.path.isdir(os.path.join(msbuild_path,obj)) and obj.startswith("20"):
                    for distribution in distributions:
                        if distribution in os.listdir(os.path.join(msbuild_path, obj)):
                            return len(os.listdir(os.path.join(msbuild_path, obj,distribution))) > 0

    def checkNodeJS(self)  -> bool:
        output  =  subprocess.check_output("node --version", shell=True)
        output =  output.decode("utf-8").strip("\n\rv")[:-2]
        if not float(output) >= REQUIRED_NODEJS_VERSION: return False
        return True

    def checkVCpkg(self)  -> bool:
        os.chdir("C:\\")
        if not os.path.exists("C:\\vcpkg"):
            if not len(os.listdir("C:\\vcpkg")) > 0:
                os.rmdir("C:\\vcpkg")
                return False
        return True

    def checkResult(self, result, nameProgram):
        if result != 0:
            print(delimiter)
            print(f"\033[1;31m==> Failed to install {nameProgram}\033[0m\n")
            print(delimiter)
            return 502

    def start(self) -> int:
        try:
            for key in self.install_commands:
                if key in self.check_functions:
                    result_check = self.check_functions[key]()
                    if result_check == False:
                        print(delimiter)
                        print(f"==> Installing {key}")
                        result = os.system(self.install_commands[key])
                        self.checkResult(result, key)
                else:
                    print(delimiter)
                    print(f"==> Installing {key}")
                    result = os.system(self.install_commands[key])
                    self.checkResult(result, key)
            #     print(
            #         "For further development, Visual Studio or MSBuild is required.\nVisual Studio download link: https://visualstudio.microsoft.com/ru/vs/\nMSBuild download link: https://aka.ms/vs/17/release/vs_BuildTools.exe"
            #     )
            return 0
        except Exception as error:
            print(error)
            return 502


class macOS:

    def __init__(self):
        self.architecture = platform.architecture()[0]
        self.packages = ("jsoncpp sqlite3 sqlite-utils fmt clang-format curl googletest gcc zlib cmake libzip openssl wget boost asio libssh2 unzip zip python@3.12 node postgresql libpq").split()
        self.check_functions = {"XcodeCommandLineTools": self.checkXcodeCommandLineTools}
        self.install_commands = {
            "XcodeCommandLineTools": "xcode-select --install",
            "Homebrew": '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            "zlib": "wget https://github.com/madler/zlib/archive/refs/tags/v1.1.2.zip && unzip v1.1.2.zip && cd zlib-1.1.2 && sudo ./configure && sudo make && sudo make install"
        }

    def checkXcodeCommandLineTools(self) -> bool:
        command = "xcode-select -p"
        return os.system(command) == 0

    def checkResult(self, result, nameProgram):
        if result != 0:
            print(delimiter)
            print(f"\033[1;31m==> Failed to install {nameProgram}\033[0m\n")
            print(delimiter)
            return 502

    def start(self) -> int:
        try:
            for key in self.install_commands:
                # Package verification among verification functions
                if key in self.check_functions:
                    # If the package is not found on the system, it is installed
                    result_check = self.check_functions[key]()
                    if result_check == False:
                        print(delimiter)
                        print(f"==> Installing {key}")
                        result = os.system(self.install_commands[key])
                        self.checkResult(result, key)
                else:
                    print(delimiter)
                    print(f"==> Installing {key}")
                    result = os.system(self.install_commands[key])
                    self.checkResult(result, key)

            success_installed = 0
            failed_packages = []
            for package in self.packages:
                install_result = os.system(f"brew  install  {package}")
                if install_result == 0:
                    success_installed += 1
                else:
                    failed_packages.append(package)
            print(delimiter)
            print(f"==> Successfully installed: {success_installed} package(s)\n==> Failed to install: {len(self.packages) - success_installed} package(s)")
            if len(failed_packages) > 0:
                print("==> Reinstall the packages:")
                i = 1
                # Print the failed installs packages 
                for package in failed_packages:
                    print(f"{i}.{package}")
                    i += 1
            return 0
        except Exception as error:
            print(error)
            return 502

if __name__ == "__main__":
    platforms = {"Linux": Linux, "Windows": Windows, "Darwin": macOS}
    checker = platforms[platform.system()]()
    print("==> Installing packages...")
    result = checker.start()
    if result != 502:
        print(delimiter)
        print("==> All packages installed successfully")
