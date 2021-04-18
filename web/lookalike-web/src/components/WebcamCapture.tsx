import React from "react";
import { useHistory } from "react-router-dom";
import Webcam from "react-webcam";
import IconButton from "@material-ui/core/IconButton";
import PhotoCamera from "@material-ui/icons/PhotoCamera";
import ReplayIcon from "@material-ui/icons/Replay";
import DoneIcon from "@material-ui/icons/Done";

import { useStyles } from "../Styles"; // must be imported last

interface captureProps {
  setFinalImg: React.Dispatch<React.SetStateAction<string>>;
}

export const WebcamCapture = ({ setFinalImg }: captureProps) => {
  const classes = useStyles();
  const webcamRef = React.useRef(null);
  let history = useHistory();

  const [localImg, setLocalImg] = React.useState<string>("");

  const capture = React.useCallback(() => {
    if (webcamRef.current) {
      // TODO: figure out how to do this properly
      setLocalImg((webcamRef.current! as any).getScreenshot());
    }
  }, [webcamRef, setLocalImg]);

  if (localImg !== "") {
    return (
      <>
        <img src={localImg} className={classes.fullwidth} alt="you" />
        <IconButton
          color="secondary"
          className={classes.button}
          aria-label="retake picture"
          component="span"
          onClick={() => {
            setLocalImg("");
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
            setFinalImg(localImg);
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
