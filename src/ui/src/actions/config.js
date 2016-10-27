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
  updateListField: APIAction((field, value, enable) => {
    const updateField = enable ? `${field}-$push` : `${field}-$remove`
    return {
      url: 'Config/update',
      params: {
        [updateField]: value
      },
      success: (dispatch, data) => {
        // console.log('config update response', data);
        dispatch(configActions.load)
        success(`${enable ? 'Added' : 'Removed'} ${value} from ${field}`)
      },
      error: (dispatch, data) => {
        console.error(data);
        error(data.message)
      }
    }
  }),
}

export default {
  config: [configActions, {src: [], lang: [], providers: [], force: false, remove: false}],
}
