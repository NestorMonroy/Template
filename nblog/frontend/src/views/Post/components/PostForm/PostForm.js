import React, { useState, useRef } from 'react';
import clsx from 'clsx';

import {
    Container,
    Grid,
    Card,
    CardActions,
    CardContent,
    Divider,
    Typography,

    TextareaAutosize,
    Tooltip,
    Paper,
    Input,
    IconButton,

} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import SendIcon from '@material-ui/icons/Send';
import AddPhotoIcon from '@material-ui/icons/AddPhotoAlternate';
import AttachFileIcon from '@material-ui/icons/AttachFile';


const useStyles = makeStyles((theme) => ({
    root: {},
    content: {
        display: 'flex',
        alignItems: 'center'
    },
    cardHeader: {

    },
    paper: {
        flexGrow: 1,
        padding: theme.spacing(0.5, 2)
    },

}));


function PostForm(props) {
    const classes = useStyles();
    const { className, } = props;
    const [value, setValue] = useState('');
    // const session = useSelector((state) => state.session);

    const fileInputRef = useRef(null);

    const handleChange = (event) => {
        event.persist();
        setValue(event.target.value);
    };


    const handleAttach = () => {
        fileInputRef.current.click();
    };


    return (
        <Container maxWidth="md" component="main">
            <Grid container spacing={2} alignItems="flex-end">
                <Grid item xs={12}>

                    <Card
                        className={classes.root}
                    // className={clsx(classes.root, className)}
                    >
                        <CardContent className={classes.content}>
                            {props.post ? (
                                <React.Fragment>

                                    <Paper
                                        className={classes.paper}
                                        elevation={1}
                                    >
                                        <Input
                                            className={classes.input}
                                            disableUnderline
                                            onChange={handleChange}
                                            placeholder=  {props.content &&  props.content.id}
                                        />
                                      
                                    </Paper>
                                    <Tooltip title="Send">
                                        <IconButton color={value.length > 0 ? 'primary' : 'default'}>
                                            <SendIcon />
                                        </IconButton>
                                    </Tooltip>


                                </React.Fragment>
                            ) : null}

                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Container>

    )
}

export default PostForm;



{/* <Card>
<CardContent>
    <Typography paragraph>
        <TextareaAutosize aria-label="empty textarea" placeholder="Empty" />
        {props.post.content} edit
    </Typography>
</CardContent>
</Card> */}


