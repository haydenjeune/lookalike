import { makeStyles, createStyles, Theme } from "@material-ui/core/styles";

export const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    app: {
      textAlign: "center",
    },
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
    flexRowCentered: {
      display: "flex",
      flexDirection: "row",
      justifyContent: "center",
    },
    navBottomMargin: {
      marginBottom: "20px"
    }
  })
);
