import React from 'react';
import { useState, useRef, useEffect } from 'react';

import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';

import {
  Card,
  CardContent,
  Divider,
  Input,
  Paper,
  Tooltip,
  Typography,
  Grid
} from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import SendIcon from '@material-ui/icons/Send';
import AddPhotoIcon from '@material-ui/icons/AddPhotoAlternate';
import AttachFileIcon from '@material-ui/icons/AttachFile';

import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import PostList from './components/PostList/PostList'

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

export default function PostsList(props) {
  const { className, ...rest } = props;

  const classes = useStyles();
  const fileInputRef = useRef(null);
  const [value, setValue] = useState('');

  const [posts, setPost] = useState([])

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

  const handleChange = event => {
    event.persist();

    setValue(event.target.value);
  };
  const handleAttach = () => {
    fileInputRef.current.click();
  };

  return (
    <div className={classes.indexpost} >
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card
            {...rest}
            className={clsx(classes.root, className)}
          >
            <CardContent className={classes.content}>
              <Paper
                className={classes.paper}
                elevation={1}
              >
                <Input
                  className={classes.input}
                  disableUnderline
                  onChange={handleChange}
                  placeholder={`What's on your mind, N`}
                />
              </Paper>
              <Tooltip title="Send">
                <IconButton color={value.length > 0 ? 'primary' : 'default'}>
                  <SendIcon />
                </IconButton>
              </Tooltip>
              <Divider className={classes.divider} />
              <Tooltip title="Attach image">
                <IconButton
                  edge="end"
                  onClick={handleAttach}
                >
                  <AddPhotoIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Attach file">
                <IconButton
                  edge="end"
                  onClick={handleAttach}
                >
                  <AttachFileIcon />
                </IconButton>
              </Tooltip>
              <input
                className={classes.fileInput}
                ref={fileInputRef}
                type="file"
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Divider className={classes.divider} />

      <PostList posts={posts} />

      {posts.map(post => {
        return <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper className={classes.paper}>
              <Typography
                component="h1"
                variant="h3"
              >
                {post.content}
          </Typography>
            </Paper>
          </Grid>
        </Grid>
      })}

    </div>
  );
}