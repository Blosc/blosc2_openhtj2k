# Release notes

## Changes from 0.1.1 to 0.1.2

* Only remove AVX2 flag for Apple.

## Changes from 0.1.0 to 0.1.1

* Removed the AVX2 flag by default (Apple Rosetta cannot emulate AVX due to
  Intel patents).

## Version 0.1.0

This is a dynamic codec plugin for Blosc2 that allows to compress and decompress images
using the High Throughput JPEG 2000 standard. The HT version brings increased performance
when compared to the traditional JPEG 2000.  For details, check the
[HTJ2K whitepaper](https://ds.jpeg.org/whitepapers/jpeg-htj2k-whitepaper.pdf).

To provide this feature, this plugin uses the
[OpenHTJ2K](https://github.com/osamu620/OpenHTJ2K) library.

This is the first public release.