barySSH
=======

TCP proxy which masks (any) underlying protocols from trivial methods
of detection. Masking is time-based (both sides need to have a
synchronized clock) and it's not trivial to unmask given secure key on
both ends. But IT'S NOT A SECURE ENCRYPTION and is NOT MEANT to be an
encryption algorithm at all.

It can be used to mask SSH connections. It's compatible with the way
sslh demultiplexes SSH.

The name `BarySSH' is just an inside joke, ignore it. Call it
"proxor" if you don't like original name.

