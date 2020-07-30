/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import { Button, TextField } from '@material-ui/core';
import { useForm } from 'react-hook-form';


const useStyles = makeStyles((theme) => ({
  root: {},
  fields: {
    margin: theme.spacing(-1),
    display: 'flex',
    flexWrap: 'wrap',
    '& > *': {
      flexGrow: 1,
      margin: theme.spacing(1)
    }
  },
  submitButton: {
    marginTop: theme.spacing(2),
    width: '100%'
  }
}));

function NewLoginForm({ className, onLogin, ...rest }) {
  const classes = useStyles();
  const { register, errors, handleSubmit } = useForm();

  const handleLogin = (data) => {
    const { username, password } = data;
    onLogin(username, password);
  };

  return (
    <form onSubmit={handleSubmit(handleLogin)}
          {...rest}
          className={clsx(classes.root, className)}>
      <div className={classes.fields}>
        <TextField
          error={Boolean(errors.username)}
          fullWidth
          helperText={errors.username ? errors.username.message : null}
          label="Username"
          name="username"
          variant="outlined"
          inputRef={register({
            required: 'Username is required'
          })}
        />
        <TextField
          error={Boolean(errors.password)}
          fullWidth
          helperText={errors.password ? errors.password.message : null}
          label="Password"
          name="password"
          type="password"
          variant="outlined"
          inputRef={register({
            required: 'Password is required'
          })}
        />
      </div>
      <Button
        className={classes.submitButton}
        color="secondary"
        size="large"
        type="submit"
        variant="contained">
        Sign in
      </Button>
    </form>
  );
}

NewLoginForm.propTypes = {
  className: PropTypes.string,
  onLogin: PropTypes.func
};

export default NewLoginForm;
