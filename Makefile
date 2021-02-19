.PHONY: data/results.xlsx data/results.tsv

out: all-data
	python massage_templates.py
	python copy_massaged_data.py
	python generate_charts.py
	python generate_profiling.py
	cp data/results.xlsx out/raw.xlsx
	cp data/results.tsv out/raw.tsv

all-data: data/results.xlsx data/results.tsv

data/results.xlsx:
	curl -fsSL -o $@ "https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=xlsx"

data/results.tsv:
	curl -fsSL -o $@ "https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=tsv"
