#!/opt/homebrew/bin/python3
# Command Library v1.2
# Created by: Ian Campbell

###Import Modules
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
from tkinter import filedialog
import pickle
import json
import os
from os import path
import glob
import atexit

###Initialize Global Variables
MyLib={}
MyLib['Recently Used']=[]

#Class Definitions
class Snippet:
    def __init__(self, title, code, info):
        self.title = title
        self.code = code
        self.info = info

class root_window_class():
    def __init__(self, master):
        self.master = master
        self.master.title("Command Library")
        self.master.geometry("850x475")
        self.master.minsize(640, 355)
        
        self.master.rowconfigure(0,weight=0)
        self.master.rowconfigure(1,weight=0)
        self.master.rowconfigure(2,weight=1)
        self.master.rowconfigure(3,weight=0)
        self.master.rowconfigure(4,weight=0)
        self.master.rowconfigure(5,weight=0)
        self.master.columnconfigure(0,weight=1)
        self.master.columnconfigure(1,weight=0)
        self.__create_widgets()
        self.__bind_widgets()
        
        self.PopulateDictSelector()

    def __create_widgets(self):
        self.ToolbarFrame = tk.Frame(self.master)
        self.ToolbarFrame.grid(column='0', row='0', sticky='nsew', padx=4, columnspan=2)
        tk.Grid.columnconfigure(self.ToolbarFrame,0,weight=1)
        tk.Grid.columnconfigure(self.ToolbarFrame,1,weight=0)
        tk.Grid.columnconfigure(self.ToolbarFrame,2,weight=0)
        self.DictSelector = ttk.Combobox(self.ToolbarFrame, values=list(MyLib.keys()) , state="readonly")
        self.DictSelector.grid(column='0', row='0',sticky="ew", pady=(4,0))
        self.DictSelector.set(self.DictSelector['values'][0])
        
        self.InspectorButton = ttk.Button(self.ToolbarFrame, text='Inspector', command=self.ToggleInspector, takefocus=False)
        self.InspectorButton.grid(column='1', row='0', sticky='e',padx=(4,4), pady=(1,0))

        self.SearchButton = ttk.Button(self.ToolbarFrame, text='Search', command=lambda: self.open_global_search(None), takefocus=False)
        self.SearchButton.grid(column='2', row='0', sticky='e', padx=(0,4), pady=(1,0))

        #Create a label for the logo
        #self.Logo = tk.PhotoImage(file='images/Logo.png')
        #self.IconLabel = tk.Label(self.ToolbarFrame, image = self.Logo)
        #self.IconLabel.grid(column='2', row='0', sticky="e", padx=(30,0))

        #Create a separator
        self.Divider=ttk.Separator(self.master,orient='horizontal')
        self.Divider.grid(column=0,row=1,sticky='ew',columnspan=4,pady=4)

        #Create a frame for the snippets, set its grid to allow scaling, and put in the Snippet List and its scrollbar
        self.SnippetListFrame=tk.Frame(self.master, height=400, bd=1, relief=tk.SUNKEN)
        self.SnippetListFrame.grid(column=0, row=2, sticky="nsew", padx=4,columnspan=1)
        tk.Grid.columnconfigure(self.SnippetListFrame,0,weight=1)
        tk.Grid.rowconfigure(self.SnippetListFrame,0,weight=1)

        self.SnippetList = tk.Listbox(self.SnippetListFrame, selectmode='single', borderwidth=0)
        self.SnippetList.grid(column='0',row='0',sticky="nsew")
        self.SnippetScrollbar = ttk.Scrollbar(self.SnippetListFrame, orient="vertical")
        self.SnippetList.config(yscrollcommand = self.SnippetScrollbar.set)
        self.SnippetScrollbar.config(command = self.SnippetList.yview)
        self.SnippetScrollbar.grid(column='1',row='0',sticky="nsew")
        
        # #Create the Searchbox and its label
        self.SearchBar = ttk.Entry(self.SnippetListFrame, width=20)
        self.SearchBar.grid(column='0',row='1',sticky="nsew", columnspan=2, padx=(0,0), pady=0)
        self.SearchBar.insert(tk.END,"type here to filter the command list...")

        #Create a separator
        self.Divider=ttk.Separator(self.master,orient='horizontal')
        self.Divider.grid(column=0,row=3,sticky='ew',columnspan=4,pady=(4,0))
        
        #Create the status bar and tie it to a variable for modification
        self.statusvar = tk.StringVar()
        self.sbar = ttk.Label(self.master, textvariable=self.statusvar, relief="flat", anchor="e")
        self.sbar.grid(column="0", row="4", sticky="sew",columnspan=4,pady=(0,0), padx=(4,4))

        #Create the InfoFrame
        self.InfoFrame=tk.Frame(self.master)
        self.InfoFrame.grid(column=1, row=2, sticky="nsew", padx=(4,8))
        #tk.Grid.columnconfigure(self.InfoFrame,0,weight=1)
        tk.Grid.rowconfigure(self.InfoFrame,1,weight=1)
        tk.Grid.rowconfigure(self.InfoFrame,2,weight=1)

        self.TitleLabel = ttk.LabelFrame(self.InfoFrame, text="Title")
        self.TitleLabel.grid(column='0', row='0', sticky='nsew', padx=4, pady=4)
        self.TitleContent = tk.Text(self.TitleLabel, width=50, height=1, bd=1, relief=tk.SUNKEN, highlightthickness=0)
        self.TitleContent.grid(column='0', row='0', pady=5, padx=5, sticky='nsew')

        self.InfoLabel = ttk.LabelFrame(self.InfoFrame, text="Description")
        self.InfoLabel.grid(column='0', row='1', sticky='nsew', padx=4, pady=4)
        tk.Grid.rowconfigure(self.InfoLabel,0,weight=1)
        self.InfoContent = tk.Text(self.InfoLabel, width=50, bd=1, relief=tk.SUNKEN,highlightthickness=0,wrap=tk.WORD)
        self.InfoContent.grid(column='0', row='0', pady=5, padx=5, sticky='nsew')

        self.SnippetTextLabel = ttk.LabelFrame(self.InfoFrame, text="Snippet Text")
        self.SnippetTextLabel.grid(column='0', row='2', sticky='nsew', padx=4, pady=4)
        tk.Grid.rowconfigure(self.SnippetTextLabel,0,weight=1)
        self.SnippetTextContent = tk.Text(self.SnippetTextLabel, width=50, bd=1, relief=tk.SUNKEN,highlightthickness=0,wrap=tk.WORD)
        self.SnippetTextContent.grid(column='0', row='0', pady=5, padx=5, sticky='nsew')
        
        self.InfoToolbar=tk.Frame(self.InfoFrame)
        self.InfoToolbar.grid(column=0, row=6, sticky='ew')
        self.InfoToolbar.grid_columnconfigure(0, weight=1)
        self.InfoToolbar.grid_columnconfigure(1, weight=1)
        self.SaveButton=ttk.Button(self.InfoToolbar, text="Save", command=lambda: self.save_dict_entry(self))
        self.SaveButton.grid(column=0, row=0, padx=2, sticky='e')
        self.DeleteButton=ttk.Button(self.InfoToolbar, text="Delete", command=lambda: self.delete_dict_entry(self))
        self.DeleteButton.grid(column=1, row=0, padx=2, sticky='w')

        #Create our Menu Items
        self.menubar = tk.Menu(self.master)
        self.librarymenu = tk.Menu(self.menubar)
        self.dictmenu = tk.Menu(self.menubar)
        self.viewmenu = tk.Menu(self.menubar)
        self.searchmenu = tk.Menu(self.menubar)

        self.librarymenu.add_command(label="Open Library", command=lambda: LoadLib())
        self.librarymenu.add_command(label="Save Library", command=lambda: SaveLib())
        self.librarymenu.add_command(label="Edit Library", command=lambda: self.open_lib_edit(self))
        self.librarymenu.add_separator()
        self.librarymenu.add_command(label="Unload All Dictionaries", command=lambda: ClearDicts())

        self.dictmenu.add_command(label="New Dictionary File", command =lambda: NewDictFile())
        self.dictmenu.add_command(label="Import Dictionary File", command =lambda: ImportJSONfiletoDict())
        self.dictmenu.add_command(label="Export Dictionary File", command =lambda: ExportDicttoJSONfile())
        self.dictmenu.add_separator()
        self.dictmenu.add_command(label="Import Dictionary Folder", command =lambda: ImportFoldertoDict())
        self.dictmenu.add_separator()
        self.dictmenu.add_command(label="New Dictionary Entry", command =lambda: self.new_dict_entry(), accelerator="CMD+N")

        self.ShowInspector = tk.IntVar()
        self.ShowInspector.set(1)
        self.viewmenu.add_checkbutton(label="Show Inspector", var=self.ShowInspector, command=lambda: self.ToggleInspector(), accelerator="CMD+I")
        
        self.OnTop = tk.IntVar()
        self.OnTop.set(0)
        self.viewmenu.add_checkbutton(label="Always On Top", var=self.OnTop, command=lambda: self.ToggleTopmost(self))

        self.searchmenu.add_command(label="Global Search", command=lambda: self.open_global_search(self), accelerator="CMD+S")

        self.menubar.add_cascade(label = "Library", menu = self.librarymenu)
        self.menubar.add_cascade(label = "Dictionary", menu = self.dictmenu)
        self.menubar.add_cascade(label = "View", menu = self.viewmenu)
        self.menubar.add_cascade(label = "Search", menu = self.searchmenu)
        self.master.config(menu = self.menubar)

    def __bind_widgets(self):
        #Binding Widget Events to their Event Handlers
        self.SearchBar.bind("<KeyRelease>", self.FilterListBox)
        self.SearchBar.bind("<Button-1>", self.Search_Click)
        self.SearchBar.bind("<FocusOut>", self.Search_Reset)
        self.SnippetList.bind('<Double-Button-1>', self.Snippet_DoubleClick)
        self.SnippetList.bind('<<ListboxSelect>>', self.Snippet_Select)
        self.DictSelector.bind("<<ComboboxSelected>>", self.DictChanged)
        self.master.bind("<Command-n>", self.new_dict_entry)
        self.master.bind("<Command-s>", self.open_global_search)
        self.master.bind("<Command-i>", self.ToggleInspector)
        self.InfoContent.bind("<Tab>", self.focus_next_widget)
        self.SnippetTextContent.bind("<Tab>", self.focus_next_widget)
        self.TitleContent.bind("<Tab>", self.focus_next_widget)

    def PopulateDictSelector(self):
        self.DictSelector['values']=sorted(list(MyLib.keys()), key=str.casefold)

    def PopulateListBox(self):
        self.SnippetList.delete(0, tk.END)
        CurrentDict = self.DictSelector.get()
        for snippet in MyLib[CurrentDict]:
                self.SnippetList.insert("end",snippet.title)    

    def FilterListBox(self, event):
        search_param=self.SearchBar.get()
        self.SnippetList.delete(0, tk.END)
        CurrentDict = self.DictSelector.get()
        for snippet in MyLib[CurrentDict]:
            if search_param.lower() in snippet.title.lower():
                self.SnippetList.insert("end",snippet.title)    

    def Snippet_DoubleClick(self,event):
        SelectedTitle=self.SnippetList.get("anchor")
        CurrentDict = self.DictSelector.get()
        for snippet in MyLib[CurrentDict]:
            if snippet.title == SelectedTitle:
                snippet_code = snippet.code
                self.master.clipboard_clear()
                self.master.clipboard_append(snippet_code)
                self.statusvar.set("Copied [" + SelectedTitle.strip() + "] to clipboard.")
                if snippet not in MyLib['Recently Used']:
                    MyLib['Recently Used'].append(snippet)
                break
            else:
                self.statusvar.set("Snippet code entry not found.")

    def Snippet_Select(self,event):
        self.SelectedTitle=self.SnippetList.get("anchor")
        self.CurrentDict = self.DictSelector.get()
        for snippet in MyLib[self.CurrentDict]:
            if snippet.title == self.SelectedTitle:
                self.TitleContent.delete("1.0","end")
                self.TitleContent.insert(tk.END,snippet.title)
                
                self.InfoContent.delete("1.0","end")
                self.InfoContent.insert(tk.END,snippet.info)
                
                self.SnippetTextContent.delete("1.0","end")
                self.SnippetTextContent.insert(tk.END,snippet.code)
                break

    def Search_Click(self,event):
        if self.SearchBar.get() == 'type here to filter the command list...':
            self.SearchBar.delete(0, tk.END)
            #self.SearchBar.config(fg = 'black')
        else:
            return

    def Search_Reset(self,event):
        if self.SearchBar.get() == '':
            #self.SearchBar.config(fg = 'gray')
            self.SearchBar.insert(tk.END,"type here to filter the command list...")
        else:
            return
    
    def DictChanged(self,event):
        self.PopulateListBox()
    
    def ToggleInspector(self, event=None):
        window_width=self.master.winfo_width()
        window_height=self.master.winfo_height()
        
        if self.InfoFrame.grid_info() == {}:
            self.master.geometry(f"{window_width + 388}x{window_height}")
            self.InfoFrame.grid()
            self.master.minsize(640, 355)
            self.ShowInspector.set(1)
            #self.InspectorButton.configure(text="ℹ︎")
        else:
            self.master.geometry(f"{window_width - 388}x{window_height}")
            self.InfoFrame.grid_remove()
            self.master.minsize(250, 355)
            self.ShowInspector.set(0)
            #self.InspectorButton.configure(text="ℹ︎")
            
    def close_windows(self):
        self.master.destroy()

    def ToggleTopmost(self, event):
        if self.OnTop.get() == 1:
            self.master.attributes('-topmost', True)
            self.master.update()
        else:
            self.master.attributes('-topmost', False)
            self.master.update()

    def open_lib_edit(self, event):
        self.newLibeditWindow = tk.Toplevel(self.master)
        self.lib_edit_window = lib_edit_window_class(self.newLibeditWindow)

    def new_dict_entry(self,event):
        self.CurrentDict = self.DictSelector.get()
        MyLib[self.CurrentDict].append(Snippet("new title", "new code", "new info"))
        self.PopulateListBox()
        
    def delete_dict_entry(self, event):
        self.SelectedTitle = self.SnippetList.get("anchor")
        self.CurrentDict = self.DictSelector.get()
        msg_box = tk.messagebox.askquestion('Delete Snippet', f'Are you sure you want to delete {self.SelectedTitle}?',icon='warning')
        if msg_box == 'yes':
            for snippet in MyLib[self.CurrentDict]:
                if snippet.title == self.SelectedTitle:
                    MyLib[self.CurrentDict].remove(snippet)
                    self.PopulateListBox()
                    self.TitleContent.delete("1.0","end")
                    self.InfoContent.delete("1.0","end")
                    self.SnippetTextContent.delete("1.0","end")
                    break
        
    def save_dict_entry(self, event):
        self.SelectedTitle = self.SnippetList.get("anchor")
        self.CurrentDict = self.DictSelector.get()
        for snippet in MyLib[self.CurrentDict]:
            if snippet.title == self.SelectedTitle:
                snippet.title = self.TitleContent.get("1.0",tk.END)
                snippet.info = self.InfoContent.get("1.0",tk.END)
                snippet.code = self.SnippetTextContent.get("1.0",tk.END)
                self.PopulateListBox()
                break

    def focus_next_widget(self,event):
        event.widget.tk_focusNext().focus()
        return("break")

    def open_global_search(self, event):
        self.newSearchWindow = tk.Toplevel(self.master)
        self.global_search_window = global_search_window_class(self.newSearchWindow)

