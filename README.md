# vs-ninja
Drop-in ninja compatibility for Visual Studio C++ projects.

## Prerequisites
You must have an installation of Python 3 available as 'py'. If you have another installation of python that you want to use instead, modify the 'py' variable in configure.py to point to the installation you want.

## Usage
Your project must be a Makefile project.
Copy all files into the directory of the project (not the solution) you'd like to use ninja with then right click your project and select properties. Under **Configuration Properties > NMake**:

**Build Command Line**
```
cd $(ProjectDir)
ninja $(TargetPath)
```
**Rebuild All Command Line**
```
cd $(ProjectDir)
ninja -t clean
py configure.py
ninja $(TargetPath)
```
**Clean Command Line** to:
```
cd $(ProjectDir)
ninja -t clean
py configure.py
```

Under **Configuration Properties > VC++ Directories**:

**Include Directories**
```
$(SolutionDir)
```

Finally, run `py configure.py` once. Any later changes will cause it to rebuild itself.

## Notes
This repo contains an executable for ninja 1.7.2. To update it, download a new version from the [official ninja repository](https://github.com/ninja-build/ninja/releases).

File additions or deletions will require reconfiguring. Rebuild all, or clean then build.

To add flags, modify the compilation flags in configure.py.
