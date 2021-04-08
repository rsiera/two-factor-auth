// @flow
import type {Node} from "react";
import React, {useEffect, useState} from 'react';
import {useHistory} from "react-router-dom";
import {
  handleFormError,
  SubmitFormError,
  useMobileView
} from "../components/helpers";
import {useStyles} from "../config/styles";
import {loginUser} from "../services/authService";
import {loginUserSuccess} from "../actions/authActions";
import get from "lodash/get";
import omit from "lodash/omit";
import Container from "@material-ui/core/Container";
import {FormSkeleton} from "../components/loading";
import {LoginForm} from "../components/forms";
import partial from "lodash/partial";
import {connect} from "react-redux";
import Grid from '@material-ui/core/Grid';


const ContentContainer: (({content: Node }) => Node) = ({content}) => {
  const isMobile = useMobileView();
  const classes = useStyles({isMobile});
  return (
    <>
      {isMobile
        ? (
          <>
            <Grid container>
              <Grid item xs={12} className={classes.right}>
                {content}
              </Grid>
            </Grid>
          </>
        ) : (
          <Grid container>
            <Grid item xs={12} md={4}>
            </Grid>
            <Grid item xs={12} md={8} className={classes.right}>
              {content}
            </Grid>
          </Grid>
        )
      }
    </>
  );
};

const UserLogin: ((props: Object) => Node) = (props) => {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();
  const isMobile = useMobileView();
  const classes = useStyles({isMobile});

  useEffect(() => {
    if (props.auth.isAuthenticated){
        history.push('/protected')
      }
  }, [props.auth.isAuthenticated])

  const handleLogin = async (values: Object, actions: Object) => {
    setError(null);
    try {
      const response = await loginUser(values.email, values.password, values.two_fa_code);
      actions.setSubmitting(false);
      props.dispatch(loginUserSuccess(response))
      history.push('/protected')
    } catch (error) {
      actions.setFieldValue('show_2fa', get(error, 'data.show_2fa', false), false);
      const formErrors = {...error, data: omit(error.data, 'show_2fa')};
      handleFormError(formErrors, setError, {values, actions});
    }
  };

  return (
    <Container disableGutters maxWidth={false} className={classes.container}>
      <ContentContainer
        content={
          isLoading
            ? <FormSkeleton/>
            : (
              <LoginForm onSubmit={handleLogin}/>
            )
        }
      />
      <SubmitFormError error={error} onDismiss={partial(setError, null)}/>
    </Container>
  );
};
const UserLoginPropsFactory = (state: Object): Object => ({
  auth: state.auth,
});

const UserLoginWithRedux: Node = connect(UserLoginPropsFactory)(UserLogin);
export default UserLoginWithRedux;
