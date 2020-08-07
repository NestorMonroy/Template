import React from 'react';
import { useState, useRef, useEffect } from 'react';

import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';

import {
    Card,
    CardContent,
    Input,
    Tooltip,
    Divider,
    Paper,
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

const useStyles = makeStyles((theme) => ({
    root: {},
    content: {
        display: 'flex',
        alignItems: 'center'
    },
    paper: {
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        whiteSpace: 'nowrap',
        marginBottom: theme.spacing(1),
    },
    input: {
        width: '100%'
    },
    fileInput: {
        display: 'none'
    },

}));


function PostSend(props) {
    const { className, ...rest } = props;
    const classes = useStyles();
    const fileInputRef = useRef(null);
    const [value, setValue] = useState('');
    const handleChange = event => {
        event.persist();

        setValue(event.target.value);
    };
    const handleAttach = () => {
        fileInputRef.current.click();
    };
    return (
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
    )

}
export default PostSend;