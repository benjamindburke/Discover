SQLite3 Installation instructions on Windows

Download the [sqlite3 precompiled binary for Windows](https://www.sqlite.org/2019/sqlite-tools-win32-x86-3270200.zip).  
Extract the files using 7zip or WinRar.  
You should see a sqlite3.exe file in the folder.  
Create a new folder C:\sqlite\ and move the sqlite3.exe file to this folder.  
Next you will need to edit your PATH variable.  
To do this, type `This PC` in the Windows search bar.  
Right-click on `This PC` and click Properties.  
Next click Advanced System Settings on the left menu.  
Click Environment variables. Double-click your `Path` variable.  
Next you should add the location `C:\sqlite` and confirm.  
Confirm you've installed it correctly by running `sqlite3 --version` in the command line.  

Installing Python3 Dependencies

Install all development dependencies with the command `python install.py`.