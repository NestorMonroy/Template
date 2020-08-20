import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';

import { Content, Deliverables, Holder } from './components';
import { postService } from "src/services/postService";

const useStyles = makeStyles(theme => ({
  root: {},
  deliverables: {
    marginTop: theme.spacing(3)
  },
  members: {
    marginTop: theme.spacing(3)
  }
}));

const Overview = props => {
  const { updateClicked, className, ...rest } = props;
  



  // useEffect(() => {
  //   postService
  //     .findAll()
  //     .then(posts => setPosts())
  //   console.log('n')
  // }, []);

  const classes = useStyles();
  return (
    <Grid


      container
      spacing={3}
    >
      <Grid
        item
        lg={8}
        xl={9}
        xs={12}
      >

      </Grid>
      <Grid
        item
        lg={4}
        xl={3}
        xs={12}
      >



      </Grid>
    </Grid>
  );
};

Overview.propTypes = {
  className: PropTypes.string,
  //posts: PropTypes.object.isRequired
};

export default Overview;
