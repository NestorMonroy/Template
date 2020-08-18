import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import moment from 'moment';
import { makeStyles } from '@material-ui/styles';
import {
  Avatar,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  Typography
} from '@material-ui/core';

import getInitials from 'src/utils/getInitials';
import { Label } from 'src/components';

const useStyles = makeStyles(theme => ({
  root: {},
  header: {
    paddingBottom: 0
  },
  content: {
    paddingTop: 0
  },
  listItem: {
    padding: theme.spacing(2, 0),
    justifyContent: 'space-between'
  }
}));

const Holder = props => {
  const { posts, className, ...rest } = props;

  const classes = useStyles();

  return (
    <Card
      {...rest}
      className={clsx(classes.root, className)}
    >
      <CardHeader
        avatar={
          <Avatar
            alt="Author"
            className={classes.avatar}
            component={RouterLink}
           
            to="/profile/1/timeline"
          >
            {getInitials(posts.user.first_name)}
          </Avatar>
        }
        className={classes.header}
        disableTypography
        subheader={
          <Typography
            component={RouterLink}
            to="/profile/1/timeline"
            variant="h5"
          >
            {posts.user.last_name}
          </Typography>
        }
        title={
          <Typography
            display="block"
            variant="overline"
          >
            Contest holder
          </Typography>
        }
      />
      <CardContent className={classes.content}>
        <List>
          <ListItem
            className={classes.listItem}
            disableGutters
            divider
          >
            <Typography variant="subtitle2">Deadline</Typography>
            <Typography variant="h6">
              {moment(posts.timestamp).format('DD MMM YYYY')}
            </Typography>
          </ListItem>
          <ListItem
            className={classes.listItem}
            disableGutters
            divider
          >
            <Typography variant="subtitle2">Per Project</Typography>
            <Typography variant="h6">
             
            </Typography>
          </ListItem>
          <ListItem
            className={classes.listItem}
            disableGutters
            divider
          >
            <Typography variant="subtitle2">Main Technology</Typography>
            
          </ListItem>
          <ListItem
            className={classes.listItem}
            disableGutters
            divider
          >
            <Typography variant="subtitle2">Last Update</Typography>
            <Typography variant="h6">
              {moment(posts.timestamp).format('DD MMM YYYY')}
            </Typography>
          </ListItem>
        </List>
      </CardContent>
    </Card>
  );
};

Holder.propTypes = {
  className: PropTypes.string,
  posts: PropTypes.object.isRequired
};

export default Holder;
