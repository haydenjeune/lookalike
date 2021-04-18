import React from "react";
import { useHistory } from "react-router-dom";
import IconButton from "@material-ui/core/IconButton";
import ReplayIcon from "@material-ui/icons/Replay";
import { CelebMatches, findMatches } from "../api";
import { useStyles } from "../Styles"; // must be imported last

interface ResultsProps {
  imgSrc: string;
}

export const Results = ({ imgSrc }: ResultsProps) => {
  const classes = useStyles();
  let history = useHistory();

  const [matches, setMatches] = React.useState<CelebMatches>([]);
  React.useEffect(() => {
    if (imgSrc === "") {
      // redirect to capture page if there's no image
      history.push("/");
    }

    findMatches(imgSrc.split(",")[1]).then((result) => {
      setMatches(result);
    });
  }, [history, imgSrc]);

  return (
    <div>
      <img src={imgSrc} width="50%" className={classes.halfwidth} alt="you" />
      <IconButton
        color="primary"
        aria-label="retake picture"
        component="span"
        onClick={() => {
          history.push("/");
        }}
      >
        <ReplayIcon fontSize="large" />
      </IconButton>
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
