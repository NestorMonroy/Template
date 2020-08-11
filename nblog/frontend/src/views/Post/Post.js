import React from 'react';
import { useState, useRef, useEffect } from 'react';
import PostSend from './components/PostSend/PostSend'
import PostList from './components/PostList/PostList'
import PostDetails from './components/PostDetails/PostDetails'
import PostForm from './components/PostForm/PostForm'
import {
    Paper,
    Typography,
    Grid
} from '@material-ui/core';

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

  useEffect(()=>{
    fetch("http://127.0.0.1:8000/api/post/posts/", {
      method: 'GET',
      headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token 6165f2762ac4358af1bdfceab20bb75b15d976d6'
      }
    })
    .then(resp => resp.json())
    .then( resp =>setPost(resp))
    .catch(error => console.log(error))
  }, [])



  // const postClicked = post => {
  //   setSelectedPost(post)
  //   // console.log(post.id)
  // }


  const loadPost = post => {
    setSelectedPost(post);
    setEditedPost(null);

  }

  const editClicked = post => {
    setEditedPost(post);
    setSelectedPost(null);
    // console.log(post.id)
  }

  return (
    <div className={classes.indexpost} >
      {/* <PostSend value={value} /> */}
      <PostForm post={editedPost} />
      <PostDetails post={selectedPost}  updatePost={loadPost}/>
      <Divider className={classes.divider} />
      <PostList posts={posts} postClicked={loadPost}  post={selectedPost} editClicked={editClicked} />
    </div>
  );
}