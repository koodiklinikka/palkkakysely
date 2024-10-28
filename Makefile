YEAR := 2024
DATA_DIR := data/${YEAR}
OUT_DIR := out/${YEAR}
DOCUMENT_ID_FI := 1dvyVEJkn3_osBeKGIlhKmid671jjH7zYgcyH1BjiGF8
DOCUMENT_ID_EN := 1o1uakk1pkoUCtx2OGJhLclxt_uraYA-uK3DH8yCYHN4
XLSX_URL_FI := https://docs.google.com/spreadsheets/d/$(DOCUMENT_ID_FI)/export?format=xlsx
TSV_URL_FI := https://docs.google.com/spreadsheets/d/$(DOCUMENT_ID_FI)/export?format=tsv
XLSX_URL_EN := https://docs.google.com/spreadsheets/d/$(DOCUMENT_ID_EN)/export?format=xlsx
TSV_URL_EN := https://docs.google.com/spreadsheets/d/$(DOCUMENT_ID_EN)/export?format=tsv

export DATA_DIR
export OUT_DIR
export YEAR


all: all-data copy-raw-data massage charts profiling

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

copy-raw-data: all-data $(OUT_DIR)
	cp $(DATA_DIR)/results-en.tsv $(OUT_DIR)/raw-en.tsv
	cp $(DATA_DIR)/results-en.xlsx $(OUT_DIR)/raw-en.xlsx
	cp $(DATA_DIR)/results-fi.tsv $(OUT_DIR)/raw-fi.tsv
	cp $(DATA_DIR)/results-fi.xlsx $(OUT_DIR)/raw-fi.xlsx

massage: all-data
	python -m pulkka.massage_outputs

charts: all-data
	python -m pulkka.generate_charts

profiling: all-data
	python -m pulkka.generate_profiling

# Comment this .PHONY out to not have to download the data every time:
.PHONY: $(DATA_DIR)/results-fi.xlsx $(DATA_DIR)/results-fi.tsv $(DATA_DIR)/results-en.xlsx $(DATA_DIR)/results-en.tsv

all-data: $(DATA_DIR)/results-fi.xlsx $(DATA_DIR)/results-fi.tsv $(DATA_DIR)/results-en.xlsx $(DATA_DIR)/results-en.tsv

$(DATA_DIR):
	mkdir -p $(DATA_DIR)

$(DATA_DIR)/results-en.tsv: $(DATA_DIR)
	curl -fsSL -o $@ $(TSV_URL_EN)

$(DATA_DIR)/results-en.xlsx: $(DATA_DIR)
	curl -fsSL -o $@ $(XLSX_URL_EN)

$(DATA_DIR)/results-fi.tsv: $(DATA_DIR)
	curl -fsSL -o $@ $(TSV_URL_FI)

$(DATA_DIR)/results-fi.xlsx: $(DATA_DIR)
	curl -fsSL -o $@ $(XLSX_URL_FI)
