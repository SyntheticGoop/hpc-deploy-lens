ROOT=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

export LENSDIR="$ROOT"

LENSBIN="$LENSDIR/Bin"

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$LENSBIN"
export PATH="$PATH:$LENSBIN"

lens -b $@
