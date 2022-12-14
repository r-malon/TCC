#!/bin/sh -e

main() {
	checkdep "python3"
	checkdep "magick"

	magick montage -mode Concatenate -tile 1x -density 150 -type Grayscale\
	 -define png:compression-level=9 -define png:format=8\
	 -define png:color-type=0 -define png:bit-depth=8\
	 ./out/out.pdf ./out/out.png
}

checkdep() {
	command -v "$1" > /dev/null 2>&1 || err 1 "dependency $1 not found"
}

main "$@"
