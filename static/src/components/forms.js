// @flow
import type {Node} from 'react';
import React, {useEffect, useState} from "react";
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import {Field, Form, Formik} from 'formik';

import InputWithLabelField from './fields';
import SubmitButton from './buttons';
import {useStyles} from '../config/styles';
import {useMobileView} from './helpers';
import * as Yup from "yup";


const LoginForm: ({onSubmit: (Object, Object) => Promise<any>} => Node) = ({onSubmit}) => {
  const isMobile = useMobileView();
  const classes = useStyles({isMobile});
  const [canSubmit, setCanSubmit] = useState(false);

  useEffect(() => {
    setCanSubmit(true);
  }, []);

  return (
    <Grid container>
      <Grid item xs={12} className={classes.headerMargin}>
        <Box marginY={2}>
          <Typography component={'span'} variant={'h3'} className={classes.label}>Log in to Website</Typography>
        </Box>
      </Grid>
      <Grid item xs={12}>
        <Formik
          enableReinitialize
          initialValues={{
            email: '',
            password: '',
            two_fa_code: '',
            show_2fa: false
          }}
          validationSchema={
            Yup.object().shape({
              email: Yup.string().email().required('Email is a required field.'),
              password: Yup.string().required('Password is a required field.'),
            })
          }
          onSubmit={onSubmit}
        >
          {({isSubmitting, values}) => (
            <Form data-testid={'user-login-form'} method={'post'}>
              <Grid container spacing={2} direction={'column'}>
                {values.show_2fa
                  ? (
                    <Grid item xs={12} md={6}>
                      <Field name={'two_fa_code'} className={classes.input} component={InputWithLabelField} label={'Security code'}/>
                    </Grid>
                  ) : (
                    <>
                      <Grid item xs={12} md={6}>
                        <Field name={'email'} className={classes.input} component={InputWithLabelField} label={'Email'} type={'email'}/>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <Field name={'password'} className={classes.input} component={InputWithLabelField} label={'Password'} type={'password'}/>
                      </Grid>
                    </>
                  )
                }
                <Grid item xs={12} md={3}>
                  <SubmitButton
                    data-testid={'login-button'}
                    disabled={isSubmitting || !canSubmit}
                    variant={'contained'}
                    color={'primary'}
                  >
                    LOG IN
                  </SubmitButton>
                </Grid>
              </Grid>
            </Form>
          )}
        </Formik>
      </Grid>
    </Grid>
  )
};

export {
  LoginForm,
};

