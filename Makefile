DATA_DIR := data/2021
OUT_DIR := out
XLSX_URL := https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=xlsx
TSV_URL := https://docs.google.com/spreadsheets/d/1l-Zgf1HqaFGd8gRA8kQzaxJ3R7eJy29ORUS8pr5o0nk/export?format=tsv

export DATA_DIR
export OUT_DIR

.PHONY: $(DATA_DIR)/results.xlsx $(DATA_DIR)/results.tsv

all: all-data copy-raw-data copy-massaged-data static charts profiling

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

copy-raw-data: all-data $(OUT_DIR)
	cp $(DATA_DIR)/results.xlsx $(OUT_DIR)/raw.xlsx
	cp $(DATA_DIR)/results.tsv $(OUT_DIR)/raw.tsv

copy-massaged-data: all-data
	python -m pulkka.copy_massaged_data

static: all-data
	python -m pulkka.massage_templates

charts: all-data
	python -m pulkka.generate_charts

profiling: all-data
	python -m pulkka.generate_profiling

all-data: $(DATA_DIR)/results.xlsx $(DATA_DIR)/results.tsv

$(DATA_DIR):
	mkdir -p $(DATA_DIR)

$(DATA_DIR)/results.xlsx: $(DATA_DIR)
	curl -fsSL -o $@ $(XLSX_URL)

$(DATA_DIR)/results.tsv: $(DATA_DIR)
	curl -fsSL -o $@ $(TSV_URL)
