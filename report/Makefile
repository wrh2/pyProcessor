PDFS := $(patsubst %.md,%.pdf,$(wildcard *.md))

all : $(PDFS)

%.pdf : %.md
	pandoc -V geometry:margin=.5in --latex-engine=xelatex $< -o $@

clean :
	rm $(PDFS)

rebuild : clean all