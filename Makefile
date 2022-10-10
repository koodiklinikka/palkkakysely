DATA_DIR := data/2022
OUT_DIR := out/2022
YEAR := 2022
XLSX_URL :=  https://docs.google.com/spreadsheets/d/1PxBV-MzFlPl1IxOp6EGj6C80HSTgfHcXUhBeL8hZ0Ck/export?format=xlsx
TSV_URL := https://docs.google.com/spreadsheets/d/1PxBV-MzFlPl1IxOp6EGj6C80HSTgfHcXUhBeL8hZ0Ck/export?format=tsv

export DATA_DIR
export OUT_DIR
export YEAR

.PHONY: $(DATA_DIR)/results.xlsx $(DATA_DIR)/results.tsv

all: all-data copy-raw-data massage charts profiling

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

copy-raw-data: all-data $(OUT_DIR)
	cp $(DATA_DIR)/results.xlsx $(OUT_DIR)/raw.xlsx
	cp $(DATA_DIR)/results.tsv $(OUT_DIR)/raw.tsv

massage: all-data
	python -m pulkka.massage_outputs

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
