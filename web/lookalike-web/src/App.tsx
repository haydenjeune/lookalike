import React from "react";
import {
  Avatar,
  IconButton,
  Toolbar,
  Typography,
  AppBar,
  Menu,
  MenuItem,
} from "@material-ui/core";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { WebcamCapture } from "./components/WebcamCapture";
import { Results } from "./components/Results";
import { NavBar } from "./components/NavBar";
import { useStyles } from "./Styles"; // must be imported last

const App = () => {
  const classes = useStyles();
  const [finalImg, setFinalImg] = React.useState<string>("");

  return (
    <div className={classes.app}>
        <Router>
          <header>
            <NavBar />
          </header>
      <div className={classes.container}>
          <Switch>
            <Route path="/" exact>
              <WebcamCapture setFinalImg={setFinalImg} />
            </Route>
            <Route path="/results">
              <Results imgSrc={finalImg} />
            </Route>
          </Switch>
      </div>
        </Router>
    </div>
  );
}

export default App;
