import React, { useEffect, useState } from 'react';
import makeStyles from '@material-ui/core/styles/makeStyles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import ButtonBase from '@material-ui/core/ButtonBase';
import Typography from '@material-ui/core/Typography';
import AddShoppingCartIcon from '@material-ui/icons/AddShoppingCart';
import { useDispatch } from 'react-redux';

// import { loadPost } from '../lookup'

const useStyles = makeStyles((theme) => ({
    root: {
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: theme.spacing(6, 2)
    },
    paper: {
        padding: theme.spacing(2),
        margin: 'auto',
        maxWidth: 500
    },
    image: {
        width: 128,
        height: 128
    },
    img: {
        margin: 'auto',
        display: 'block',
        maxWidth: '100%',
        maxHeight: '100%'
    }
}));


export function PostsDetails(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Paper className={classes.paper}>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm container>
                        <Grid item xs container direction="column" spacing={2}>
                            <Grid item xs>
                                return (
                                    <Typography variant="subtitle1"> 
                                        {props.post}
                                    </Typography>
									);
							</Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
        </div>
    );
}


