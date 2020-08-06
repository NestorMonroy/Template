import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';
import { Page } from "../../components";

import {
  Header,
  TodaysMoney,
  // FAQ,
  // PluginsSupport,
  // SourceFiles,
  // UserFlows
} from './components';

import PostsList from 'src/views/Post'

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  container: {
    marginTop: theme.spacing(3)
  }
}));


const Home = () => {
  const classes = useStyles();

  return (
    <Page
      className={classes.root}
      title="Presentación"
    >
      <PostsList />
      {/* <Header /> */}
      {/* <Grid
        className={classes.container}
        container
        spacing={3}
      >
        <Grid
          item
          xs={12}
        > 
          <PostsList />
        </Grid>
      </Grid> */}
    </Page>
  );
};

export default Home;
