import React, { useEffect, useState } from "react";
import clsx from "clsx";

import { makeStyles } from '@material-ui/styles';
import { Button, Grid, Hidden, Typography } from "@material-ui/core";
import { Page } from "../../components";
import BarChartIcon from "@material-ui/icons/BarChart";
import PropTypes from "prop-types";

import {
  Header,
  TodaysMoney,
  
  // FAQ,
  // PluginsSupport,
  // SourceFiles,
  // UserFlows
} from './components';

import Post from 'src/views/Post'
import { useHistory } from "react-router-dom";

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  container: {
    marginTop: theme.spacing(3)
  },
  summaryButton: {
    backgroundColor: theme.palette.white,
  },
  barChartIcon: {
    marginRight: theme.spacing(1),
  },
  image: {
    width: "100%",
    maxHeight: 400,
  },
}));


const Home = (props) => {
  const { className, ...rest } = props;
  const history = useHistory();
  const classes = useStyles();
  const [user, setUser] = useState({
    sub: "nestor.monroy.90@gmail.com",
    scopes: "ROLE_ADMIN,ROLE_USER",
    first_name: "Nestor",
    last_name: "Monroy",
      
  });

  const handleClick = () => {
    history.push("/post");
  };

  return (
    <div {...rest} className={clsx(classes.root, className)}>
      <Grid alignItems="center" container justify="space-between" spacing={3}>
        <Grid item md={6} xs={12}>
          <Typography component="h2" gutterBottom variant="overline">
            Home
          </Typography>
          <Typography component="h1" gutterBottom variant="h3">
            Hi, {user.first_name.toUpperCase()}{" "}
            {user.last_name.toUpperCase()}
          </Typography>
          <Typography gutterBottom variant="subtitle1">
            Here’s what’s happening with your projects today
          </Typography>
          <Button
            className={classes.summaryButton}
            edge="start"
            variant="contained"
            onClick={handleClick}

          >
            <BarChartIcon className={classes.barChartIcon} />
            View Post
          </Button>
        </Grid>
        <Hidden smDown>
          <Grid item md={6}>
            <img
              alt="Cover"
              className={classes.image}
              src="/images/undraw_growth_analytics_8btt.svg"
            />
          </Grid>
        </Hidden>
      </Grid>
    </div>
  );
};

Home.propTypes = {
  className: PropTypes.string,
};
export default Home;
