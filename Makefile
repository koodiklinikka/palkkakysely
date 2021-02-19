.PHONY: data/results.xlsx data/results.tsv

out: all-data copy-raw-data copy-massaged-data static charts profiling

copy-raw-data: all-data
	cp data/results.xlsx out/raw.xlsx
	cp data/results.tsv out/raw.tsv

copy-massaged-data: all-data
	python copy_massaged_data.py

static: all-data
	python massage_templates.py

charts: all-data
	python generate_charts.py

profiling: all-data
	python generate_profiling.py

all-data: data/results.xlsx data/results.tsv

data/results.xlsx:
	curl -fsSL -o $@ "https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=xlsx"

data/results.tsv:
	curl -fsSL -o $@ "https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=tsv"
