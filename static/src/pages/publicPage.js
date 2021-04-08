// @flow
import Container from "@material-ui/core/Container";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import React from "react";
import {useStyles} from '../config/styles';

const PublicPage = () => {
  const classes = useStyles({});

  return (
    <Container disableGutters maxWidth={false} className={classes.container}>
      <Box paddingY={2} paddingX={2.5} textAlign={'center'}>
        <Typography variant={'h5'} className={classes.title}>
          This is public page
        </Typography>
      </Box>
    </Container>
  );
}
export default PublicPage;
