#! /usr/bin/env python3
#! -*- coding: utf-8 -*-

from wsgiref import simple_server

def application (environment, start_response):
	status = "200 OK"
	headers = [("Content-type", "text/plain; charset=utf-8")]
	body = "Hello, World!".encode("utf-8")
	start_response(status, headers)
	return [body]

def main ():
	host = ""
	port = 8001
	server = simple_server.make_server(host, port, application)
	server.serve_forever()

if __name__ == "__main__":
	main()
