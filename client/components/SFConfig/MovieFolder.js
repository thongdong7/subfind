import React from 'react'

export default class MovieFolder extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <div className="col-sm-11">{this.props.src}</div>
        <div className="col-sm-1">
          <button className="btn btn-danger btn-xs" onClick={this.props.onRemove}>
            <i className="fa fa-trash"></i>
          </button>
        </div>
      </div>
    )
  }
}
