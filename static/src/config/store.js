// @flow
import {combineReducers, createStore} from 'redux';

import {authReducer, dataReducer} from '../reducers';

const rootReducer = combineReducers({
  auth: authReducer,
  data: dataReducer
});


const store = createStore(rootReducer);

export default store;
export {
  rootReducer
};
