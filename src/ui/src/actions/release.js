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
  toggleOnlyShowMissedSubtitle: () => state => ({...state, onlyShowMissedSubtitle: !state.onlyShowMissedSubtitle}),
}

export default {
  releases: [releaseActions, []],
  releaseFilter: [releaseFilterActions, {onlyShowMissedSubtitle: false, }],
}
