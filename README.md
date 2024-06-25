Fork of https://github.com/assquare/Custom-MEC meant for development of TSN-AF.

# Multi-access Edge Computing (MEC) API with Flask
This project gives a custom MEC implementation based on 3GPP specifications
It implements the Edge Configuration Server (ECS) as the registration entity of components such as Edge Application Server (EAS)
While relying on 3GPP and ETSI specifications, the MEC architecture is redefined to fit our needs for a custom MEC testbed.
![Edge-Architecture](https://github.com/assquare/Custom-MEC/assets/66039114/c84abc35-f7e6-422c-9a06-3de106da3bcf)

As the original MEC architecture is quite complexe, this project allows developers to have a starting point on edge developments.
More information about MEC can be found here: https://www.etsi.org/technologies/multi-access-edge-computing

3GPP Open API github reference: https://github.com/jdegre/5GC_APIs


## Installation
Create a new virtual environment and activate it

`python3 -m venv .venv`

`source .venv/bin/activate`

Install the requirements

`pip3 install -r requirements.txt`

(Quick reset pip packages if something doesn't work)

`pip3 freeze > un.txt`

`pip3 uninstall -r un.txt`

## TODO
- [ ] Figure out `mysql.connector`, `dnslib` dependencies in `ThreadedDNSProxyv3.py`
- [ ] Document/set up authentication
- [ ] Fix false red linter highlighting from MongoEngine-related dependencies in pylance