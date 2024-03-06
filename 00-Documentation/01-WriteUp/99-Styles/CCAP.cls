\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CCAP}[2020/08/27]
\usepackage{color}      % use if color is used in text
\definecolor{DarkRed}{cmyk}{0.00, 0.99, 0.99, 0.25}
\definecolor{RedViolet}{cmyk}{0.60, 0.99, 0.99, 0.0}
\definecolor{Blue}{cmyk}{0.95, 0.75, 0.0, 0.25}
\definecolor{BlueViolet}{cmyk}{0.90, 0.70, 0.10, 0.0}
\definecolor{DarkBlue}{cmyk}{0.90, 0.65, 0.25, 0.0}
\definecolor{DarkGreen}{cmyk}{0.95, 0.25, 0.95, 0.25}
\definecolor{DarkYellow}{cmyk}{0.0, 0.25, 0.95, 0.25}
\let\ccap@startsection\@startsection
%\LoadClass[a4paper,fleqn,preprintnumbers,nofootinbib,PRD,11pt]{revtex4-1}
\LoadClass[11pt,twoside,a4paper,fleqn,titlepage]{article}
%-- YU: [prl,12pt,tightenlines]
\renewcommand\thesection{\arabic{section}}
\renewcommand\p@section{}
\renewcommand\thesubsection{\thesection.\arabic{subsection}}
\renewcommand\p@subsection{}
\renewcommand\thesubsubsection{\thesubsection.\arabic{subsubsection}}
\renewcommand\p@subsubsection{}
\renewcommand\theparagraph{\thesubsubsection.\arabic{paragraph}}
\renewcommand\p@paragraph{}
\renewcommand\thesubparagraph{\theparagraph.\arabic{subparagraph}}
\renewcommand\p@subparagraph{}
\renewcommand\section{%
\@startsection{section}{1}{\z@}%
              {-3.5ex \@plus -1ex \@minus -.2ex}%
              {2.3ex \@plus.2ex}%
              {\color{Blue}\sffamily\Large\bfseries}}
\renewcommand\subsection{%
\@startsection{subsection}{2}{\z@}%
              {-3.25ex\@plus -1ex \@minus -.2ex}%
              {1.5ex \@plus .2ex}%
              {\color{BlueViolet}\sffamily\large\bfseries}}
\renewcommand\subsubsection{%
\@startsection{subsubsection}{2}{\z@}%
              {-3.25ex\@plus -1ex \@minus -.2ex}%
              {1.5ex \@plus .2ex}%
              {\color{DarkBlue}\sffamily\large\bfseries}}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{5}
\newlength\ccap@border
\setlength\ccap@border{20mm}
\setlength\paperheight{297mm}
\setlength\paperwidth{210mm}
\special{papersize=210mm,297mm}
\setlength\hoffset{\ccap@border}
\addtolength\hoffset{-1in}
\setlength\oddsidemargin{0mm}
\setlength\evensidemargin{\oddsidemargin}
\setlength\textwidth{\paperwidth}
\addtolength\textwidth{-2\ccap@border}
\setlength\voffset{\ccap@border}
\addtolength\voffset{-1in}
\setlength\topmargin{0mm}
\setlength\headheight{0mm}
\setlength\headsep{0mm}
\setlength\footskip{13mm}
\setlength\textheight{\paperheight}
\addtolength\textheight{-2\ccap@border}
\addtolength\textheight{-\footskip}
\leftmargini   28pt
\leftmarginii  18pt
\leftmarginiii 18pt
\leftmarginiv  18pt
\leftmarginv   18pt
\leftmarginvi  18pt
\renewcommand\baselinestretch{1.1}
\renewcommand\@listI{\leftmargin\leftmargini\parsep0pt plus 1pt\itemsep\parsep\topsep\parsep}
\renewcommand\@listii{\leftmargin\leftmarginii\parsep0pt plus 1pt\itemsep\parsep\topsep\parsep}
\renewcommand\@listiii{\leftmargin\leftmarginiii\parsep0pt plus 1pt\itemsep\parsep\topsep\parsep}
\renewcommand\@listiv{\leftmargin\leftmarginiv\parsep0pt plus 1pt\itemsep\parsep\topsep\parsep}
\renewcommand\@listv{\leftmargin\leftmarginv\parsep0pt plus 1pt\itemsep\parsep\topsep\parsep}
\renewcommand\@listvi{\leftmargin\leftmarginvi\parsep0pt plus 1pt\itemsep\parsep\topsep\parsep}
