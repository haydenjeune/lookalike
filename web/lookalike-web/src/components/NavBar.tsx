import React from "react";
import {
  Avatar,
  IconButton,
  Toolbar,
  Typography,
  AppBar,
  Menu,
  MenuItem,
} from "@material-ui/core";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { useStyles } from "../Styles"; // must be imported last

export const NavBar = () => {
  const classes = useStyles();
  return (
    <AppBar className={classes.navBottomMargin} position="static">
      <Toolbar className={classes.flexRowCentered}>
        <Link to="/">
          <img src="/look-a-like.svg" alt="look-a-like" />
        </Link>
      </Toolbar>
    </AppBar>
  );
};
