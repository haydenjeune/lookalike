import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { WebcamCapture } from "./components/WebcamCapture";
import { Results } from "./components/Results";
import { useStyles } from "./Styles"; // must be imported last

function App() {
  const classes = useStyles();
  const [finalImg, setFinalImg] = React.useState<string>("");

  return (
    <div className={classes.app}>
      <div className={classes.container}>
        <Router>
          <Switch>
            <Route path="/" exact>
              <WebcamCapture setFinalImg={setFinalImg} />
            </Route>
            <Route path="/results">
              <Results imgSrc={finalImg} />
            </Route>
          </Switch>
        </Router>
      </div>
    </div>
  );
}

export default App;
