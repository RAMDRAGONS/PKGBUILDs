#!/bin/sh
export ELECTRON_FORCE_IS_PACKAGED=1
exec /opt/msbt-editor/msbteditor-app "$@"
