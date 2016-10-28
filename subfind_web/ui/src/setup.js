import {api} from 'tb-react'

export default function setup() {
  if (window && window.apiHost) {
    api.host = `${window.apiHost}/api/`
  } else {
    api.host = "http://127.0.0.1:5001/api/"
  }

//  console.log('actual API host', api.host);
}
