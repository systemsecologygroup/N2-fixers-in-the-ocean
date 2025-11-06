# Instructions for setting up the virtual python environment

## Starting from scarctch
First we create the environment and then we switch the terminal to open it. 
```
python -m venv .venv
source .venv/bin/active
```

Now you should see somethign like: 
```
(.venv) bash-5.3$ 
```
We are inside the virtual environment.

Then we need to install all libraries. This can technically be also done outside of the environment, but more chances of encountering compatibility issues.
```
pip install -r libraries.txt
```

## Entering existing virtual environment
In the jupyter notebook it should appear as one of the options for the kernel to use. And I made the environment visible at the beginning of every file. So, it should be clear if somethign is wrong.

In order to enter in terminal(if not already entered)

```
source .venv/bin/active
```

