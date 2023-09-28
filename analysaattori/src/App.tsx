import React from "react";
import PivotTableUI from "react-pivottable/PivotTableUI";
import "react-pivottable/pivottable.css";
import TableRenderers from "react-pivottable/TableRenderers";
import createPlotlyComponent from "react-plotly.js/factory";
import createPlotlyRenderers from "react-pivottable/PlotlyRenderers";
import useSWR from "swr/esm";

const Plot = createPlotlyComponent(window.Plotly);
const PlotlyRenderers = createPlotlyRenderers(Plot);
const renderers = Object.assign({}, TableRenderers, PlotlyRenderers);

function App() {
  const qs = new URLSearchParams(window.location.search);
  const [pivotState, setPivotState] = React.useState({});
  const dataSwr = useSWR(qs.get("url") || "/palkkakysely/data.json");
  if (!dataSwr.data) {
    if (dataSwr.error) {
      return <>Virhe ladatessa dataa: {`${dataSwr.error}`}</>;
    }
    return <>Ladataan...</>;
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
