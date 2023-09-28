import base64
import datetime
import glob
import io
import os

import jinja2
import numpy
import pandas

from pulkka import column_maps
from pulkka.config import OUT_DIR, YEAR
from pulkka.data_ingest import read_data

TEMPLATE_DIR = os.path.realpath("./template")


def write_massaged_files(env, df):
    with open(OUT_DIR / "data.html", "w") as f:
        with io.StringIO() as s:
            df.to_html(s, index=False, na_rep="", border=0)
            table_html = s.getvalue()
        f.write(
            env.get_template("_table.html").render(
                table_html=table_html,
                body_class="table-body",
            ),
        )
    with open(OUT_DIR / "data-vertical.html", "w") as f:
        with io.StringIO() as s:
            for _, row in df.iterrows():
                row.dropna().to_frame().to_html(s, header=False, na_rep="", border=0)
                s.write("\n")
            table_html = s.getvalue()
        f.write(
            env.get_template("_table.html").render(
                table_html=table_html,
                body_class="table-body",
            ),
        )
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


def read_asset_to_data_uri(filename, content_type):
    with open(filename, "rb") as f:
        return (
            f"data:{content_type};base64,{base64.b64encode(f.read()).decode('ascii')}"
        )


def main():
    df = read_data()
    env = jinja2.Environment(
        autoescape=True,
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        undefined=jinja2.StrictUndefined,
    )
    env.globals.update(
        {
            "date": datetime.datetime.utcnow(),
            "cm": column_maps,
            "pd": pandas,
            "np": numpy,
            "df": df,
            "year": YEAR,
            "logo_svg": read_asset_to_data_uri(
                os.path.join(TEMPLATE_DIR, "logo.svg"),
                "image/svg+xml",
            ),
            "site_url": f"https://koodiklinikka.github.io/palkkakysely/{YEAR}/",
        },
    )
    render_statics(env)
    write_massaged_files(env, df)


if __name__ == "__main__":
    main()
