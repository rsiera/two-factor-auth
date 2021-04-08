// @flow
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';
import map from 'lodash/map';
import type {Node} from 'react';
import React from 'react';
import Alert from '@material-ui/lab/Alert';
import FormHelperText from '@material-ui/core/FormHelperText';
import Typography from '@material-ui/core/Typography';
import {useTheme} from '@material-ui/core/styles';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import Snackbar from '@material-ui/core/Snackbar';
import isNil from "lodash/isNil";
import size from "lodash/size";
import filter from "lodash/filter";
import has from "lodash/has";

const getTypeOf = (obj: any): string => {
  return Object.prototype.toString.call(obj).slice(8, -1);
};

const isTypeOf = (obj: any, type: string): boolean => {
  return !isNil(obj) && type === getTypeOf(obj);
};

const useMobileView: () => boolean = () => {
  const theme = useTheme();
  return useMediaQuery(theme.breakpoints.down('sm'));
};

const FieldValidationError: ({form: Object, field: Object} => Node) = ({form, field}) => {
  const errors = get(form.errors, field.name, {});
  if (isEmpty(errors)) {
    return null;
  }
  return (
    <FormHelperText error component={'div'}>
      {isTypeOf(errors, 'Array')
        ? errors.map((errMsg, idx) => <Typography key={idx} variant={'caption'}>{errMsg}</Typography>)
        : <Typography variant={'caption'}>{errors}</Typography>
      }
    </FormHelperText>
  );
};

const NonFieldErrors: ({error: Object, onClose?: () => void} => Node) = ({error, onClose}) => {
  const errors = get(error, 'non_field_errors', {});
  if (isEmpty(errors)) {
    return null;
  }
  if (!onClose) {
    return (
      <Alert severity={'error'}>
        {errors.map((msg, idx) => (
          <Typography variant={'body2'} key={idx}>{msg}</Typography>
        ))}
      </Alert>
    );
  }

  return (
    <Snackbar
      data-testid={'non-field-errors-snackbar'}
      open={!isEmpty(errors)}
      onClose={onClose}
    >
      <Alert onClose={onClose} severity={'error'}>
        {errors.map((msg, idx) => (
          <Typography variant={'body2'} key={idx}>{msg}</Typography>
        ))}
      </Alert>
    </Snackbar>
  );
};

const RequestError: ({error: Object, onClose?: (Object) => void} => Node) = ({error, onClose}) => {
  if (!error) {
    return null;
  }
  return (
    <Snackbar
      data-testid={'request-error-snackbar'}
      open={!isEmpty(error)}
      onClose={onClose}
    >
      {isTypeOf(error, 'String')
        ? <Alert onClose={onClose} severity={'error'}><Typography variant={'body1'}>{error}</Typography></Alert>
        : (
          <Alert onClose={onClose} severity={'error'}>
            <Typography variant={'body1'}>Your request hasn't been completed.</Typography>
            {map(error, (value, key) => (
              <Typography key={key} variant={'body2'}>
                {`${key}: ${isTypeOf(value, 'String') ? value : map(value, msg => msg).join(';')}`}
              </Typography>
            ))}
          </Alert>
        )
      }
    </Snackbar>
  );
};

const SubmitFormError = ({error, onDismiss}: {error: Object, onDismiss?: () => void}): Node => {
  if (isEmpty(error)) {
    return null;
  }

  return get(error, 'non_field_errors')
    ? <NonFieldErrors error={error} onClose={onDismiss}/>
    : <RequestError error={error} onClose={onDismiss}/>
};

const emptyFunc = () => {};

const hasFormikErrors = (error: Object, formikValues?: Object) => {
  const errors = get(error, 'data.errors', null) || error.data;
  return !!size(filter(formikValues, (fieldVal, fieldName) => has(errors, fieldName)));
};

const handleFormError = (
  error: Object, onError?: (Object) => void = emptyFunc, formik?: { values: Object, actions: Object }
): any => {
  const {actions, values} = formik || {};
  actions && actions.setSubmitting(false);

  if (error.data) {
    const errorSetter = hasFormikErrors(error, values) ? actions.setErrors : onError;
    errorSetter(error.data.errors || error.data);
  } else if (error.message) {
    onError(error.message);
  } else {
    console.error(error);
  }
};

export {
  useMobileView,
  FieldValidationError,
  NonFieldErrors,
  RequestError,
  SubmitFormError,
  handleFormError
};
