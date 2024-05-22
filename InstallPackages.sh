#!/bin/bash
# Installing libraries
# Mac OSX
echo "==> Installing libraries"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install jsoncpp sqlite3 sqlite-utils fmt clang-format curl googletest gcc zlib cmake libzip openssl wget boost asio
echo "==> Libraries successfully installed"