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

## 4.5.0

1. [Web] Support `edit max-sub` and `min-movie-size`
2. [Web] Redirect to config page when missed config file
3. [Web] Improve performance when has a lot of movies

## 4.4.0

1. Change to use `beautifulsoup` instead of `lxml`

## 4.3.0

1. [Web]: Refactor web package
2. [Web]: Correct restUrl
3. [Web]: Fix list languages and filter in release api
4. [Web] Clean up layout, update icons, optimize css and js
5. [Web]: Add config button in release page
6. [Web]: Show toastr message when connection error

## 4.2.0

1. Refactor cli, core package
2. [Web]: Add option `force` and `remove` to config form
3. Update unit tests

## 4.1.2

1. [Bug]: Fix download non-related release when click download button
2. [Feature]: Remove subtitle for specific release

## 4.1.1

1. Movie matching bug: the matched title is more important than the matched year
2. Remove `:` character when build title query

## 4.1.0

1. Movie matching: only return movies which year distance <= 1
