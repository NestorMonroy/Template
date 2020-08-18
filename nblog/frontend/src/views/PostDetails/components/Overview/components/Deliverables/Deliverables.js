import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/styles';
import { Card, CardContent, Typography } from '@material-ui/core';

const useStyles = makeStyles(() => ({
  root: {}
}));

const Deliverables = props => {
  const {posts, className, ...rest } = props;

  const classes = useStyles();

  return (
    <Card
      {...rest}
      className={clsx(classes.root, className)}
    >
      <CardContent>
        <Typography variant="h4">Deliverables:</Typography>
        <Typography variant="body1">
          f
        </Typography>
      </CardContent>
    </Card>
  );
};

Deliverables.propTypes = {
  className: PropTypes.string
};

export default Deliverables;
