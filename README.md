
# OBSFuckOFFSafeMode

Yeah I could run it OBS with the --disable-shutdown-check startup parameter but it never shuts down cleanly. So I just made a small program that deletes the safemode file before launch. Launches the program, watches to see if it's running and then clears the safemode file again if OBS didn't clean exit. Also has a force close button because I'm sick of opening taskmanager when it hangs.



## Getting Started

You’ll need Nuitka to compile the program.

Download the .py file.

Grab an icon file if you like for the program.

Run the following command to build a standalone Windows executable:
nuitka obsfuckoffsafemode.py --standalone --enable-plugin=tk-inter --windows-console-mode=disable --windows-icon-from-ico=your_icon.ico


### Prerequisites


-Nuitka
-Python 3.x



## License

This project is licensed under the [GPL-3.0 license](LICENSE.md)
see [LICENSE.md](LICENSE.md) file for
details
