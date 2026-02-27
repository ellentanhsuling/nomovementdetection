# Fix libcamera Command Not Found

## Problem
Package says it's installed, but command not found.

## Solution 1: Find Where It's Installed

```bash
which libcamera-hello
```

OR

```bash
dpkg -L libcamera-apps | grep libcamera-hello
```

## Solution 2: Install Full Package

The package might be installed but missing the binaries. Try:

```bash
sudo apt install --reinstall libcamera-apps
```

## Solution 3: Check Package Contents

```bash
dpkg -L libcamera-apps
```

This shows all files in the package.

## Solution 4: Use Alternative Command

Some Pi OS versions use different commands:

```bash
libcamera-jpeg --list-cameras
```

OR

```bash
rpicam-hello --list-cameras
```

## Solution 5: Check What's Actually Available

```bash
ls /usr/bin/libcamera*
ls /usr/bin/rpicam*
```

See what camera commands are actually available.