class lib_edit_window_class():
    def __init__(self, master):
        global MyLib
        self.master = master
        self.master.title("Library Editor")
        
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        self.ChecklistFrame = tk.Frame(self.master)
        self.ChecklistFrame.grid(column=0, row=0, columnspan=1, sticky='nsew')

        self.DictList = []
        self.vars=[]
        for dict in MyLib.keys():
            self.var = tk.IntVar()
            self.vars.append(self.var)
            self.DictList.append(tk.Checkbutton(self.ChecklistFrame, text=dict, variable=self.var,anchor="w"))
            self.DictList[-1].grid(column=0, row=len(self.DictList), sticky='nsew')
            self.var.set(1)

        height=(len(self.DictList) * 25 + 25)
        print(height)
        self.master.geometry(f"275x{str(height)}")

        self.buttonframe = tk.Frame(self.master)
        self.buttonframe.grid(column=0,row=1,sticky='sew')
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        okb = ttk.Button(self.buttonframe, text='OK', command=self.savedicts)
        okb.grid(column=0,row=0,sticky='sew')

        cancelb = ttk.Button(self.buttonframe, text='Cancel', command=self.canceldicts)
        cancelb.grid(column=1,row=0,sticky='sew')

    def savedicts(self):
        for var in self.vars:
            if var.get() == 0:
                delete_target = self.DictList[self.vars.index(var)].cget("text")
                print(delete_target)
                MyLib.pop(delete_target)
        root_window.DictSelector['values']=list(MyLib.keys())
        self.master.destroy()

    def canceldicts(self):
        self.master.destroy()

