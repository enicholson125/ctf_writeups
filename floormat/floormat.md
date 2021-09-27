# Floormat

This was in the misc section and the initial instruction was `nc pwn-2021.duc.tf 31903`. A python file was also provided: [floormat.py](./floormat.py).

Connecting to the endpoint revealed a server running the floormat.py script, that would like to build pictures of floormats for me. It had a number of pre-set options for floormat templates. However, looking at the script's code revealed a custom template option, which was reachable if you requested a template which wasn't in the pre-sets.

From looking at the code, I also noticed that the flag was stored as a global variable - obviously set to REDACTED in the downloadable version.

The floormat templates were then populated with patterns, using .format(). It wasn't possible to specify a custom pattern (I was really hoping I could just ask for the string `FLAG`!), but strings are objects in python, and so have an `__init__` function, from which you can get the globals in the environment.

Using this, I created a custom template of
```
{f.__init__.__globals__[FLAG]}
```
which, when run through `template.format(f)` produced me the flag.
