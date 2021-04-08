// @flow
import React from 'react';
import {BrowserRouter as Router, Link, Route, Switch} from 'react-router-dom';
import {connect} from "react-redux";

import {logout} from "./actions/authActions";

import {useStyles} from './config/styles';
import {useMobileView} from './components/helpers';
import {createMuiTheme, ThemeProvider} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import {PrivateRoute} from "./components/privateRoute";
import UserLoginWithRedux from "./pages/userLogin";
import PublicPage from "./pages/publicPage";
import ProtectedPageWithRedux from "./pages/protectedPage";
import CssBaseline from "@material-ui/core/CssBaseline";

const theme = createMuiTheme({
  palette: {
    background: {
      default: '#f8f8f8'
    },
    primary: {
      main: '#6838F2'
    }
  }
})

const App = (props) => {
  const isMobile = useMobileView();
  const classes = useStyles({isMobile});

  const handleLogout = () => {
      props.dispatch(logout())
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline/>
      <Router>
      <AppBar position='sticky'>
        <Toolbar>
          <Link to={'/'} className={classes.link}>
            <Typography variant={'h6'}>Public</Typography>
          </Link>
          <Link to={'/protected'} className={classes.link}>
            <Typography variant={'h6'}>Protected</Typography>
          </Link>
          {props.auth.isAuthenticated ?
            <Button color="inherit" onClick={handleLogout}>Logout</Button>
            :
            <Link to={'/login'} className={classes.link}>
              <Typography variant={'h6'}>Login</Typography>
            </Link>
          }
        </Toolbar>
      </AppBar>
      <div>
        <Switch>
          <Route path="/login">
            <UserLoginWithRedux/>
          </Route>
          <PrivateRoute path="/protected">
            <ProtectedPageWithRedux/>
          </PrivateRoute>
          <Route path="/">
            <PublicPage/>
          </Route>
        </Switch>
      </div>
    </Router>
    </ThemeProvider>
  );
}

const AppPropsFactory = (state: Object) => ({
  auth: state.auth
});

const StoreApp = connect(AppPropsFactory)(App);
export default StoreApp
