from os.path import realpath, dirname
from pathlib import Path

from tkinter import Tk, IntVar
from tkinter.ttk import Frame, Label, Checkbutton, Radiobutton, Button
from tkinter.scrolledtext import ScrolledText

from engine.errors import YovecError
from engine.run import run_yovec
from engine.version import VERSION


class GUI:
    """Manages the Yovec guided user interface."""
    def __init__(self):
        self._init_root()

    def _init_root(self):
        """Initialize the root object."""
        self.root = Tk()
        self.root.title('Yovec v{}'.format(VERSION))
        self.root.resizable(False, False)
        self._init_content()

    def _init_content(self):
        """Initialize the content frame."""
        self.content = Frame(self.root)
        self.content.grid()
        self._init_source()
        self._init_optimizations()
        self._init_format()
        self._init_run()
        self._init_output()
        self._init_copy()

    def _init_source(self):
        """Initialize the source box."""
        self.source_text = ScrolledText(self.content, width=70, height=20 )
        self.source_text.grid(row=0, column=0, columnspan=3, sticky='NEWS')
        self.source_text.bind('<Shift-Return>', self.run)
        self.source_text.bind('<Control-Key-a>', self.select_source)
        self.source_text.bind('<Control-Key-A>', self.select_source)

    def _init_optimizations(self):
        """Initialize the optimization options."""
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
        """Initialize the formatting options."""
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
        """Initialize the run button."""
        self.run_button = Button(self.content, text='Run', command=self.run)
        self.run_button.grid(row=1, column=2, rowspan=4, sticky='SE')

    def _init_output(self):
        """Initialize the output box."""
        self.output_text = ScrolledText(self.content, width=70, height=20)
        self.output_text.grid(row=5, column=0, columnspan=3, sticky='NEWS')
        self.output_text.configure(state='disabled')

    def _init_copy(self):
        """Initialize the copy button."""
        self.copy_button = Button(self.content, text='Copy', command=self.copy)
        self.copy_button.grid(row=6, column=2, sticky='SE')

    def select_source(self, *args):
        """Select the source."""
        self.source_text.tag_add('sel', '1.0', 'end')
        self.source_text.mark_set('insert', '1.0')
        self.source_text.see('insert')
        return 'break'

    def clear_output(self):
        """Clear the output."""
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.configure(state='disabled')

    def fill_output(self, text):
        """Fill the output with text."""
        self.output_text.configure(state='normal')
        self.output_text.insert('end', text)
        self.output_text.configure(state='disabled')

    def run(self, *args):
        """Run Yovec."""
        self.clear_output()
        try:
            output = run_yovec(
                self.source_text.get('1.0', 'end'),
                root=Path(dirname(realpath(__file__))),
                no_elim=not self.elim_var.get(),
                no_reduce=not self.reduce_var.get(),
                no_mangle=not self.mangle_var.get(),
                ast=bool(self.format_var.get() == 1),
                cylon=bool(self.format_var.get() == 2)
            )
        except YovecError as e:
            self.fill_output(str(e))
        except Exception as e:
            self.fill_output('Unexpected error: {}'.format(str(e)))
        else:
            self.fill_output(output)

    def copy(self):
        """Copy the output to the clipboard."""
        output = self.output_text.get('1.0', 'end')
        self.root.clipboard_clear()
        self.root.clipboard_append(output)
        self.root.update()

    def loop(self):
        """Start the GUI."""
        self.root.mainloop()


GUI().loop()
