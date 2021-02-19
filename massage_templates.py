import datetime
import glob
import os

import jinja2
import numpy
import pandas

from data_ingest import read_data


def main():
    env = jinja2.Environment(
        autoescape=True,
    )
    data = {
        "date": datetime.datetime.utcnow(),
        "pd": pandas,
        "np": numpy,
        "df": read_data(),
    }
    for filename in glob.glob("template/*"):
        out_filename = os.path.join("out", os.path.relpath(filename, "template"))
        with open(filename, "r") as inf:
            tpl: jinja2.Template = env.from_string(inf.read())
            content = tpl.render(data)
        with open(out_filename, "w") as outf:
            outf.write(content)
        print(filename, "=>", out_filename)


if __name__ == "__main__":
    main()
