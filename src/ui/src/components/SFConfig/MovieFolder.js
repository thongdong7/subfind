import React from 'react'
import * as tb from 'tb-react'

export default class MovieFolder extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <div className="col-sm-11 col-xs-10">{this.props.src}</div>
        <div className="col-sm-1 col-xs-2">
          <tb.Button
            name="Remove"
            icon="trash"
            hideName
            type="danger"
            onClick={this.props.onRemove}
          />
        </div>
      </div>
    )
  }
}
