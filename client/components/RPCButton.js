import React from 'react'
import RestService from './RestService'

export default class RPCButton extends React.Component {
  constructor(props) {
    super(props)

    this.state = {loading: false}
  }

  async onClick() {
    this.setState({loading: true})
    let data = await RestService.load(this.props.query, this.props.params)

    this.setState({loading: false})

    if (this.props.onComplete) {
      this.props.onComplete(data)
    }
  }

  render() {
    let loading
    if (this.state.loading) {
      loading = (
        <i className="fa fa-spin fa-refresh"></i>
      )
    }

    return (
      <button className="btn btn-default" onClick={this.onClick.bind(this)}>{loading} {this.props.name}</button>
    )
  }
}
