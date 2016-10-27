export default class DataLoader {
  constructor(host) {
    this.host = host
  }

  async load(path, params) {
    return new Promise((resolve, reject) => {
      let url = this.host + '/' + path
      $.ajax({
        url: url,
        data: params,
        success: function(data) {
          resolve(data)
        },
        error: function(err) {
          reject(err)
        }
      })
    })
  }

  async get(path) {
    return this.ajax('GET', path)
  }

  async post(path, doc) {
    return this.ajax('POST', path, doc)
  }

  async put(path, doc) {
    return this.ajax('PUT', path, doc)
  }

  async ajax(method, path, params) {
    return new Promise((resolve, reject) => {
      let url = this.host + '/' + path
      $.ajax({
        url: url,
        method: method,
        data: params,
        success: function(data) {
          resolve(data)
        },
        error: function(err) {
          reject(err)
        }
      })
    })
  }
}
