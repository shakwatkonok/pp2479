from socket import *
import os
import sys
import struct
import time
import select
import binascii
import statistics


ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fill in start
        # Fetch the ICMP header from the IP packet
        global rtt_min, rtt_max, rtt_sum, rtt_cnt, rtt_array

        type1, code, checksum1, id1, seq = struct.unpack('bbHHh', recPacket[20:28])
        if type1 != 0:
            return 'expected type=0, but got {}'.format(type)
        if code != 0:
            return 'expected code=0, but got {}'.format(code)
        if ID != id1:
            return 'expected id={}, but got {}'.format(ID, id)
        send_time, = struct.unpack('d', recPacket[28:])

        rtt = (timeReceived - send_time) * 1000
        rtt_cnt += 1
        rtt_sum += rtt
        rtt_min = min(rtt_min, rtt)
        rtt_max = max(rtt_max, rtt)
        rtt_array.append(rtt)
        print (rtt, rtt_cnt, rtt_sum, rtt_min, rtt_max,rtt_array)
        ip_header = struct.unpack('!BBHHHBBH4s4s', recPacket[:20])
        ttl = ip_header[5]
        saddr = destAddr
        length = len(recPacket) - 20
        return 'Reply from {}: bytes={} time={:.7f} ms ttl={}'.format(saddr,length, rtt, ttl)

        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)


    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")


    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    global rtt_min, rtt_max, rtt_sum, rtt_cnt, rtt_array
    rtt_min = float('+inf')
    rtt_max = float('-inf')
    rtt_sum = 0
    rtt_cnt = 0
    cnt = 0
    rtt_array =[]
    # timeout=1 means: If one second goes by without a reply from the server,  	# the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Calculate vars values and return them

    #vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]
    #vars = ['round-trip min/avg/max/stddev {:.2f}/{:.2f}/{:.2f}/{:.2f} ms'.format(rtt_min, rtt_sum / rtt_cnt, rtt_max,statistics.pstdev(rtt_array))]
    # Send ping requests to a server separated by approximately one second
    for i in range(0,4):
        cnt += 1
        delay = doOnePing(dest, timeout)
        #print(delay)
        time.sleep(1)  # one second
    if rtt_cnt != 0:
        loss = float(100-(100 * (rtt_cnt/cnt)))
        vars = [(cnt, 'packets transmitted,', rtt_cnt, 'packets received,', loss, '% packet loss'), ('round-trip min/avg/max/stddev = {:.2f}/{:.2f}/{:.2f}/{:.2f} ms'.format(rtt_min, rtt_sum / rtt_cnt, rtt_max,statistics.pstdev(rtt_array)))]
        print("")
        print('--- %s ping statistics ---'% host)
        #print("%d packets transmitted, %d packets received, %d % packet loss" %(cnt,rtt_cnt,loss))
        print(cnt,'packets transmitted,',rtt_cnt,'packets received,',loss,"% packet loss")
        #print('{} packets transmitted, {} packets received, {}% packet loss'.format(cnt,rtt_cnt,loss))

        print(rtt_array)
        print('round-trip min/avg/max/stddev = {:.2f}/{:.2f}/{:.2f}/{:.2f} ms'.format(rtt_min, rtt_sum / rtt_cnt, rtt_max,statistics.pstdev(rtt_array)))
        vars = [float(round(rtt_min, 2)), float(round((rtt_sum / rtt_cnt), 2)), float(round(rtt_max, 2)),
                float(round(statistics.pstdev(rtt_array), 2))]
        #print(vars)
        #vars = ['round-trip min/avg/max/stddev {:.2f}/{:.2f}/{:.2f}/{:.2f} ms'.format(rtt_min, rtt_sum / rtt_cnt, rtt_max,statistics.pstdev(rtt_array))]

    return vars


if __name__ == '__main__':
    ping("google.co.il")
   

