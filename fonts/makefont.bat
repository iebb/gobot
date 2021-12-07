@echo off
echo "1"
otf2bdf -p 10 -r 64 -o lcdsolid.bdf lcdsolid.ttf
python pil.py lcdsolid.bdf
