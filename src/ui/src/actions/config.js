import {
  APIAction,
  ReducerSet,
  error,
//  createSchema,
} from 'tb-react'

export const configActions = {
  update: ReducerSet(),
  load: APIAction(() => ({
    url: 'Config',
    success: (dispatch, data) => {
      dispatch(configActions.update, data)
    },
    error: (dispatch) => {},
  })),
  pushField: APIAction((field, value) => ({
    url: 'Config/update',
    params: {
      [`${field}-$push`]: value
    },
    success: (dispatch, data) => {
      console.log('config update response', data);
      dispatch(configActions.load)
    },
    error: (dispatch, data) => {
      console.error(data);
      error(data.message)
    }
  }))
}

export default {
  config: [configActions, {src: [], lang: [], providers: [], force: false, remove: false}],
}
