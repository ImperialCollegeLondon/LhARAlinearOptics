'''
  --------  --------  --------  --------  --------  --------  
    Module to contain LaTeX generatio code ...
  --------  --------  --------  --------  --------  --------  
'''

def TableHeader(FilePath='LaTex.tex', TabString='|c|c|', \
                Caption="Caption."):
    Fl = open(FilePath, 'a')

    Line = "\\begin{table}\n"
    Fl.write(Line)
    if Caption != '':
        Line = "  \\caption{" + Caption + "}\n"
        Fl.write(Line)
    Line = "  \\begin{center}\n"
    Fl.write(Line)
    Line = "    \\begin{tabular}{" + TabString + "}\n"
    Fl.write(Line)
    Line = "      \\hline\n"
    Fl.write(Line)

    Fl.close()

def TableLine(FilePath='LaTex.tex', TabString='|1|2|'):
    Fl = open(FilePath, 'a')

    if TabString.find("hline") != -1:
        Fl.write("        " + TabString + "\n")
    else:
        Fl.write("        " + TabString + " \\\\ \n")

    Fl.close()

def TableTrailer(FilePath='LaTex.tex'):
    Fl = open(FilePath, 'a')

    Line = "      \\hline\n"
    Fl.write(Line)
    Line = "    \\end{tabular}\n"
    Fl.write(Line)
    Line = "  \\end{center}\n"
    Fl.write(Line)
    Line = "\\end{table}\n"
    Fl.write(Line)

    Fl.close()
