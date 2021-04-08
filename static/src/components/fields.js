// @flow
import isNil from 'lodash/isNil';
import React from 'react';
import type {Node} from 'react';
import {FormControl, InputLabel} from '@material-ui/core';
import Skeleton from '@material-ui/lab/Skeleton';
import {Box} from '@material-ui/core';
import {InputBase} from '@material-ui/core';
import classnames from 'classnames';
import {makeStyles} from "@material-ui/core/styles";

import {FieldValidationError} from "./helpers";

const formControlStyles = (theme: Object): Object => ({
  root: {
    display: 'block',
  }
});

const useFormControlStyles: ((Object) => Object) = makeStyles(formControlStyles);

const inputStyles = (theme: Object): Object => ({
  root: {
    width: '100%',
    fontSize: '16px',
    height: '2.5em',
    color: '#4d4d4d',
    padding: '0.5em',
    borderRadius: '3px',
    border: '1px solid #cccac8'
  }
});

const useInputStyles: ((Object) => Object) = makeStyles(inputStyles);

const labelStyles = (theme: Object): Object => ({
  root: {
    position: 'relative',
    transform: 'none',
    marginBottom: theme.spacing(1),
    fontSize: '0.875rem',
    lineHeight: 1.3,
  },
});

const useLabelStyles: ((Object) => Object) = makeStyles(labelStyles);

const RawInput = (
  {styles = useInputStyles(), className, ...props}: Object
) => {
  return <InputBase className={classnames(styles.root, className)} {...props} />;
};

const InputSkeleton = (
  {show, children, width = '80%', height = '2.5em', fieldName = ''}:
    {show: boolean, children: Node, width?: string|number, height?: string|number, fieldName?: string}) => (
  <>
    {show
      ? (
        <Box data-testid={`skeleton-id-${fieldName}`}>
          <Skeleton variant={'text'} width={width}/>
          <Skeleton variant={'rect'} width={width} height={height}/>
        </Box>
      ): (children)
    }
  </>
);

const InputWithLabelField = (
  {field, form, label, loading, required, children, controlStyles = useFormControlStyles(),
    labelStyles = useLabelStyles(), ...props}: Object
): Node => {
  const fieldId = `id-${field.name}`;

  return (
    <FormControl classes={controlStyles}>
      <InputSkeleton show={loading || form.isSubmitting}>
        <InputLabel
          classes={labelStyles}
          required={required}
          htmlFor={fieldId}
        >
          {label}
        </InputLabel>
        <RawInput
          {...props}
          id={fieldId}
          name={field.name}
          value={isNil(field.value) ? '' : field.value}
          onChange={event => form.setFieldValue(field.name, event.target.value)}
        />
        <FieldValidationError form={form} field={field}/>
      </InputSkeleton>
    </FormControl>
  )
};

export default InputWithLabelField;
