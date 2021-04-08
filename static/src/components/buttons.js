// @flow
import React from 'react';

import {Button} from '@material-ui/core';
import {useMobileView} from './helpers';

const SubmitButton = (
  {isSubmitting, children, ...props}: Object
) => {
  const isMobile = useMobileView();
  return (
    <Button
      type={'submit'}
      disabled={isSubmitting}
      {...props}
      fullWidth={isMobile}
    >
      {children}
    </Button>
  )
};

export default SubmitButton;
