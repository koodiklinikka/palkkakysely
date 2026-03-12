YEAR := 2025
DATA_DIR := data/${YEAR}
OUT_DIR := out/${YEAR}
PYTHON := python3

export DATA_DIR
export OUT_DIR
export YEAR


all: all-data copy-raw-data massage charts profiling

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

copy-raw-data: all-data $(OUT_DIR)
	cp $(DATA_DIR)/data.tsv $(OUT_DIR)/raw.tsv
	cp $(DATA_DIR)/data.xlsx $(OUT_DIR)/raw.xlsx

massage: all-data
	$(PYTHON) -m pulkka.massage_outputs

charts: all-data
	$(PYTHON) -m pulkka.generate_charts

profiling: all-data
	$(PYTHON) -m pulkka.generate_profiling

all-data: $(DATA_DIR)/data.tsv $(DATA_DIR)/data.xlsx
