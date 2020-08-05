import React from 'react';
import { makeStyles } from '@material-ui/styles';

import { Page } from "../../components";

import {
  Header,
  // FAQ,
  // PluginsSupport,
  // SourceFiles,
  // UserFlows
} from './components';


const useStyles = makeStyles(() => ({
  root: {}
}));

const HPresentation = () => {
  const classes = useStyles();

  return (
    <Page
      className={classes.root}
      title="Presentación"
    >
      <Header />

    </Page>
  );
};

export default HPresentation;
