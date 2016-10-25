import {
  APIAction,
  ReducerSet,
//  createSchema,
} from 'tb-react'

export const releaseActions = {
  update: ReducerSet(),
  load: APIAction(site => ({
    url: 'Release/list',
    success: (dispatch, data) => {
      dispatch(releaseActions.update, data)
    },
    error: (dispatch) => {},
  })),
}

export default {
  releases: [releaseActions, []],
}
