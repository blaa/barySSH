barySSH
=======

TCP proxy which masks (any) underlying protocols from trivial methods
of detection. Masking is time-based (both sides need to have a
synchronized clock, key changes by default every 5 minutes) and it's not 
trivial to unmask given secure key on both ends. But IT'S NOT A SECURE
ENCRYPTION and is NOT MEANT to be an encryption algorithm at all.

It can be used to mask SSH connections. It's compatible with the way
sslh demultiplexes SSH.

The name `BarySSH' is just an inside joke, ignore it. Call it
"proxor" if you don't like original name.

Use 'baryssh -t' to run internal test and measure throughput.

Usage
=====
To install from pip use: 
pip install barySSH

Run it on two computers to create a *masked* channel. 
For example, to connect to an ssh service on "server.com" 
using tcp tunnel on port 20023:

Run on client:
baryssh -k 'shared passphrase' -l 20023 -c server.com -p 20023

Run on server.com:
baryssh -k 'shared passphrase' -l 20023 -c 127.0.0.1 -p 22

Then connect to the tunnel entry point with ssh:
ssh -p 20023 localhost

```
  ssh client -> :20023 entrypoint -- masked channel --> server.com:20023 endpoint --> localhost:22 ssh server
```
