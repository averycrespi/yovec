from tkinter import Tk, IntVar
from tkinter.ttk import Frame, Label, Checkbutton, Radiobutton, Button
from tkinter.scrolledtext import ScrolledText


class GUI:
    def __init__(self):
        self._init_root()

    def _init_root(self):
        self.root = Tk()
        self.root.title('Yovec')
        for i in (0, 5, 6):
            self.root.rowconfigure(i, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, weight=1)
        self._init_content()

    def _init_content(self):
        self.content = Frame(self.root).grid()
        self._init_source()
        self._init_optimizations()
        self._init_format()
        self._init_run()
        self._init_log()
        self._init_output()
        self._init_copy()

    def _init_source(self):
        self.source_text = ScrolledText(self.content, height=20)
        self.source_text.grid(row=0, column=0, columnspan=3, sticky='NEWS')

    def _init_optimizations(self):
        self.optimizations_label = Label(self.content, text='Optimizations')
        self.optimizations_label.grid(row=1, column=0, sticky='NW')

        self.elim_var = IntVar(value=1)
        self.elim_check = Checkbutton(self.content, text='Eliminate dead code', var=self.elim_var)
        self.elim_check.grid(row=2, column=0, sticky='NW')

        self.reduce_var = IntVar(value=1)
        self.reduce_check = Checkbutton(self.content, text='Reduce expressions', var=self.reduce_var)
        self.reduce_check.grid(row=3, column=0, sticky='NW')

        self.mangle_var = IntVar(value=1)
        self.mangle_check = Checkbutton(self.content, text='Mangle names', var=self.mangle_var)
        self.mangle_check.grid(row=4, column=0, sticky='NW')

    def _init_format(self):
        self.format_label = Label(self.content, text='Format')
        self.format_label.grid(row=1, column=1, sticky='NW')

        self.format_var = IntVar(value=0)

        self.text_radio = Radiobutton(self.content, text='Text', var=self.format_var, value=0)
        self.text_radio.grid(row=2, column=1, sticky='W')

        self.yovec_radio = Radiobutton(self.content, text='Yovec AST', var=self.format_var, value=1)
        self.yovec_radio.grid(row=3, column=1, sticky='W')

        self.cylon_radio = Radiobutton(self.content, text='Cylon AST', var=self.format_var, value=2)
        self.cylon_radio.grid(row=4, column=1, sticky='W')

    def _init_run(self):
        self.run_button = Button(self.content, text='Run')
        self.run_button.grid(row=1, column=2, rowspan=4, sticky='SE')

    def _init_log(self):
        self.log_text = ScrolledText(self.content, height=10)
        self.log_text.grid(row=5, column=0, columnspan=3, sticky='NEWS')
        self.log_text.configure(state='disabled')

    def _init_output(self):
        self.output_text = ScrolledText(self.content, height=20)
        self.output_text.grid(row=6, column=0, columnspan=3, sticky='NEWS')
        self.output_text.configure(state='disabled')

    def _init_copy(self):
        self.copy_button = Button(self.content, text='Copy')
        self.copy_button.grid(row=7, column=2, sticky='SE')

    def loop(self):
        self.root.mainloop()


GUI().loop()
