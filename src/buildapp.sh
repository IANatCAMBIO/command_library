#!/bin/bash

#remove old build files
rm -rf build dist 

#build the .app file
python3 setup.py py2app

#move it to the bin folder
rm -rf ../bin/Salt_Command_Library.app.old
mv ../bin/Command_Library.app ../bin/Command_Library.app.old
mv ./dist/Command_Library.app ../bin/Command_Library.app

#cleanup old build files
rm -rf build dist