# Setup environment

```
virtualenv env; and ./env/bin/pip install -e .[cli,opensubtitles,subscene,web]
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
