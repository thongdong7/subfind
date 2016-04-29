import React from 'react'

let switchId = 0

export default class Switch extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      id: switchId,
      checked: this.props.checked ? true : false
    }
    
    switchId++
  }

  onChange() {
    if (this.props.onChange) {
      this.props.onChange(this.state.checked)
    }
  }

  render() {
    return (
      <span>
        <input id={"cmn-toggle-"+this.state.id}
          className="cmn-toggle cmn-toggle-round"
           type="checkbox" onChange={this.onChange.bind(this)}
           defaultChecked={this.state.checked} />
        <label htmlFor={"cmn-toggle-"+this.state.id}></label>
      </span>
    )
  }
}
