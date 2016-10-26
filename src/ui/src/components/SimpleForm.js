import React from 'react'
import * as tb from 'tb-react'

class SimpleForm extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      value: '',
      error: false,
    }
  }

  async onSubmit(e) {
    e.preventDefault()

    this.refs.submitButton.submit()
  }

  formChange({target: {value}}) {
    this.setState({value})
  }

  onComplete = () => {
    this.setState({error: false, value: ''})
    if (this.props.onComplete) {
      this.props.onComplete()
    }
  }

  onError = () => {
    this.setState({error: true})
  }

  getData() {
    return this.state.formData
  }

  render() {
    const {field, url} = this.props
    const {value, error} = this.state
    const params = {
      [field]: value
    }

    const errorClass = error ? 'has-error': ''
    return (
      <form role="form" onSubmit={this.onSubmit.bind(this)}
        onChange={this.formChange.bind(this)}>
        <div className={`input-group input-group-sm ${errorClass}`}>
          <input
            name={field}
            type="text"
            className={`form-control`}
            autoComplete="off"
            value={value} />
          <span className="input-group-btn">
            <tb.RemoteButton
              ref="submitButton"
              url={url}
              params={params}
              name="Add"
              onError={this.onError}
              onComplete={this.onComplete}
            />
          </span>
        </div>
      </form>
    )
  }
}

export default SimpleForm
