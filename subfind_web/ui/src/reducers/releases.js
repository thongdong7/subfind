import { UPDATE_RELEASES, RELEASE_LOADING } from "../actions";

const initScanningRelease = {
  releaseName: null,
  total: 0,
  index: 0,
};

const initState = {
  items: [],
  loading: false,
  scanningRelease: initScanningRelease,
};

export default function reducer(state = initState, action) {
  switch (action.type) {
    case UPDATE_RELEASES:
      return {
        ...state,
        items: action.releases,
        loading: false,
      };
    case RELEASE_LOADING:
      return {
        ...state,
        loading: true,
      };
    case "SCAN_RELEASE": {
      return {
        ...state,
        scanningRelease: action.payload,
      };
    }
    case "SCAN_RELEASE_COMPLETE":
      return {
        ...state,
        scanningRelease: initScanningRelease,
      };

    default:
      return state;
  }
}
