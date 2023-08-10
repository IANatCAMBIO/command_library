## README for Command Library

# Requirements:
Command Library was written in Python 3.9, and the GUI uses TKinter.  
To run properly, you must have both of these installed on your system.

# Prereqs:
- Python 3.6 or greater 
- tkinter

If you install python from the python.org package, tkinter comes included

On MacOS, you can use homebrew for both requirements:  
*brew install Python*  
*brew install tcl-tk*  

[Note: if you run into tcl errors such as `ModuleNotFoundError: No module named '_tkinter'` try `brew install python-tk`]

# Quickstart:

1. Clone this git repo, and run command_library_.py
2. Load some sample dictionaries
  Click the 'Dictionary' menu item and select 'Import Dictionary Folder'. In the open dialog, select the directory called 'Dictionary' from the local Git repo. This will load all .dct files in the directory.
3. Select a Dictionary from the dropdown menu.
4. Click a snippet in the list on the left.
5. Information for the selected snippet is displayed on the right.
6. Double-click the snippet to copy the snippet text to your clipboard.

# Dictionary (.dct) files
Dictionary files are standard JSON format text files with the following structure:
```
{
    "snippets": [
        {
            "title": "Get pods",
            "code": "kubectl get pods",
            "info": "This will get all pods in the local namespace"
        },
        {
            "title": "Get nodes",
            "code": "kubectl get nodes",
            "info": "This will get all nodes in the local namespace"
        },
        {
            "title": "Get node info",
            "code": "kubectl describe nodes",
            "info": "This will describe all the nodes in the cluster"
        }
    ]
}
```
# DB
Command Library uses a database file (.lib) to store your currently loaded dictionaries. Each DB file contains one or more Dictionaries, and the dictionary files (.dct) contain one or more Snippets.
  
Snippets are discrete objects consisting of:  
Title : The test displayed for the snippet in the Snippets list  
Code : This is the actual text that will be copied to the clipboard  
Info : A short description of the snippet usage (displayed in the info panel)

