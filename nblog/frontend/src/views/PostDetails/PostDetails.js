import React, { useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import {
  Container,
  Paper,
  Tabs,
  Typography,
  Tab,
  Divider,
  colors,
  Grid,
  IconButton,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Button

} from '@material-ui/core';
import axios from 'src/utils/axios';
import StarRateIcon from '@material-ui/icons/StarRate';

import { Page } from 'src/components';
// import { Header, Summary, } from './components';

const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(3)
  },
  tabs: {
    marginTop: theme.spacing(3)
  },
  divider: {
    backgroundColor: colors.grey[300]
  },
  content: {
    marginTop: theme.spacing(3)
  }
}));

function PostDetails(props) {
  const { match, history } = props;
  const classes = useStyles();
  const { id, tab } = match.params;

  const [highlighted, setHighlihted] = useState(-1);

  const highlightRate = high => evt => {
    setHighlihted(high)
  }


  const [openAlert, setOpenAlert] = useState(true);
  const [project, setProject] = useState(null);

  let pos = props.post;
  
  const getDetails = () => {
    fetch(`http://127.0.0.1:8000/api/post/posts/${pos.id}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token 6165f2762ac4358af1bdfceab20bb75b15d976d6'
      },
    })
      .then(resp => resp.json())
      .then(resp => props.updatePost(resp))
      .catch(error => console.log(error))

  }

  const handleTabsChange = (event, value) => {
    history.push(value);
  };

  const tabs = [
    { value: 'summary', label: 'Summary' },


  ];
  if (!tab) {
    //   return <Redirect to={`api/post/posts/${id}/`} />;
  }

  // if (!tabs.find(t => t.value === tab)) {
  //   return <Redirect to="/errors/error-404" />;
  // }

  return (
    <Page
      className={classes.root}
      title="Customer Management Details"
    >
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
                    <Typography>
                      <IconButton className={pos.avg_rating > 0 ? classes.starButton2 : classes.starButton}>
                        <StarRateIcon />
                      </IconButton>
                      <IconButton className={pos.avg_rating > 1 ? classes.starButton2 : classes.starButton}>
                        <StarRateIcon />
                      </IconButton>
                      <IconButton className={pos.avg_rating > 2 ? classes.starButton2 : classes.starButton}>
                        <StarRateIcon />
                      </IconButton>
                      <IconButton className={pos.avg_rating > 3 ? classes.starButton2 : classes.starButton}>
                        <StarRateIcon />
                      </IconButton>
                      <IconButton className={pos.avg_rating > 4 ? classes.starButton2 : classes.starButton}>
                        <StarRateIcon />
                      </IconButton>
                    </Typography>

                    <Typography component="h2" variant="h3" color="textPrimary">
                      ({pos.no_of_ratings})
                                    </Typography>
                  </div>
                  <Divider className={classes.divider} />

                  <Typography component="h2" variant="subtitle1" align="center">
                    Rate it
                                </Typography>
                  {[...Array(5)].map((e, i) => {
                    return <IconButton key={i} className={highlighted > i - 1 ? classes.rateButton1 : classes.rateButton}
                      onMouseEnter={highlightRate(i)}
                      onMouseLeave={highlightRate(-1)}
                      onClick={console.log(i)}
                    >
                      <StarRateIcon />
                    </IconButton>
                  })}
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

    </Page>
  );
};

PostDetails.propTypes = {
  history: PropTypes.object.isRequired,
  match: PropTypes.object.isRequired
};

export default PostDetails;
