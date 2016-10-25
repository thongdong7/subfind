import React from 'react'
import update from 'react-addons-update'

export default class SimpleForm extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      formData: {},
      editMinMovieSize: false
    }
  }

  async onSubmit(e) {
    e.preventDefault()

    if (this.props.onSubmit) {
      let ok = await this.props.onSubmit(this.getData())
      if (ok === true) {
        this.setState({formData: {}})
      }
    }
  }

  formChange(e) {
    let field = e.target.name
    let value = e.target.value
    this.setState(update(this.state, {formData: {[field]: {$set: value}}}))
  }

  getData() {
    return this.state.formData
  }

  render() {
    let field = this.props.field
    return (
      <form role="form" onSubmit={this.onSubmit.bind(this)}
        onChange={this.formChange.bind(this)}>
        <div className="input-group input-group-sm">
          <input name={field} type="text" className="form-control"
            autoComplete="off"
            value={this.state.formData[field] || ''} />
          <span className="input-group-btn">
            <button type="submit" className="btn btn-default">Add</button>
          </span>
        </div>
      </form>
    )
  }
}
