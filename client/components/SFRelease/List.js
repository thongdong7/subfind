import React from 'react'
import { Link } from 'react-router'
import RestService from '../RestService'
import LanguageStats from './LanguageStats'
import RPCButton from '../RPCButton'
import SFConfigIndex from '../SFConfig/Index'

export default class SFReleaseList extends React.Component {
  constructor(props) {
    super(props)

    this.state = {data: [], current: null, connectionError: false, loading: false}
  }

  componentWillMount() {
    this.loadData()
  }

  async loadData() {
    try {
      this.setState({loading: true})

      let data = await RestService.load('release')
      // console.log(data)

      this.setState({data: data, connectionError: false, loading: false})
    } catch (promise) {
//      console.log('error', promise)
      this.setState({connectionError: true, loading: false})
    }
  }

  render() {
    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">SFReleaseList Title</h3>

          <div className="box-tools">
            <button type="button" className="btn btn-box-tool" data-widget="collapse"><i className="fa fa-minus"></i>
            </button>

            <RPCButton query="release/scan-all" name="Scan All" />
          </div>
        </div>
        <div className="box-body">
          <SFConfigIndex />
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Name</th>
                <th>subtitles</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
            {this.state.data.map((item, k) => {
              return (
                <tr key={k}>
                  <td>
                      {item.name}
                  </td>
                  <td>
                    <LanguageStats data={item.subtitles} />
                  </td>
                  <td>
                    <RPCButton query="release/download" params={{src: item.src}} name="Download" />
                  </td>
                </tr>
              )
            })}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}
