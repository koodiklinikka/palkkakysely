import datetime
import glob
import io
import os

import jinja2
import numpy
import pandas

from pulkka.config import OUT_DIR, YEAR
from pulkka.data_ingest import read_data

TEMPLATE_DIR = os.path.realpath("./template")


def write_massaged_files(env, df):
    with open(OUT_DIR / 'data.html', 'w') as f:
        with io.StringIO() as s:
            df.to_html(s, index=False, na_rep="", border=0)
            table_html = s.getvalue()
        f.write(env.get_template('_table.html').render(table_html=table_html, body_class="table-body"))
    df.to_csv(OUT_DIR / "data.csv", index=False)
    df.to_excel(OUT_DIR / "data.xlsx", index=False)
    df.to_json(
        OUT_DIR / "data.json",
        orient="records",
        date_format="iso",
        force_ascii=False,
    )
    print("Wrote data files")


def render_statics(env):
    for filename in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        basename = os.path.relpath(filename, TEMPLATE_DIR)
        if basename.startswith("_"):
            continue
        out_filename = OUT_DIR / basename
        with open(filename, "r") as inf:
            tpl: jinja2.Template = env.from_string(inf.read())
            content = tpl.render(body_class="static-body")
        with open(out_filename, "w") as outf:
            outf.write(content)
        print(filename, "=>", out_filename)


def main():
    df = read_data()
    env = jinja2.Environment(
        autoescape=True,
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
    )
    env.globals.update({
        "date": datetime.datetime.utcnow(),
        "pd": pandas,
        "np": numpy,
        "df": df,
        "year": YEAR,
    })
    render_statics(env)
    write_massaged_files(env, df)


if __name__ == "__main__":
    main()
