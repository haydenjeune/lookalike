import React from 'react';
import './App.css';
import Webcam from 'react-webcam';
import IconButton from '@material-ui/core/IconButton';
import PhotoCamera from '@material-ui/icons/PhotoCamera';
import ReplayIcon from '@material-ui/icons/Replay';

const CapturedPicture = () => {

}

const WebcamCapture = () => {
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
      <>
        <img src={imgSrc} />
        <IconButton color="primary" aria-label="retake picture" component="span" onClick={()=>{setImgSrc("")}}>
          <ReplayIcon fontSize="large"/>
        </IconButton>
      </>
    );
  }

  return (
    <>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={{facingMode: "user"}}
        mirrored={true}
      />
      <IconButton color="primary" aria-label="take picture" component="span" onClick={capture}>
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
