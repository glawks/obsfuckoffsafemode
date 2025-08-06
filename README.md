
# OBSFuckOFFSafeMode

Yeah I could run it OBS with the --disable-shutdown-check startup parameter but it never shuts down cleanly. So I just made a small program that deletes the safemode file before launch. Launches the program, watches to see if it's running and then clears the safemode file again if OBS didn't clean exit. Also has a force close button because I'm sick of opening taskmanager when it hangs.



## Getting Started

You'll need pyinstaller or something similar to compile.
Download the .py file.
Grab an icon file if you like for the program,
and run 

"pyinstaller obsfuckoffsafemode.py --noconsole --onefile --icon=your_icon.ico"


### Prerequisites


- [pyinstaller](https://pyinstaller.org/en/stable/)



## License

This project is licensed under the [GPL-3.0 license](LICENSE.md)
see [LICENSE.md](LICENSE.md) file for
details
