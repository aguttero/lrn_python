#HomeBrew
## install
https://brew.sh/
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

### install message
==> Next steps:
- Run these commands in your terminal to add Homebrew to your PATH:
    echo >> /Users/aleguttero/.zprofile
    echo 'eval "$(/usr/local/bin/brew shellenv zsh)"' >> /Users/aleguttero/.zprofile
    eval "$(/usr/local/bin/brew shellenv zsh)"
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh

## documentation
    https://docs.brew.sh

# python 3.13 install
brew install python@3.13

## install  notes in mac with python 3.14:
=> python@3.13
Python is installed as
  /usr/local/bin/python3.13

Unversioned and major-versioned symlinks `python`, `python3`, `python-config`, `python3-config`, `pip`, `pip3`, etc. pointing to
`python3.13`, `python3.13-config`, `pip3.13` etc., respectively, are installed into
  /usr/local/opt/python@3.13/libexec/bin

If you do not need a specific version of Python, and always want Homebrew's `python3` in your PATH:
  brew install python3

`idle3.13` requires tkinter, which is available separately:
  brew install python-tk@3.13

`dbm.gnu` is available separately:
  brew install python-gdbm@3.13

For more information about Homebrew and Python, see: https://docs.brew.sh/Homebrew-and-Python
