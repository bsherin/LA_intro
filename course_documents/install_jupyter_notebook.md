# Installing Jupyter Lab

This can be an iffy process, but you should only have to do it once.

These directions are to, a certain extent, mac specific. I'll try to point out
Windows differences as best as I can.

### 1. Copy stuff from this github repository

A first step is to copy the material from this repository to your own computer.
I recommend that you do this in your home directory. Open up the Terminal
application then type the following. ("cd" means "change directory")

```
cd ~
git clone https://github.com/bsherin/LSA_intro.git
```

When you're done, you should have a new folder named `LSA_intro`.

### 2. Create your python virtual environment

Open the Terminal application and `cd` into the `LSA_intro` folder you just created

```
cd ~/LSA_intro
```
Then, on a mac, use these commands to create the virtual environment.

```
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:
```
python3 -m venv venv
# just one of the next two lines
venv\Scripts\activate.bat # if you're using cmd.exe
venv\Scripts\Activate.ps1 # if you're using PowerShell
# then this
pip install -r requirements.txt
```

# Launch the jupyter notebook or jupyter lab

Go back into your terminal. First `cd` into the text_mining_2021 folder

```
cd ~/LSA_intro
```

Then activate the python virtual environment you created above

```
source venv/bin/activate  # or the Windows version from above
```

Finally, start the jupyter lab or jupyter notebook

```
jupyter lab
```
```
jupyter notebook
```

A browser window should magically open with the jupyter lab or notebook.
You need to keep the terminal window open. If it doesn't, you can enter `http://localhost:8888/lab` in your browser for jupyter lab or `http://localhost:8888/tree` for the jupyter notebook.
