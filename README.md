# subfind

[![PyPI version](https://badge.fury.io/py/subfind.svg)](https://badge.fury.io/py/subfind)
[![Build Status](https://travis-ci.org/thongdong7/subfind.svg?branch=master)](https://travis-ci.org/thongdong7/subfind)

Crawl subtitle base on file name in the movie folder. Support both movie and TV shows.

Supported providers:

* Subscene
* Opensubtitles

# Getting started

## Install

Subfind is developed by Python and packaged using pip. Ensure you have pip installed.

```
pip install subfind[cli,opensubtitles,subscene]
```

## Scan movie folder 

```
subfind scan -d <movie_folder> -l <language>
```

Example: The below command will scan subtitle for language Vietnamese and English, at folder `/movie/folder`
    
````
subfind scan -d /movie/folder -l vi -l en
```

For more detail

```
subfind scan -h
```

```
Usage: subfind scan [OPTIONS]

  Scan movie directories

Options:
  -d, --movie-dir TEXT      Movie directories (support multiple)
  -l, --lang TEXT           Language (support multiple). E.g.: -l en -l vi
  -p, --providers TEXT      Subtitle provider. E.g: -p opensubtitles -p
                            subscene. Default is opensubtitles and subscene.
  -f, --force               Force to override the existed subtitles
  -r, --remove              Remove olf subtitle if not found. Only affect when
                            --force is enabled
  -v, --verbose             Verbose
  --min-movie-size INTEGER  Min movie size. Default: 500MB
  -h, --help                Show this message and exit.

```

## Scan movie folder by config file

Another way to avoid typing a long `scan` command is putting all parameters into a config file named `subfind.yml` and using the following command:

```
subfind scan-config -c /path/to/you/subfind.yml
```

In case there is a `subfind.yml` in your current working directory or at `$HOME/.subfind/subfind.yml`, you just need to use:

```
subfind scan-config
```

Example `subfind.yml`:

```yaml
src: [/my/movie/folder, /my/tv-shows/folder]
lang: [vi,en]
# Force to override the existed subtitle. Default is false
#force: false
# Remove old subtitle if not found. Only work when `force` is enabled.
#remove: false
#providers: [opensubtitles, subscene]
```

# Change log

## 4.1.0

1. Movie matching: only return movies which year distance <= 1

# Development

```
python setup.py bdist_wheel --universal upload
```
