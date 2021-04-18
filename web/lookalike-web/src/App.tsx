import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";
import { CelebMatches, findMatches } from "./api";
import { WebcamCapture } from "./components/WebcamCapture";
import { useStyles } from "./Styles"; // must be imported last

interface ResultsProps {
  imgSrc: string;
}

const Results = ({ imgSrc }: ResultsProps) => {
  const classes = useStyles();
  let history = useHistory();

  const [matches, setMatches] = React.useState<CelebMatches>([]);
  React.useEffect(() => {
    if (imgSrc === "") {
      history.push("/");
    }

    findMatches(imgSrc.split(",")[1]).then((result) => {
      setMatches(result);
    });
  }, [imgSrc]);

  return (
    <div>
      <img src={imgSrc} width="50%" className={classes.halfwidth} alt="you" />
      {matches.map((result) => (
        <div style={{ verticalAlign: "top", display: "inline-block" }}>
          <img
            width="200px"
            src={encodeURI(
              "https://lookalike-manual.s3-ap-southeast-2.amazonaws.com/" +
                result.name +
                "/0.jpg"
            )}
          />
          <span style={{ display: "block" }}>
            {result.name} ({result.similarity.toFixed(2)})
          </span>
        </div>
      ))}
    </div>
  );
};

function App() {
  const classes = useStyles();
  const [imgSrc, setImgSrc] = React.useState<string>("");

  return (
    <div className="App">
      <div className={classes.container}>
        <Router>
          <Switch>
            <Route path="/" exact>
              <WebcamCapture imgSrc={imgSrc} setImgSrc={setImgSrc} />
            </Route>
            <Route path="/results">
              <Results imgSrc={imgSrc} />
            </Route>
          </Switch>
        </Router>
      </div>
    </div>
  );
}

export default App;
