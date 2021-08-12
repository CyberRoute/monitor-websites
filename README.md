[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CircleCI](https://circleci.com/gh/CyberRoute/monitor-websites.svg?style=svg)](https://circleci.com/gh/CyberRoute/monitor-websites)

# A Flask App that monitors websites

The monitors website availability over the network, produces metrics about this and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.

Project structure
--------
```sh
├── README.md
├── main.py
├── requirements.txt
├── tox.ini
├── .circleci
│      └── config.yml
├── config
│   ├── config.py
│   └── urls.json
├── src
│   ├── kafka.py
│   ├── monitor.py
│   └── postgres.py
├── templates
│    ├── index.html
│    ├── layout.html
│    └── update.html
├── tests
│    └── test_monitor.py
```

### Screenshot
![Site](https://github.com/CyberRoute/monitor-websites/blob/main/screenshot/site.png)

### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/CyberRoute/monitor.git
  $ cd monitor
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Configure Kafka Broken and Postgres Database in config.py
```
class Config:
    DEBUG = False
    TESTING = False
    PROCS = 8
    DOWN = 'UNREACHABLE'
    REFRESH = 60
    URLS = 'config/urls.json'
    SERVER_KAFKA = "kafka-broker:18158",
    ssl_cafile = "creds/ca.pem",
    ssl_certfile = "creds/service.cert",
    ssl_keyfile = "creds/service.key",
    #POSTGRES CONF
    DB_PASSWORD = "password"
    DB = "defaultdb"
    DBHOST = "pg-host"
    DBUSER = "user"
    DBTABLE = "monstats"
    
    The table that needs to be created in PostGres  
  
    "CREATE TABLE monstats  (id SERIAL 
    PRIMARY KEY, site_url VARCHAR NOT NULL, 
    http_status VARCHAR, response_time_ms VARCHAR, time TIMESTAMP);

```

5. Run the development server:
  ```
  $ python main.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

