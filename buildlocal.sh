#!/bin/bash

set -e

TMPDIR=/tmp/buildlocal.$$
trap "rm -rf ${TMPDIR}" EXIT
mkdir -p ${TMPDIR}
spectool -gS -C ${TMPDIR} *.spec
rpkg srpm --outdir ${TMPDIR}
mock --rebuild ${TMPDIR}/*.src.rpm
