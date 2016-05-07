import React from 'react'

export default class InputEditable extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      editing: false,
      name: this.props.name,
      value: this.props.defaultValue
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.name != this.props.name) {
      this.setState({name: nextProps.name})
    }
  }

  getValue() {
    return this.state.value != undefined ? this.state.value : this.props.defaultValue
  }

  async toggle() {
    await this.setState({editing: !this.state.editing})

    if (this.state.editing) {
      // console.log('do focus');
      $(`[name='${this.state.name}']`).focus()
    }
  }

  onControlChange(e) {
    let value = e.target.value
    this.setState({value: value})
  }

  async updateValue(e) {
    e.preventDefault()

    if (this.props.onUpdate) {
      this.props.onUpdate(this.state.value)
    }

    this.setState({editing: false})
  }

  render() {
    return (
      <div>
        {!this.state.editing &&
          <div className="editable-value" onClick={this.toggle.bind(this)}>
            {this.getValue()}
          </div>
        }
        {
          this.state.editing &&
          <form onSubmit={this.updateValue.bind(this)}>
            <input type="number" className="form-control"
              name={this.state.name}
              value={this.getValue()}
              onChange={this.onControlChange.bind(this)}
              onBlur={this.updateValue.bind(this)}
            />
          </form>
        }
      </div>
    )
  }

}
