// @flow
import React, {useEffect} from 'react';
import {useDispatch, useSelector} from "react-redux";
import {loginUserSuccess, logout} from "../actions/authActions";
import {Redirect, Route} from "react-router-dom";
import {verifyToken} from "../services/authService";

export const PrivateRoute = ({children, ...props}) => {
  const auth = useSelector(state => state.auth);
  const dispatch = useDispatch();

  useEffect(() => {
    checkAuth(auth.isAuthenticated)
  }, [auth.isAuthenticated])

  const checkAuth = async (isAuthenticated) => {
    if (!isAuthenticated) {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await verifyToken(token);
          dispatch(loginUserSuccess({token}))
        } catch (error) {
          dispatch(logout())
        }
      }
    }
  }

  return (
    <Route
      {...props}
      render={({location}) =>
        auth.isAuthenticated ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: {from: location}
            }}
          />
        )
      }
    />
  );
}
