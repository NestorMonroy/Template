import React from 'react';
import { makeStyles } from '@material-ui/styles';

import Page from 'src/components/Page';

import { Header, Timeline } from './components';


const useStyles = makeStyles(theme => ({
  root: {},
  inner: {
    width: theme.breakpoints.values.lg,
    maxWidth: '100%',
    margin: '0 auto',
    padding: theme.spacing(3)
  },
  divider: {
    backgroundColor: colors.grey[300]
  },
  content: {
    marginTop: theme.spacing(3)
  }
}));

const Post = props => {
  const { match, history } = props;
  const classes = useStyles();
  const { id, tab } = match.params;

  const handleTabsChange = (event, value) => {
    history.push(value);
  };

  const tabs = [
    { value: 'timeline', label: 'Timeline' },

  ];

  if (!tab) {
    return <Redirect to={`/profile/${id}/timeline`} />;
  }

  if (!tabs.find(t => t.value === tab)) {
    return <Redirect to="/errors/error-404" />;
  }

  return (
    <Page
      className={classes.root}
      title="Post"
    >
      <Header />
      <div className={classes.inner}>
        <Tabs
          onChange={handleTabsChange}
          scrollButtons="auto"
          value={tab}
          variant="scrollable"
        >
          {tabs.map(tab => (
            <Tab
              key={tab.value}
              label={tab.label}
              value={tab.value}
            />
          ))}
        </Tabs>
        <Divider className={classes.divider} />
        <div className={classes.content}>
          {tab === 'timeline' && <Timeline />}

        </div>
      </div>
    </Page>
  );
};

Post.propTypes = {
  history: PropTypes.object.isRequired,
  match: PropTypes.object.isRequired
};

export default Post;
