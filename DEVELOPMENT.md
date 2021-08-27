# Development
Requirements for development are
```
altgraph==0.17
colorama==0.4.4
cycler==0.10.0
future==0.18.2
kiwisolver==1.3.1
matplotlib==3.4.3
numpy==1.21.2
pefile==2021.5.24
Pillow==8.3.1
pyinstaller==4.5.1
pyinstaller-hooks-contrib==2021.3
pyparsing==2.4.7
python-dateutil==2.8.2
pywin32-ctypes==0.2.0
scipy==1.7.1
six==1.16.0
sly==0.4
termcolor==1.1.0
```

All of them can be installed by running:
`pip3 install -r requirements.txt`

# Building

`PyInstaller` is used to create a distributable version of the utility. It will automatically create an executable and standalone version of it under the `dist` directory. All this can be done by running

```
PyInstaller -F gecko.py
```
If the above command does not work, you can run
```
python3 -m PyInstaller gecko.py
```
