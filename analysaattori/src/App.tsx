import React from "react";
import "@imc-trading/react-pivottable/pivottable.css";
import {
  PivotTableUI,
  TableRenderers,
  createPlotlyRenderers,
} from "@imc-trading/react-pivottable";
import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js-dist/plotly";
import useSWR from "swr";

const Plot = createPlotlyComponent(Plotly);
const PlotlyRenderers = createPlotlyRenderers(Plot);
const renderers = Object.assign({}, TableRenderers, PlotlyRenderers);

const fetcher = (url: string) => fetch(url).then((res) => res.json());

function App() {
  const qs = new URLSearchParams(window.location.search);
  const url = qs.get("url") || "/palkkakysely/data.json";
  const [pivotState, setPivotState] = React.useState({});
  const dataSwr = useSWR(url, fetcher, { revalidateOnFocus: false });
  if (!dataSwr.data) {
    if (dataSwr.error) {
      return (
        <>
          Virhe ladatessa dataa {url}: {`${dataSwr.error}`}
        </>
      );
    }
    return <>Ladataan {url}...</>;
  }
  return (
    <div>
      <PivotTableUI
        data={dataSwr.data}
        renderers={renderers}
        onChange={setPivotState}
        {...pivotState}
      />
    </div>
  );
}

export default App;
