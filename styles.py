COLORS = {
    'background': '#3A3B3C',
    'foreground': '#E4E6EB',
    'accent': '#5778A8',
    'success': '#6DA56F',
    'warning': '#D4A15F',
    'error': '#C75D5D',
    'highlight': '#5D8EC7',
    'text': '#E4E6EB',
    'card': '#242526'
}

FONTS = {
    'title': ('Segoe UI', 14, 'bold'),
    'header': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 11),
    'button': ('Segoe UI', 11, 'bold'),
    'input': ('Segoe UI', 11)
}

def configure_styles():
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Custom.TFrame', background=COLORS['background'])
    style.configure('Card.TLabelframe', background=COLORS['background'], foreground=COLORS['highlight'], bordercolor=COLORS['accent'])
    style.configure('Card.TLabelframe.Label', background=COLORS['background'], foreground=COLORS['highlight'], font=FONTS['header'])
    style.configure('Title.TLabel', background=COLORS['background'], foreground=COLORS['highlight'], font=FONTS['title'])
    style.configure('Header.TLabel', background=COLORS['background'], foreground=COLORS['highlight'], font=FONTS['header'])
    style.configure('Body.TLabel', background=COLORS['background'], foreground=COLORS['text'], font=FONTS['body'])
    style.configure('Stats.TLabel', background=COLORS['background'], foreground=COLORS['highlight'], font=('Segoe UI', 11, 'bold'))
    style.configure('Custom.TEntry', fieldbackground=COLORS['card'], foreground=COLORS['text'], insertcolor=COLORS['text'], font=FONTS['input'])
    style.configure('Accent.TButton', background=COLORS['accent'], foreground=COLORS['text'], font=FONTS['button'])
    style.configure('Success.TButton', background=COLORS['success'], foreground=COLORS['text'], font=FONTS['button'])
    style.configure('Warning.TButton', background=COLORS['warning'], foreground=COLORS['text'], font=FONTS['button'])
    style.configure('Custom.Treeview', background=COLORS['card'], foreground=COLORS['text'], fieldbackground=COLORS['card'])
    style.map('Custom.Treeview', background=[('selected', COLORS['accent'])])
    style.configure('Custom.Treeview.Heading', background=COLORS['accent'], foreground=COLORS['text'], font=FONTS['body'])
