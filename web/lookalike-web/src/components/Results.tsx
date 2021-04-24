import React from "react";
import { useHistory } from "react-router-dom";
import { Button } from "@material-ui/core";
import ReplayIcon from "@material-ui/icons/Replay";
import Carousel from "react-material-ui-carousel";
import { CelebMatches, findMatches } from "../external/api";
import { getImageSrc } from "../external/celebImages";
import { useStyles } from "../Styles"; // must be imported last

interface MatchProps {
  name: string;
  similarity: number;
  imgSrc: string;
}

function Match({ name, similarity, imgSrc }: MatchProps) {
  return (
    <div style={{ width: "400px" }}>
      <img height="400px" src={imgSrc} />
      <h3>
        {name} ({similarity.toFixed(2)})
      </h3>
    </div>
  );
}

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
      return;
    }

    findMatches(imgSrc.split(",")[1]).then(
      (result) => {
        setMatches(result);
      },
      (error) => {
        alert("Error fetching from matches API");
        history.push("/");
      }
    );
  }, [history, imgSrc]);

  return (
    <>
      <div className={classes.flexRowCentered}>
        <img src={imgSrc} height="400px" alt="you" />
        <Carousel
          autoPlay={false}
          navButtonsAlwaysVisible={true}
          animation="slide"
          timeout={100}
        >
          {matches.map((match, i) => (
            <Match
              key={i}
              name={match.name}
              similarity={match.similarity}
              imgSrc={getImageSrc(match.name)}
            />
          ))}
        </Carousel>
      </div>
      <h2>Don't think any of them look like you?</h2>
      <Button
        color="primary"
        variant="contained"
        aria-label="retake picture"
        component="span"
        onClick={() => {
          history.push("/");
        }}
        startIcon={<ReplayIcon />}
      >
        Try again
      </Button>
    </>
  );
};
