import React from "react";
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
    image: {
      width: "100%",
    },
  })
);

const WebcamCapture = () => {
  const classes = useStyles();
  const webcamRef = React.useRef(null);
  const [imgSrc, setImgSrc] = React.useState<string>("");

  const [val, setVal] = React.useState<CelebMatches>([]);
  React.useEffect(() => {
    if (imgSrc === "") {
      return;
    }

    findMatches(imgSrc.split(",")[1]).then((result) => {
      setVal(result);
    });
  }, [imgSrc]);

  const capture = React.useCallback(() => {
    if (webcamRef.current) {
      // TODO: figure out how to do this properly
      const imageSrc = (webcamRef.current! as any).getScreenshot();
      setImgSrc(imageSrc);
    }
  }, [webcamRef, setImgSrc]);

  if (imgSrc !== "") {
    return (
      <>
        <img src={imgSrc} className={classes.image} alt="you" />
        <IconButton
          color="secondary"
          className={classes.button}
          aria-label="retake picture"
          component="span"
          onClick={() => {
            setImgSrc("");
          }}
        >
          <ReplayIcon fontSize="large" />
        </IconButton>
        <IconButton
          color="primary"
          className={classes.button}
          aria-label="accept picture"
          component="span"
        >
          <DoneIcon fontSize="large" />
        </IconButton>
        <div>
          {val.map((result) => (
            <div>
              <img src={result.image} />
              <span>
                {result.name} ({result.similarity})
              </span>
            </div>
          ))}
        </div>
      </>
    );
  }

  return (
    <>
      <Webcam
        audio={false}
        ref={webcamRef}
        className={classes.image}
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

function App() {
  const classes = useStyles();

  return (
    <div className="App">
      <div className={classes.container}>
        <WebcamCapture />
      </div>
    </div>
  );
}

export default App;
