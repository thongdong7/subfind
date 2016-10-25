# Setup environment

```
virtualenv env
./env/bin/pip install -e .[cli,opensubtitles,subscene,web]
./env/bin/pip install -e ../tb-api
./env/bin/pip install -e ../tb-ioc
cd src/ui
yarn
bb8 up
```

# Release package to pypi

```
python setup.py bdist_wheel --universal upload
```

# Create tag

```
./tag.sg <tag_name>
```

# Run server

```
./env/bin/python subfind_web/main.py
```
