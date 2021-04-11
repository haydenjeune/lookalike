import React from 'react';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import './App.css';
import Webcam from 'react-webcam';
import IconButton from '@material-ui/core/IconButton';
import PhotoCamera from '@material-ui/icons/PhotoCamera';
import ReplayIcon from '@material-ui/icons/Replay';
import DoneIcon from '@material-ui/icons/Done';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    button: {
      transform: "translateY(-120%)",
      backgroundColor: "rgba(255, 255, 255, 0.7)",
      '&:hover': {
        backgroundColor: "rgba(255, 255, 255, 0.8)",
      },
      margin: "0px 10px"
    },
    image: {
      width: "100%"
    },
  }),
);

const WebcamCapture = () => {
  const classes = useStyles();
  const webcamRef = React.useRef(null);
  const [imgSrc, setImgSrc] = React.useState<string>("");
  const [photoTaken, setPhotoTaken] = React.useState<boolean>(false);

  const capture = React.useCallback(() => {
    if (webcamRef.current) {
      // TODO: figure out how to do this properly
      const imageSrc = (webcamRef.current! as any).getScreenshot();
      setImgSrc(imageSrc);
    }
  }, [webcamRef, setImgSrc]);

  if (imgSrc !== "") {
    return (
      <div>
        <img 
          src={imgSrc}
          className={classes.image}
        />
        <IconButton 
          color="secondary"
          className={classes.button}
          aria-label="retake picture"
          component="span"
          onClick={()=>{setImgSrc("")}}
        >
          <ReplayIcon fontSize="large"/>
        </IconButton>
        <IconButton 
          color="primary"
          className={classes.button}
          aria-label="accept picture"
          component="span"
        >
          <DoneIcon fontSize="large"/>
        </IconButton>
      </div>
    );
  }

  return (
    <>
      <Webcam
        audio={false}
        ref={webcamRef}
        className={classes.image}
        screenshotFormat="image/jpeg"
        videoConstraints={{facingMode: "user"}}
        mirrored={true}
        style={{width: "100%"}}
      />
      <IconButton 
        color="primary"
        className={classes.button}
        aria-label="take picture"
        component="span"
        onClick={capture}
      >
          <PhotoCamera fontSize="large"/>
      </IconButton>
    </>
  );
};

function App() {
  return (
    <div className="App">
      <WebcamCapture />
    </div>
  );
}

export default App;
