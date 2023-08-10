## README for Command Library

# Requirements:
Command Library was written in Python 3.9, and the GUI uses TKinter.  
To run properly, you must have both of these installed on your system.

# Installation:
On MacOS, you can use homebrew for both requirements:  
*brew install Python*  
*brew install tcl-tk*  
Then, just clone this git repo, and run command_library_.py

[Note: if you run into tcl errors such as `ModuleNotFoundError: No module named '_tkinter'` try `brew install python-tk`]

# Operation:
Upon opening the app, you will be presented with a 3 part window. The 1st pane contains the Dictionary selection dropdown and a snippet search box.
The dictionary Selector dropdown allows you to switch between all dictionaries in your currently loaded Mohel. The search bar allows you to filter the list of Snippets for easy access.  
The center pane, is a clickable list of all snippets. Clicking a snippet once, will select it and show info in the Info panel. Double-Clicking a snippet will copy the code to your clipboard for use in any program.  
Finally the bottom info pane will show you a) the actual command itself and b) any information or options regarding the command.  

DB files can be imported/exported via the Library menu. Upon exiting, the current DB is saved (~/MyDB.lib). This fill will automatically be re-loaded the next time you open Command Library.  

Finally, a special dictionary called "Recently Used" will contain a list of all Snippets that you have copied to the clipboard in order of usage.

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

