Create a new virtual environment and activate it

`python3 -m venv .venv`

`source .venv/bin/activate`

Install the requirements

`pip3 install -r requirements.txt`

(Quick reset pip packages if something doesn't work)

`pip3 freeze > un.txt`

`pip3 uninstall -r un.txt`


## TODO
Figure out dependencies:
- `mysql.connector`, `dnslib` in ThreadedDNSProxyv3.py

Authentication