import React from 'react'

export default class InputEditable extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      editing: false,
      name: props.name,
      value: props.defaultValue
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.name !== this.props.name) {
      this.setState({name: nextProps.name})
    }
  }

  async toggle() {
    await this.setState({editing: !this.state.editing})
  }

  onControlChange(e) {
    let value = e.target.value
    this.setState({value: value})
  }

  updateValue = async (e) => {
    e.preventDefault()

    if (this.props.onUpdate) {
      this.props.onUpdate(this.state.value)
    }

    this.setState({editing: false})
  }

  render() {
    const {value: stateValue} = this.state
    const {defaultValue} = this.props
    const value = stateValue || defaultValue || ''
    return (
      <div>
        {
          !this.state.editing &&
          <div
            className="editable-value"
            onClick={this.toggle.bind(this)}
          >
            {value}
          </div>
        }
        {
          this.state.editing &&
          <form onSubmit={this.updateValue}>
            <input
              type="number"
              className="form-control"
              autoFocus={this.state.editing}
              name={this.state.name}
              value={value}
              onChange={this.onControlChange.bind(this)}
              onBlur={this.updateValue}
            />
          </form>
        }
      </div>
    )
  }

}
