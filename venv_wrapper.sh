#!/bin/bash    

cd "$(dirname "$0")"
source venv/bin/activate

export PROJECT_ID=`cat PROJECT_ID`

"$@"

