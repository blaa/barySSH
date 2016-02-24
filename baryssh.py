#!/usr/bin/env python
# coding: utf-8

"""
Proxy which uses simple time-based XOR scheme to make heuristic detection
of underlying transmission impossible.

Based on twisted example 'tcp proxy' with an original link:
http://musta.sh/2012-03-04/twisted-tcp-proxy.html

MIT license
"""

import sys

from twisted.internet import defer
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.python import log

from optparse import OptionParser

from time import time
import random
from hashlib import sha256

cfg = {
    'server_addr': None,
    'server_port': None,
    'listen_port': None,
    'base_key': None,
}

class Mixer(object):
    """Mix input string so that it can be unmixed but looks random.

    Don't be mistaken. This is not the true cryptography. It is not intended
    to be the true cryptography and it really doesn't need to be (as you're
    masking a secure protocol anyhow, aren't you?)
    """

    WINDOW = 5 * 60
    KEY_SIZE_MB = 5

    def __init__(self, base_key):
        self._generate_key(base_key)

    @staticmethod
    def prepare_base_key(base_key):
        "Just slow-down bruteforce attacks"
        s = time()
        # This takes around 0.5s on my i7 machine.
        for i in range(512*1024):
            base_key = sha256('\xF0' + str(i) + base_key + '\x0F').digest()

        log.msg("Prepared base_key in", time() - s, "[s]")
        return base_key

    def _generate_key(self, base_key):
        "Generate a mixing key from current time and base key"

        time_part = int(time() / (self.WINDOW))
        temp_key = 'S{0}{1}{0}E'.format(time_part, base_key)

        self.key = ""

        length = self.KEY_SIZE_MB * (1024*1024) + (time_part % 3000)

        self.key = "".join(sha256(str(i) + temp_key + str(i)).digest()
                           for i in range(0, length / 32))
        self.key = [ord(c) for c in self.key]
        self.key_length = len(self.key)
        self.pos = time_part % self.key_length

    def mix(self, s):
        k = self.key
        l = self.key_length
        result = []
        for ch in s:
            result.append(chr(ord(ch) ^ k[self.pos % l]))
            self.pos += 1
        return "".join(result)


class ProxyClientProtocol(protocol.Protocol):
    """Handles connection with client.

    Data incoming from the server object is read from the queue
    and sent to the client. Data read from the client is written
    into the server pipe.
    """

    def connectionMade(self):
        log.msg("Client: connected to peer")
        self.mixer = Mixer(cfg['base_key'] + '_cli')
        self.cli_queue = self.factory.cli_queue
        self.cli_queue.get().addCallback(self.serverDataReceived)

    def serverDataReceived(self, chunk):
        if chunk is False:
            self.cli_queue = None
            log.msg("Client: disconnecting from peer")
            self.factory.continueTrying = False
            self.transport.loseConnection()
        elif self.cli_queue:
            chunk = self.mixer.mix(chunk)
            self.transport.write(chunk)
            self.cli_queue.get().addCallback(self.serverDataReceived)
        else:
            self.factory.cli_queue.put(chunk)

    def dataReceived(self, chunk):
        self.factory.srv_queue.put(chunk)

    def connectionLost(self, why):
        if self.cli_queue:
            self.cli_queue = None
            log.msg("Client: peer disconnected unexpectedly")


class ProxyClientFactory(protocol.ReconnectingClientFactory):
    maxDelay = 10
    continueTrying = True
    protocol = ProxyClientProtocol

    def __init__(self, srv_queue, cli_queue):
        self.srv_queue = srv_queue
        self.cli_queue = cli_queue


class ProxyServer(protocol.Protocol):
    """On each new connection to the server spawn new client connection
    and a new mixer.
    """

    def connectionMade(self):
        self.srv_queue = defer.DeferredQueue()
        self.cli_queue = defer.DeferredQueue()
        self.srv_queue.get().addCallback(self.clientDataReceived)
        self.mixer = Mixer(cfg['base_key'])

        factory = ProxyClientFactory(self.srv_queue, self.cli_queue)
        reactor.connectTCP(cfg['server_addr'], cfg['server_port'], factory)

    def clientDataReceived(self, chunk):
        chunk = self.mixer.mix(chunk)
        self.transport.write(chunk)
        self.srv_queue.get().addCallback(self.clientDataReceived)

    def dataReceived(self, chunk):
        self.cli_queue.put(chunk)

    def connectionLost(self, why):
        self.cli_queue.put(False)


def main():

    # Parse options
    parser = OptionParser()

    parser.add_option("-c", "--connect-ip", action="store", help="Connect to this specific ip address")
    parser.add_option("-p", "--connect-port", action="store", type=int, help="Connect to this specific port")
    parser.add_option("-l", "--listen-port", action="store", type=int, help="Listen on this port")
    parser.add_option("-k", "--base-key", action="store", help="Base key for masking",
                      default='You should set up your own key, although this one is usually fine.')

    options, args = parser.parse_args()

    log.startLogging(sys.stdout)

    cfg['server_addr'] = options.connect_ip
    cfg['server_port'] = options.connect_port
    cfg['listen_port'] = options.listen_port
    cfg['base_key'] = Mixer.prepare_base_key(options.base_key)

    # Start proxy
    factory = protocol.Factory()
    factory.protocol = ProxyServer
    reactor.listenTCP(cfg['listen_port'], factory, interface="0.0.0.0")
    reactor.run()


if __name__ == "__main__":
    main()
