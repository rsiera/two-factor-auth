// @flow
import makeStyles from '@material-ui/core/styles/makeStyles';

const useStyles: ((Object) => Object) = makeStyles(theme => ({
  container: {
    position: 'relative',
    width: '100vw',
    height: '100vh',
    '& > .MuiGrid-root': {
      height: ({isMobile}) => isMobile ? 'auto' : '100%',
    },
    '& a:hover': {
      textDecoration: 'none'
    },
    background: theme.palette.background.light
  },
  right: {
    padding: ({isMobile}) => isMobile ? '1rem 3rem 1rem 1rem' : '30px 45px 40px 50px',
  },
  label: {
    color: '#3b327a',
  },
  headerMargin: {
    margin: `${theme.spacing(2.25)}px 0 ${theme.spacing(0.75)}px`,
  },
  input: {
    background: theme.palette.common.white
  },
  link: {
    color: '#FFFFFF',
    paddingRight: theme.spacing(1),
  }
}));

export {useStyles};
