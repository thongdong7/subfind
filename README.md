# subfind

[![Build Status](https://travis-ci.org/thongdong7/subfind.svg?branch=master)](https://travis-ci.org/thongdong7/subfind)

Crawl subtitle base on file name in the movie folder.

Supported provider:

* Subscene
* Opensubtitles


# Install

    $ pip install subfind-cli

# Usage

    $ subfind scan -d <movie_folder> -l <languages>

Example:
    
    $ subfind scan -d /movie/folder -l vi,en

Detail:

```
$ subfind scan -h
```

```
Usage: cli.py scan [OPTIONS]

  Scan movie directory

Options:
  -d, --movie-dir TEXT      Movie directory  [required]
  -l, --lang TEXT           Languages. Multiple languages separated by comma
                            (,). E.g.: en,vi  [required]
  -p, --providers TEXT      Subtitle provider. Default: opensubtitles,subscene
  -f, --force               Force to override the existed subtitles
  -v, --verbose             Verbose
  --min-movie-size INTEGER  Min movie size. Default: 500MB
  --help                    Show this message and exit.
```