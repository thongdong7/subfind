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
    let icon
    if (this.state.loading) {
      loading = (
        <i className="fa fa-spin fa-spinner"></i>
      )
    } else {
      if (this.props.icon) {
        icon = (
          <i className={"fa fa-"+this.props.icon}></i>
        )
      }
    }

    let tag = this.props.tag ? this.props.tag : "button"

    let props = this.props['tag-props'] ? this.props['tag-props'] : {}
    if (tag == "button") {
      props.className = "btn btn-default"
    }

    props.onClick = this.onClick.bind(this)

    return React.createElement(tag, props, loading, icon, ' ' + this.props.name)
  }
}
