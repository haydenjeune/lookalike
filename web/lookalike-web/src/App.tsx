import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";
import { makeStyles, createStyles, Theme } from "@material-ui/core/styles";
import "./App.css";
import { CelebMatches, findMatches } from "./api";
import Webcam from "react-webcam";
import IconButton from "@material-ui/core/IconButton";
import PhotoCamera from "@material-ui/icons/PhotoCamera";
import ReplayIcon from "@material-ui/icons/Replay";
import DoneIcon from "@material-ui/icons/Done";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      maxWidth: "1000px",
      margin: "0 auto",
    },
    button: {
      transform: "translateY(-120%)",
      backgroundColor: "rgba(255, 255, 255, 0.7)",
      "&:hover": {
        backgroundColor: "rgba(255, 255, 255, 0.8)",
      },
      margin: "0px 10px",
    },
    fullwidth: {
      width: "100%",
    },
    halfwidth: {
      width: "50%",
    },
  })
);

interface imgState {
  imgSrc: string;
  setImgSrc: React.Dispatch<React.SetStateAction<string>>;
}

const WebcamCapture = (props: imgState) => {
  const classes = useStyles();
  const webcamRef = React.useRef(null);
  let history = useHistory();

  const [val, setVal] = React.useState<CelebMatches>([]);
  React.useEffect(() => {
    if (props.imgSrc === "") {
      return;
    }

    findMatches(props.imgSrc.split(",")[1]).then((result) => {
      setVal(result);
    });
  }, [props.imgSrc]);

  const capture = React.useCallback(() => {
    if (webcamRef.current) {
      // TODO: figure out how to do this properly
      const imageSrc = (webcamRef.current! as any).getScreenshot();
      props.setImgSrc(imageSrc);
    }
  }, [webcamRef, props.setImgSrc]);

  if (props.imgSrc !== "") {
    return (
      <>
        <img src={props.imgSrc} className={classes.fullwidth} alt="you" />
        <IconButton
          color="secondary"
          className={classes.button}
          aria-label="retake picture"
          component="span"
          onClick={() => {
            props.setImgSrc("");
            setVal([]);
          }}
        >
          <ReplayIcon fontSize="large" />
        </IconButton>
        <IconButton
          color="primary"
          className={classes.button}
          aria-label="accept picture"
          component="span"
          onClick={() => {
            history.push("/results");
          }}
        >
          <DoneIcon fontSize="large" />
        </IconButton>
      </>
    );
  }

  return (
    <>
      <Webcam
        audio={false}
        ref={webcamRef}
        className={classes.fullwidth}
        screenshotFormat="image/jpeg"
        videoConstraints={{ facingMode: "user" }}
        mirrored={true}
        style={{ width: "100%" }}
      />
      <IconButton
        color="primary"
        className={classes.button}
        aria-label="take picture"
        component="span"
        onClick={capture}
      >
        <PhotoCamera fontSize="large" />
      </IconButton>
    </>
  );
};

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
      <img src={imgSrc} width="50%"  className={classes.halfwidth} alt="you" />
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
