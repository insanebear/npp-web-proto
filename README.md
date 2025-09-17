# Setting up the project
## Install Git
Install [git](https://git-scm.com/downloads) from the official website and set it up using the wizard.

 Alternatively, if you are on Linux or Mac, run

 ``/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" ``

in your terminal. This will install Homebrew. Close the terminal and open it again.

After that, type ``brew install git
`` in the terminal again.

## Download the source code
1. Open a text editor (e.g VS Code) and go to the terminal using `` Ctrl + ` `` on Windows, or `` command + ~ `` on Mac.
2. Navigate the current directory to your desired directory using `` cd `` command in terminal. Desired directory is where you want the project files to be located. 
3. Type ``git clone https://github.com/insanebear/npp-web-proto.git `` and download the source code.



## Installing miniconda

Conda is a modern package manager. You can install its simpler version [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) from the official website.

Run the wizard and use the default settings. Next, close and re open your terminal.

To check if installation is succesfull, run ``conda --version`` in the terminal.

 On Mac, this should be it. If you are using Windows, conda may not be activated directly, but you should allow for conda to change environment variables in the powersehll.

### Note: 
I forgot the exact solution for Windows, but searching how to set conda in the terminal for windows should solve it.

## Setting an environment
In your text editor's terminal while inside the project folder type
`` conda create --name myenv `` 
Here you can change the term ``myenv`` to any other word. This will be the name of the environment.

To activate environment just run ``conda activate myenv`` and replace ``myenv`` with the name you chose if you chose a different environment name.

Next, install the required files using ``pip install -r requirements.txt``. Here, it is assumed you have installed ``pip`` using ``conda install pip
``.


## Node.JS installation

Assuming you have activated the environment :
1. Install [Node.JS](https://nodejs.org/en) from the official website and run the wizard. You can choose default settings.
2. Open the source code in a text editor (e.g VS Code) and navigate to the project directory if you are not already there. Run ``npm install`` in the terminal.

## Docker Installation
Install [Docker](https://www.docker.com/) from the official source based on your device architecture. You may need to restart your machine. 

### Note:
Depending on computer, Docker may not be available even after installation because of various reasons such as outdated windows edition, or certain permissions such as  virtualization are disabled. For these, you should look for tutorials on them. Usually, Mac doesn't have such issues after installation. 

# How to see the UI
Open your project folder  using a text editor such as VS Code. Next, open the terminal. Then, run ``npm run dev`` which will initialize a webpage at the ``localhost`` with a certain port number. You can hover on the link to go to the website or type the link in the browser.

