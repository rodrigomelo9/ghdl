#! /bin/sh

. ../../testenv.sh

UNIT=assert0
GHDL_STD_FLAGS=--std=08

synth_only $UNIT

# There should be no assume gate without assert-assume option.
if grep -q -e "--  assume" syn_$UNIT.vhdl; then
  exit 1
fi

# There should be an assert gate without assert-assume option.
if ! grep -q -e "--  assert" syn_$UNIT.vhdl; then
  exit 1
fi

GHDL_FLAGS=--assert-assumes

synth_only $UNIT

# There should be an assume gate with assert-assume option.
if ! grep -q -e "--  assume" syn_$UNIT.vhdl; then
  exit 1
fi

# There should be no assert gate with assert-assume option.
if grep -q -e "--  assert" syn_$UNIT.vhdl; then
  exit 1
fi

clean

echo "Test successful"
