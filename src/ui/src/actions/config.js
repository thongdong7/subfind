import {
  APIAction,
  ReducerSet,
  success,
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
      // console.log('config update response', data);
      dispatch(configActions.load)
      success(`Added ${value} to ${field}`)
    },
    error: (dispatch, data) => {
      console.error(data);
      error(data.message)
    }
  })),
  removeField: APIAction((field, value) => ({
    url: 'Config/update',
    params: {
      [`${field}-$remove`]: value
    },
    success: (dispatch, data) => {
      // console.log('config update response', data);
      dispatch(configActions.load)
      success(`Removed ${value} from ${field}`)
    },
    error: (dispatch, data) => {
      console.error(data);
      error(data.message)
    }
  })),
}

export default {
  config: [configActions, {src: [], lang: [], providers: [], force: false, remove: false}],
}
