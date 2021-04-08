// @flow
import {connect} from "react-redux";
import React, {Node, useEffect} from "react";
import Container from "@material-ui/core/Container";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import {fetchUserData} from "../services/dataService";
import {fetchProtectedDataSuccess} from "../actions/dataActions";

import {useStyles} from '../config/styles';

const ProtectedPage: ((props: Object) => Node) = (props) => {
  const classes = useStyles({});
  useEffect(() => {
    const fetchProtectedData = async () => {
      const response = await fetchUserData(props.auth.token);
      props.dispatch(fetchProtectedDataSuccess(response));
    }
    fetchProtectedData();
  }, []);

  return (
    <Container disableGutters maxWidth={false} className={classes.container}>
      <Box paddingY={2} paddingX={2.5} textAlign={'center'}>
        <Typography variant={'h5'} className={classes.title}>
            This is protected content
        </Typography>
        <Typography variant={'h6'} className={classes.title}>ID: {props.data.data.id}</Typography>
        <Typography variant={'h6'} className={classes.title}>Email: {props.data.data.email}</Typography>

      </Box>
    </Container>
  );
}
const protectedPagePropsFactory = (state: Object) => ({
  data: state.data,
  auth: state.auth
});

const ProtectedPageWithRedux = connect(protectedPagePropsFactory)(ProtectedPage);
export default ProtectedPageWithRedux;
