import React from 'react'


export default class Switch extends React.Component {
  constructor(props) {
    super(props)

    this.checked = this.props.checked ? true : false
  }

  onChange() {
    if (this.props.onChange) {
      this.props.onChange(this.checked)
    }
  }

  render() {
    return (
      <span>
        <input id="cmn-toggle-1"
          className="cmn-toggle cmn-toggle-round"
           type="checkbox" onChange={this.onChange.bind(this)}
           defaultChecked={this.checked} />
        <label htmlFor="cmn-toggle-1"></label>
      </span>
    )
  }
}
