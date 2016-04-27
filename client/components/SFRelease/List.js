import React from 'react'
import { Link } from 'react-router'
import RestService from '../RestService'
import LanguageStats from './LanguageStats'
import RPCButton from '../RPCButton'
import SFConfigIndex from '../SFConfig/Index'
import _ from 'lodash'
import update from 'react-addons-update'
import Switch from '../Switch'

export default class SFReleaseList extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      data: [],
      current: null,
      connectionError: false,
      loading: false,
      filter: {
        empty: false
      }
    }
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

  toggleFilter() {
    this.setState(update(this.state, {filter: {$set: {empty: !this.state.filter.empty}}}))
  }

  filter(item) {
    if (this.state.filter.empty) {
      return _.isEmpty(item.subtitles)
    }

    return true
  }

  render() {
    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">Movies</h3>

          <div className="box-tools">
            <button type="button" className="btn btn-box-tool" data-widget="collapse"><i className="fa fa-minus"></i>
            </button>

            <RPCButton query="release/scan-all" name="Scan All" />
          </div>
        </div>
        <div className="box-body">
          <div className="row">
            <div className="col-md-6 col-xs-8">
              Only show missed subtitle release
            </div>
            <div className="col-md-6 col-xs-4">
              <Switch checked={this.state.filter.empty}
                onChange={this.toggleFilter.bind(this)} />
            </div>
          </div>

          {this.state.data.filter(this.filter.bind(this)).map((item, k) => {
            let stateClass = ""
            if (_.isEmpty(item.subtitles)) {
              stateClass = " bg-warning"
            }
            return (
              <div key={k} className={"row row-hover row-list-item"+stateClass}>
                <div className="col-xs-12">
                    {item.name}
                </div>
                <div className="col-xs-6">
                  <LanguageStats data={item.subtitles} />
                </div>
                <div className="col-xs-6 pull-right">
                  <RPCButton query="release/download" params={{src: item.src}} name="Download" />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }
}