class global_search_window_class():
    def __init__(self, master):
        self.master = master
        self.master.title("Global Search")
        window_width = 465
        window_height = 290
        screen_width = self.master.master.winfo_screenwidth()
        screen_height = self.master.master.winfo_screenheight()
        position_top = int(screen_height/2 -window_height/2)
        position_right = int(screen_width / 2 - window_width/2)
        self.master.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=0)
        self.master.rowconfigure(1,weight=0)
        self.master.rowconfigure(2,weight=1)
        self.__create_widgets()
        self.__bind_widgets()

    def __create_widgets(self):
        self.big_font = tkfont.Font(font=tkfont.nametofont("TkDefaultFont"))
        self.big_font.configure(size=32)
        self.searchframe = tk.Frame(self.master)
        self.searchframe.grid(column=0, row=0, sticky='new')
        self.searchlabel = tk.Label(self.searchframe, text=">", relief=tk.FLAT)
        self.searchlabel.grid(column=0, row=0)
        self.searchbox = tk.Entry(self.searchframe, highlightthickness=0, relief=tk.FLAT,font=self.big_font, bg=self.master.cget('bg'))
        self.searchbox.grid(column=1, row=0, sticky='new')
        self.searchbox.focus_set()
        
        self.Divider=ttk.Separator(self.master,orient='horizontal')
        self.Divider.grid(column=0,row=1,sticky='ew',pady=(4,0))
        
        self.resultbox = tk.Listbox(self.master, relief=tk.FLAT, bg=self.master.cget('bg'))
        self.resultbox.grid(column=0, row=2, sticky='nsew', padx=4)
        
    def __bind_widgets(self):
        self.master.bind("<FocusOut>", self.close_window)
        self.resultbox.bind("<Escape>", self.close_window)
        self.searchbox.bind("<Escape>", self.close_window)
        self.searchbox.bind("<KeyRelease>", self.do_search)
        self.searchbox.bind('<Down>', self.focus_results)
        self.resultbox.bind('<Up>', self.focus_search)
        self.resultbox.bind('<Return>', self.copy_snippet_to_clipboard)
        self.resultbox.bind('<Double-Button-1>', self.copy_snippet_to_clipboard)
        
    def close_window(self, event):
        if event.type == "10" and event.widget == self.master:
            self.master.destroy()
        if event.keysym == "Escape":
            self.master.destroy()
        
    def do_search(self, event):
        if event.keysym == "Escape":
            self.master.destroy()
            return
        self.resultslist=[]
        self.resultbox.delete(0,tk.END)
        currentvalue=self.searchbox.get().lower()
        for key in MyLib.keys():
            for snippet in MyLib[key]:
                if currentvalue in snippet.title.lower():
                    self.resultslist.append(snippet)
                    #break
        
        # for snippetindex, snippet in enumerate(self.resultslist):
        #     self.resultbox.insert(tk.END, f"{snippetindex}. {snippet.title}")
        for snippet in self.resultslist:
            self.resultbox.insert(tk.END, snippet.title)
        
    def focus_results(self, event):
        self.resultbox.focus_set()
        
    def focus_search(self, event):
        first_item=self.resultbox.get(0)
        if self.resultbox.get(tk.ACTIVE) == first_item:
            self.searchbox.focus_set() 
            
    def copy_snippet_to_clipboard(self, event):
        global MyLib
        current_title=self.resultbox.get(tk.ACTIVE)
        self.master.master.clipboard_clear()
        for snippet in self.resultslist:
            if current_title in snippet.title:
                self.master.master.clipboard_append(snippet.code)
                root_window.statusvar.set("Copied [" + snippet.title.strip() + "] to clipboard.")
                if snippet not in MyLib['Recently Used']:
                    MyLib['Recently Used'].append(snippet)
                break
        
                
                
        self.master.destroy()
    
    
    
