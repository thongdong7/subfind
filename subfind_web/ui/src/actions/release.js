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
  toggleOnlyShowLang: lang => state => {
    let {onlyShowLang} = state
    if (onlyShowLang.indexOf(lang) < 0) {
      onlyShowLang = [...onlyShowLang, lang]
    } else {
      onlyShowLang = onlyShowLang.filter(l => l !== lang)
    }

    return {
      ...state,
      onlyShowLang
    }
  }
}

export default {
  releases: [releaseActions, []],
  releaseFilter: [releaseFilterActions, {onlyShowMissedSubtitle: false, onlyShowLang: [] }],
}
