import dns.query
import dns.message
import json
import logging
# import mariadb
import mysql.connector as mariadb
import socket
import sys
import threading
import time
from dnslib import DNSRecord, RR, QTYPE

class DNSProxyServer:

    def __init__(self, dns_server, cache_time=60, max_requests_per_minute=100):
        self.dns_server = dns_server
        self.cache_time = cache_time
        self.max_requests_per_minute = max_requests_per_minute
        self.cache = {}
        self.request_counter = {}
        self.lock = threading.Lock()
        self.credentials = None

        with open('source.json') as f:
            self.credentials = json.load(f)
        
        try:
            self.conn = mariadb.connect(host=self.credentials.get('host'),
                                        user=self.credentials.get('user'),
                                        password=self.credentials.get('password'),
                                        database=self.credentials.get('database'))
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)

        self.cursor = self.conn.cursor()    

    def handle_request(self, request, client_address, sock):
        """Validate the request to ensure it is a valid DNS request

        Args:
            request (object): DNS query
            client_address (tuple): client's address and port number
        """
        try:
            logging.info(f"Received request from {client_address[0]}:{client_address[1]}")
            request = DNSRecord.parse(request)
        except Exception as err:
            print("Invalid request received:", err)
            return

        # Check rate limiting of requests sent by client
        now = int(time.time())

        if client_address[0] in self.request_counter:
            if self.request_counter[client_address[0]] > self.max_requests_per_minute:
                print("Too many requests from", client_address[0])
                time.sleep(1000)
            else:
                self.request_counter[client_address[0]] += 1
        else:
            self.request_counter[client_address[0]] = 1

        # Check cache
        query = request.q.qname
        qtype = request.q.qtype
        fqdn = str(query).strip(".")
        _id = request.header.id
        print(fqdn)
        record = self.check_cache(fqdn)

        
        if record:
            print("Using cached response for", query)
            question = DNSRecord.question(fqdn)
            question.header.id = _id
            
            zone = f"{record[0]} {record[2]} IN {record[1]} {record[3]}"

            response = question.replyZone(zone)
            response = response.pack()
            self.send_response(response, client_address, sock)
        else:
            # Forward request to real DNS server
            response = self.forward_request(fqdn, qtype, _id)
            self.send_response(response, client_address, sock)

            # Update cache
            # improve to call update_cache(query)
            self.cache[query] = (response, now)

    # Function to check if a hostname is already in cache database
    def check_cache(self, hostname):
        query = "SELECT * FROM records WHERE domain = %s"
        try:
            self.lock.acquire()
            self.cursor.execute(query, (hostname,))
        except Exception:
            print("SELECT statement went wrong.")
        result = self.cursor.fetchone()
        self.lock.release()
        if result:
            return result
        else:
            return None

    # Function to update the cache with a new hostname and its IP address
    def update_cache(self, hostname, qtype, ttl, ip_address):
        query = "INSERT INTO dns_records (domain, rr_type, rr_ttl, address) VALUES (%s, %s, %s, %s)"
        self.lock.acquire()
        self.cursor.execute(query, (hostname, qtype, ttl, ip_address))
        self.conn.commit()
        self.lock.release()
        
    def forward_request(self, qname, qtype, _id):
        # Forward the request to the real DNS server
        query = dns.message.make_query(qname=qname, rdtype=QTYPE[qtype], id=_id)
        response = dns.query.udp(query, self.dns_server)
        response = response.to_wire()
        logging.info(f"Forwarding request to {self.dns_server}")
        # To send bytes through the socket    
        return response

    def send_response(self, response, client_address, sock):
        # Send the response back to the client
        sock.sendto(response, client_address)
        logging.info(f"Sent response to {client_address[0]}:{client_address[1]}")
    

    def run(self, host='172.16.210.252', port=53):
        # Start the proxy server
        logging.basicConfig(filename='dns_proxy.log', level=logging.INFO)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        print("DNS proxy server running on", host, port)
        logging.info(f"DNS proxy server started on {host}:{port}")
        try:
            while True:
                request, client_address = sock.recvfrom(4096)
                # Start a new thread to handle the request
                thread = threading.Thread(target=self.handle_request, args=(request, client_address, sock))
                thread.start()
        except KeyboardInterrupt:
            self.conn.close()
            logging.info(f"DNS proxy server shut down {host}:{port}")
            print("Interrupted from command line, database connection closed.")
        
        
        
          
if __name__ == '__main__':
    dns_proxy = DNSProxyServer(dns_server='8.8.8.8')
    dns_proxy.run()