###Global Function Definitions
def LoadLib(filepath=None):
    if filepath == None:
        filepath = tk.filedialog.askopenfilename()
    global MyLib

    pickleloadfile = open(filepath,"rb")
    MyLib = pickle.load(pickleloadfile)
    pickleloadfile.close()
    
    root_window.PopulateDictSelector()
    root_window.statusvar.set(f"Library [{os.path.basename(pickleloadfile.name)}] loaded")

def SaveLib(filepath=None):
    if filepath == None:
        filepath = tk.filedialog.asksaveasfilename(initialfile="MyLib.lib", defaultextension=".lib")
    picklesavefile = open(filepath,"wb")
    pickle.dump(MyLib, picklesavefile)
    picklesavefile.close()
    root_window.statusvar.set(f"Library saved as [{os.path.basename(picklesavefile.name)}]")

def ImportJSONfiletoDict(filepath=None):
    filetypes = (
        ('Dict files', '*.dct'),
        ('All files', '*.*')
    )
    if filepath == None:
        filepath = tk.filedialog.askopenfilename(filetypes=filetypes)
    with open(filepath, 'r') as DictFile:
        fname=os.path.basename(filepath)
        MyLib[fname]=[]
        tmpdict = json.load(DictFile, strict=False)
        for item in tmpdict['snippets']:
            MyLib[fname].append( Snippet(item['title'], item['code'], item['info']) )
    root_window.DictSelector['values']=sorted(list(MyLib.keys()), key=str.casefold)
    root_window.statusvar.set(fname + " loaded.")

