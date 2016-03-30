# "Why IT Security" Demo for the Layman

The idea is to show a very simple demo, of why simple bugs or careless
programming can lead to security vulnerabilities. Hopefully this example is
something everybody can grasp.

## The App, The Bug, The Vuln

This simple flask web app mimics a banking web interface, where you can
transfer money to other users.

Unfortunately the programmer forgot to check whether the amount the user tries
to transfer is negative. So by sending negative amounts of money, the evil
person can enrich himself.

## Running

It's written in python using flask so I suggest you install everything in a
virtualenv:

    pip install flask flas-bootstrap
    python bank.py

There are a couple of users, such as `jdoe` and `mmustermann`, which you can
use. The login doesn't check the passwords, so it doesn't matter what you put
there.
