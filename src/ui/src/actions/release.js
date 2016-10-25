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

export const releaseFilterActions = {
  toggleShow: () => state => ({...state, showMissed: !state.showMissed}),
}

export default {
  releases: [releaseActions, []],
  releaseFilter: [releaseFilterActions, {showMissed: false, }],
}