def ImportFoldertoDict(folderpath=None):
    if folderpath == None:
        folderpath = tk.filedialog.askdirectory(initialdir=os.path.dirname(os.path.realpath(__file__)))
    fileslist = glob.glob(folderpath+"/*.dct")
    for file in fileslist:
        print("File:")
        print(file)
        with open(file, 'r') as DictFile:
            fname=os.path.basename(file)
            MyLib[fname]=[]
            tmpdict = json.load(DictFile, strict=False)
            for item in tmpdict['snippets']:
                MyLib[fname].append( Snippet(item['title'], item['code'], item['info']) )
        root_window.DictSelector['values']=sorted(list(MyLib.keys()), key=str.casefold)
        root_window.statusvar.set(fname + " loaded.")

def ExportDicttoJSONfile(currentFilename="MyDict.dct"):
    filepath = tk.filedialog.asksaveasfilename(initialfile=currentFilename, defaultextension=".dct")

    dictsavefile = open(filepath,"w")
    key = root_window.DictSelector.get()
    tmpJSONdict = {}
    tmpJSONdict['snippets'] = []
    for snippet in MyLib[key]:
        tmpJSONdict['snippets'].append({"title" : snippet.title, "code" : snippet.code, "info" : snippet.info})
    json.dump(tmpJSONdict, dictsavefile, indent=4)
    dictsavefile.close()

