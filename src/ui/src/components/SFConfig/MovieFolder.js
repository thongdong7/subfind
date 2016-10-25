import React from 'react'

export default class MovieFolder extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <div className="col-sm-11 col-xs-10">{this.props.src}</div>
        <div className="col-sm-1 col-xs-2">
          <button className="btn btn-danger btn-xs" onClick={this.props.onRemove}>
            <i className="fa fa-trash"></i>
          </button>
        </div>
      </div>
    )
  }
}
