import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogActions from '@material-ui/core/DialogActions';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import PropTypes from 'prop-types';

function DeleteConfirmationDialog({ open, onCancel, onOk }) {

  return (
    <div>
      <Dialog
        open={open}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{'Are you sure you want to delete?'}</DialogTitle>
        <DialogActions>
          <Grid>
            <Grid container spacing={2}>
              <Grid item s={6}>
                <Button onClick={onCancel} color="primary">
                  Cancel
                </Button>
              </Grid>
              <Grid item s={6}>
                <Button onClick={onOk} color="primary" variant={'contained'}>
                  Ok
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </DialogActions>
      </Dialog>
    </div>
  );
}

DeleteConfirmationDialog.propTypes = {
  open: PropTypes.bool,
  onCancel: PropTypes.func,
  onOk: PropTypes.func
};

export default DeleteConfirmationDialog;
