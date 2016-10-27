import React from 'react'

class MovieFolder extends React.Component {
  render() {
    return (
      <div>
        <div className="col-sm-11 col-xs-10">{this.props.src}</div>
        <div className="col-sm-1 col-xs-2">
          {this.props.children}
        </div>
      </div>
    )
  }
}

export default MovieFolder
