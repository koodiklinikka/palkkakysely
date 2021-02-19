.PHONY: data/results.xlsx data/results.tsv

all: data/results.xlsx data/results.tsv

data/results.xlsx:
	curl -fsSL -o $@ "https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=xlsx"

data/results.tsv:
	curl -fsSL -o $@ "https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=tsv"
