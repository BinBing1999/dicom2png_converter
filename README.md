# dicom2png_converter
This is a small software that can change a folder of dicom files to pngs, each png is a layer in one dicom file, you can find in which dicom file this png belongs to base on its generated name.

Use pyhon3.9's pip to install pyinstaller, then use command: "pyinstaller -F dicom2png.py" to generate dicom2png.exe, you can find the exe file in 'dist' folder.
The exe file is about 60MB size , so i cannot just upload it on this platform.

Sofeware Usage:

On the UI, choose an input path, which is a folder that only contains dicom files, then press ok. Then, choose a output path, which is a clean folder with nothing inside.
#choose grey or RGB channel base on your need
#choose 1 dimension mode to get the front dicom file vision

