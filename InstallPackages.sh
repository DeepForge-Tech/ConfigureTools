#!/bin/bash
# Installing libraries
# Mac OSX
echo "==> Installing libraries"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install jsoncpp sqlite3 sqlite-utils fmt clang-format curl googletest gcc zlib cmake libzip openssl wget boost asio libssh2 unzip zip
wget https://github.com/madler/zlib/archive/refs/tags/v1.1.2.zip && unzip v1.1.2.zip && cd zlib-1.1.2 && sudo ./configure && sudo make && sudo make install
echo "==> Libraries successfully installed"