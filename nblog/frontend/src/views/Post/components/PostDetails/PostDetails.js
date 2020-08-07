import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import StarRateIcon from '@material-ui/icons/StarRate';
// import StarOutlineIcon from '@material-ui/icons/StarOutline';

import {
    Container,
    Paper,
    Typography,
    Grid,
    IconButton,
    Divider,
    Card,
    CardActions,
    CardContent,
    CardHeader,
    Button

} from '@material-ui/core';
import StarIcon from '@material-ui/icons/StarBorder';

const useStyles = makeStyles((theme) => ({
    root: {},
    content: {
        display: 'flex',
        alignItems: 'center'
    },
    cardHeader: {
        backgroundColor:
            theme.palette.type === 'light' ? theme.palette.grey[200] : theme.palette.grey[700],
    },
    cardPricing: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'baseline',
        marginBottom: theme.spacing(2),
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
    options: {
        lineHeight: '5px'
    },
    starButton: {
        // display: 'none',
        // color: 'orange',
        marginLeft: theme.spacing(1)
    },
    starButton2: {
        // display: 'none',
        color: 'orange',
        marginLeft: theme.spacing(1)
    },
    divider: {
        margin: theme.spacing(2, 0),
    },
}));


function PostDetails(props) {
    const { className, } = props;
    const classes = useStyles();

    const pos = props.post;

    return (
        <Container maxWidth="md" component="main">
            <Grid container spacing={2} alignItems="flex-end">
                {pos ? (
                    <Grid item xs={12}>
                        <Card>
                            <CardHeader
                                title={pos.content}
                                titleTypographyProps={{ align: 'center' }}
                                subheaderTypographyProps={{ align: 'center' }}
                                className={classes.cardHeader}
                            />
                            <CardContent>
                                <div className={classes.cardPricing}>
                                    <Typography component="h2" variant="h3" color="textPrimary">
                                        ${pos.no_of_ratings}
                                    </Typography>
                                    <Typography variant="h6" color="textSecondary">
                                        {pos.content}
                                    </Typography>
                                </div>
                                <ul>
                                    {/* {tier.description.map((line) => (
                                        <Typography component="li" variant="subtitle1" align="center" key={line}>
                                            {line}
                                        </Typography>
                                    ))} */}
                                </ul>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth color="primary">

                                </Button>
                            </CardActions>
                        </Card>
                    </Grid>
                ) : null}
            </Grid>
        </Container>
    )
}
export default PostDetails;