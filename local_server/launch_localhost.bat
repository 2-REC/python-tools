@echo off
call ".\python_http_server\Scripts\activate"
python server_brotli.py --cert cert.pem --key key.pem --dir D:\webserver\root --local
pause
