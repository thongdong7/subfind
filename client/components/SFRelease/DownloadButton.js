import React from 'react'
import RestService from '../RestService'

export default class DownloadButton extends React.Component {
  constructor(props) {
    super(props)

    this.state = {loading: false}
  }

  async download() {
    // console.log('download release', this.props.release);
    this.setState({loading: true})
    let data = await RestService.load('release/download', {src: this.props.release.src})

    this.setState({loading: false})
  }

  render() {
    let loading
    if (this.state.loading) {
      loading = (
        <i className="fa fa-spin fa-refresh"></i>
      )
    }

    return (
      <button className="btn btn-default" onClick={this.download.bind(this)}>{loading}Download</button>

    )
  }
}