def NewDictFile(currentFilename="MyDict.dct"):
    filepath = tk.filedialog.asksaveasfilename(initialfile=currentFilename, defaultextension=".dct")
    fname=os.path.basename(filepath)
    MyLib[fname]=[]
    root_window.DictSelector['values']=list(MyLib.keys())
    root_window.DictSelector.set(fname)
    #EditDict()
    dictsavefile = open(filepath,"w")
    key = root_window.DictSelector.get()
    tmpJSONdict = {}
    tmpJSONdict['snippets'] = []
    for snippet in MyLib[key]:
        tmpJSONdict['snippets'].append({"title" : snippet.title, "code" : snippet.code, "info" : snippet.info})
    json.dump(tmpJSONdict, dictsavefile, indent=4)
    dictsavefile.close()

def ClearDicts():
    global MyLib

    MyLib={}
    MyLib['Recently Used']=[]
    root_window.DictSelector['values']=list(MyLib.keys())
    root_window.DictSelector.set('Recently Used')
    root_window.PopulateListBox()

### Program Init
#Create the main app window and start the TK loop
root_tk = tk.Tk()
root_window = root_window_class(root_tk)

#attempt to autoload pickled Lib file
curpath=os.getcwd()
if path.exists(curpath + "/MyLib.lib"):
    LoadLib("MyLib.lib")

#Main Loop
def main(): 
    root_tk.mainloop()

#Start the main loop
if __name__ == '__main__':
    main()

#autosave Lib at exit
atexit.register(lambda: SaveLib(filepath = "./MyLib.lib"))
