import React from "react";
import { useHistory } from "react-router-dom";
import Webcam from "react-webcam";
import IconButton from "@material-ui/core/IconButton";
import PhotoCamera from "@material-ui/icons/PhotoCamera";
import ReplayIcon from "@material-ui/icons/Replay";
import DoneIcon from "@material-ui/icons/Done";

import { useStyles } from "../Styles"; // must be imported last

interface captureProps {
  imgSrc: string;
  setImgSrc: React.Dispatch<React.SetStateAction<string>>;
}

export const WebcamCapture = ({ imgSrc, setImgSrc }: captureProps) => {
  const classes = useStyles();
  const webcamRef = React.useRef(null);
  let history = useHistory();

  React.useEffect(() => {
    if (imgSrc === "") {
      return;
    }
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
        <img src={imgSrc} className={classes.fullwidth} alt="you" />
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
