# Computer-Aided-Quality-Data-Handling

## User Guide
### Directory Configuration
To configure directory paths for the application, use the pathsConfig.json file.
Make sure this file stays within the same directory as CAQDH.exe.
#### Paths
pathsConfig.json is in the format of a list containing sets of input, output, archive paths.  Each set is separated by a comma and in this format:
> {\
> &nbsp;&nbsp;&nbsp;&nbsp;"input_paths": [\
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"..\\\\PathToInputDirectory",\
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"..\\\\PathToInputDirectory2"\
> &nbsp;&nbsp;&nbsp;&nbsp;],\
> &nbsp;&nbsp;&nbsp;&nbsp;"output_path" : "..\\PathToOutputDirectory",\
> &nbsp;&nbsp;&nbsp;&nbsp;"archive_path": "..\\PathToArchiveDirectory"\
> }
##### Input Paths
The input_paths characteristic is a comma-separated list of directory paths for the program to watch and pull files for conversion.
##### Output Paths
The output_path characteristic is the path to the directory where the program will output the converted files.
##### Archive Path
The archive_path characteristic is the path to the directory where the program will move the original unconverted file.

## General Information
### External Packages Used
* watchdog
* pandas
* xmltodict
### Scripts Guide
If using the uncompiled code, the main file to run is CAQDH.py and must be run from inside the directory.  This directory must also contain all other script files along with pathsConfig.json
CAQDH.exe is compiled using pyinstaller with the single-file command.
> pyinstaller CAQDH.py -F

### Authors
Reid Foster\
Spencer Bonvillain\
Jared Siecinski\
Kyra Govan
