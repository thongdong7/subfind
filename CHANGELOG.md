# Change log

## 4.5.4

1. Fix error when uninstall Ubuntu package

## 4.5.3

1. Fix bugs
2. Refactor UI
3. Auto run after install and boot thanks to service (only support Ubuntu 15.04 and later)

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
