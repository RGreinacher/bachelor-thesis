MAIN_TEX_FILE = thesis.tex
MAIN_TEX_FILE_BASENAME = thesis

pdf: compile bibliography double_compile cleanup

compile:
	pdflatex -shell-escape -halt-on-error -file-line-error $(MAIN_TEX_FILE)

bibliography:
	biber $(MAIN_TEX_FILE_BASENAME) || true

double_compile:
	pdflatex -shell-escape -halt-on-error -file-line-error $(MAIN_TEX_FILE)
	pdflatex -shell-escape -halt-on-error -file-line-error $(MAIN_TEX_FILE)

cleanup:
	rm -f $(MAIN_TEX_FILE_BASENAME)
	rm -f $(MAIN_TEX_FILE_BASENAME).aux
	rm -f $(MAIN_TEX_FILE_BASENAME).bbl
	rm -f $(MAIN_TEX_FILE_BASENAME).bcf
	rm -f $(MAIN_TEX_FILE_BASENAME).lof
	rm -f $(MAIN_TEX_FILE_BASENAME).log
	rm -f $(MAIN_TEX_FILE_BASENAME).nav
	rm -f $(MAIN_TEX_FILE_BASENAME).out
	rm -f $(MAIN_TEX_FILE_BASENAME).run.xml
	rm -f $(MAIN_TEX_FILE_BASENAME).snm
	rm -f $(MAIN_TEX_FILE_BASENAME).toc
	rm -f *blg
	rm -f *eps-converted-to.pdf
	rm -f $(MAIN_TEX_FILE_BASENAME)-gnuplottex*
	rm -f $(MAIN_TEX_FILE_BASENAME).gnuploterrors
