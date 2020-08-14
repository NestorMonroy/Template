import React from 'react';
import { Redirect } from 'react-router-dom';

import { useState, useRef, useEffect } from 'react';
import PostSend from './components/PostSend/PostSend'
import PostList from './components/PostList/PostList'
import PostDetails from './components/PostDetails/PostDetails'
import PostForm from './components/PostForm/PostForm'
import {
  Paper,
  Typography,
  Grid,
  Container

} from '@material-ui/core';
import Header from "./components/Header";

import { Divider } from '@material-ui/core';

import { makeStyles } from '@material-ui/styles';

const useStyles = makeStyles((theme) => ({
  root: {},
  content: {
    display: 'flex',
    alignItems: 'center'
  },
  input: {
    width: '100%'
  },
  fileInput: {
    display: 'none'
  },
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(12, 1fr)',
    gridGap: theme.spacing(3),
  },
  paper: {
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
    whiteSpace: 'nowrap',
    marginBottom: theme.spacing(1),
  },
  divider: {
    margin: theme.spacing(2, 0),
  },
}));

export default function Post(props) {
  const { className, ...rest } = props;

  const classes = useStyles();
  const fileInputRef = useRef(null);
  const [value, setValue] = useState('');

  const [posts, setPost] = useState([])
  const [selectedPost, setSelectedPost] = useState([null])
  const [editedPost, setEditedPost] = useState([null])

  const { match, history } = props;
  const { tab } = match.params;

  const handleTabsChange = (event, value) => {
    history.push(value);
  };

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/post/posts/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token 6165f2762ac4358af1bdfceab20bb75b15d976d6'
      }
    })
      .then(resp => resp.json())
      .then(resp => setPost(resp))
      .catch(error => console.log(error))
  }, [])

  const loadPost = post => {
    setSelectedPost(post);
    setEditedPost(null);

  }

  const editClicked = post => {
    setEditedPost(post);
    setSelectedPost(null);
    // console.log(post.id)
  }


  // const tabs = [
  //   { value: 'general', label: 'General' },
  //   { value: 'subscription', label: 'Subscription' },
  //   { value: 'notifications', label: 'Notifications' },
  //   { value: 'security', label: 'Security' }
  // ];

  // if (!tab) {
  //   return <Redirect to="/settings/general" />;
  // }

  // if (!tabs.find(t => t.value === tab)) {
  //   return <Redirect to="/errors/error-404" />;
  // }



  return (
    
    <Container>
      {/* <Header></Header> */}
      <PostList posts={posts} postClicked={loadPost} post={selectedPost} editClicked={editClicked} />

    </Container>
  );
}