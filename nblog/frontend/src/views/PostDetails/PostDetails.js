import React, { useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import {
  Container,
  Paper,
  Tabs,
  Typography,
  Tab,
  Divider,
  colors,
  Grid,
  IconButton,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Button

} from '@material-ui/core';
import axios from 'axios';
import StarRateIcon from '@material-ui/icons/StarRate';

import { Page } from 'src/components';
import { Header, Overview } from './components';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  tabs: {
    marginTop: theme.spacing(3)
  },
  divider: {
    backgroundColor: colors.grey[300]
  },
  content: {
    marginTop: theme.spacing(3)
  }
}));

function PostDetails(props) {
  const { match, history } = props;
  const classes = useStyles();
  const { id, tab } = match.params;

  const [highlighted, setHighlihted] = useState(-1);

  const highlightRate = high => evt => {
    setHighlihted(high)
  }


  const [openAlert, setOpenAlert] = useState(true);
  const [posts, setPosts] = useState(null);



  useEffect(() => {

    axios.get(`http://127.0.0.1:8000/api/post/posts/${id}/`)
      .then(response => {
        setPosts(response.data);
        // console.log(response)
      })
      .catch(error => console.log(error))
  }, []);

  const [mode, setMode] = useState('grid');
  const handleTabsChange = (event, value) => {
    history.push(value);
  };

  //let post = props.post;

  console.log(posts)
  const tabs = [
    { value: 'overview', label: 'Overview' },
    { value: 'files', label: 'Files' },
    { value: 'activity', label: 'Activity' },
    { value: 'subscribers', label: 'Subscribers' }


  ];

  if (!tab) {
    return <Redirect to={`/post/${id}/overview`} />;
  }

  if (!tabs.find(t => t.value === tab)) {
    return <Redirect to="/errors/error-404" />;
  }

  if (!posts) {
    return null;
  }

  return (
    <Page
      className={classes.root}
      title="Detalle de Post"
    >
      <Header posts={posts} />
      <Tabs
        className={classes.tabs}
        onChange={handleTabsChange}
        scrollButtons="auto"
        value={tab}
        variant="scrollable"
      >
        {tabs.map(tab => (
          <Tab
            key={tab.value}
            label={tab.label}
            value={tab.value}
          />
        ))}
      </Tabs>
      <Divider className={classes.divider} />
      <div className={classes.content}>
        {tab === 'overview' && <Overview posts={posts} />}
      </div>
    </Page>
  );
};

PostDetails.propTypes = {
  history: PropTypes.object.isRequired,
  match: PropTypes.object.isRequired
};

export default PostDetails;
