For the security reason moved to the Praca/lhcom4.

## Setup for developer

### For Macos

#### Install MacOS packages
```bash
brew install mariadb

brew install openssl
export LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include"

pip install -r requirements.txt
```

#### Prepare config file
`cp config_sample.py config.py`

#### Run in Pycharm
Right click on microblog.py and choose Run 'Flask' microblog.py

Not the home page should start. 

#### Setup database
Run postgres docker container `postgres-docker.sh`
```bash
createuser -h localhost -U postgres lhcom4
createdb -h localhost -U postgres -O lhcom4 lhcom4
psql -h localhost  -U postgres template1
template1=# alter user lhcom4 password 'pass';
psql -h localhost -U lhcom4 lhcom4 < lhcom4-2022-05-15.db
```
Change the config.py:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://lhcom4:pass@localhost/lhcom4'                              'sqlite:///' + os.path.join(basedir, 'app.db')
```

