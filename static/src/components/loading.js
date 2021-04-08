// @flow
import times from 'lodash/times';
import React from 'react';
import Grid from '@material-ui/core/Grid';
import Skeleton from '@material-ui/lab/Skeleton';

const FormSkeleton = ({count = 3}: {count?: number}) => (
  <Grid container direction={'column'} spacing={2}>
    {times(count, (idx) => (
      <div key={idx}>
        <Grid item><Skeleton variant={'text'} width={'100%'}/></Grid>
        <Grid item><Skeleton component={'div'} variant={'rect'} height={'2.5rem'} width={'100%'}/></Grid>
      </div>
    ))}
  </Grid>
);

export {
  FormSkeleton
};
