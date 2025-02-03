# Simply-Present

> Application to update your discord status to whoever is fronting using data from Simply Plural

- [Simply-Present](#Simply-Present)
  - [System requirements](#system-requirements)
  - [Getting Started](#getting-started)
  - [License](#license)


## System requirements

- Python 3.8 or higher is required to run Simply-Present (tested with 3.12). You can check your Python version by running `python --version` in your terminal. You can install it using your package manager or from the [Python website](https://www.python.org/downloads/). 
- Both Windows 10 and Linux (Arch, Fedora) have been tested to work with Simply-Present.
  - MacOS should work as well but has not been tested. 

## Getting started

Clone the repository and navigate to the project directory.
```
git clone https://github.com/CrimsonTome/simply-present
cd simply-present
```
Virtual environments are recommended to keep dependencies isolated from other projects and in some cases to keep them from breaking your system system packages. You can create a virtual environment and install the dependencies with the following commands:

with bash
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Or if you're on windows and using powershell
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Once you have the dependencies installed and/or have made your changes you can run the application with `python src/main.py`

It is recommended to run your changes through a linter such as pylint. Code in this repository is linted with pylint (from the Official python extension) and formatted with Black. You can run it with `black src/` to format your code.

## Known issues and limitations

- If the first fronter in the list does not have an avatar the application will use an empty avatar. 

## License

Simply-Present is licensed under the MIT license. The full license text is included in the [LICENSE](LICENSE) file in this repository. Tldr legal have a [great summary](https://www.tldrlegal.com/license/mit-license) of the license if you're interested.
