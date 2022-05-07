#!/bin/env python3

find . -iname "*.png" -exec mogrify -crop '600x400+100+150' {} \;
