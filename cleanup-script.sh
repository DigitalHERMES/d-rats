#!/bin/bash

# remove the executable for lzhuf. Although source
# is available, it only builds in an arcane environment,
# and the license and authorship is unclear.

git rm -f libexec/lzhuf
rm -f libexec/lzhuf

