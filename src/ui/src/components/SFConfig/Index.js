import React from 'react'
import Loading from '../Loading'
// import RestService from '../RestService'
import update from 'react-addons-update'
import MovieFolder from './MovieFolder'
import Switch from '../Switch'
import InputEditable from '../InputEditable'
import SimpleForm from '../SimpleForm'
import toastr from 'toastr'
import * as tb from 'tb-react'
import {configActions} from '../../actions/config'

let mb = 1024 * 1024

class SFConfigIndex extends React.Component {
  constructor(props, context) {
    super(props, context)

    this.providers = [
      {name: "opensubtitles", display_name: "Opensubtitles"},
      {name: "subscene", display_name: "Subscene"},
    ]

    this.state = {data: null, formData: {}, loading: false}
  }

  componentWillMount() {
    this.loadData()
  }

  async loadData() {
    // this.setState({loading: true})
    //
    // let data = await RestService.load("config")
    //
    // this.setState({data: data, loading: false})
  }

  async addFolder(data) {
    console.log('data', data);
    this.props.onPushField('src', data.src)
  }

  async addLanguage(data) {
    return this.updateConfig({
      'lang-$push': data.name
    })
  }

  async updateConfig(params) {
    // this.setState({loading: true})
    // try {
    //   let ret = await RestService.load("config/update", params)
    //   // console.log(ret);
    //
    //   this.setState({data: ret, loading: false})
    //
    //   return true
    // } catch (response) {
    //   // console.log(response);
    //   toastr.error(response.responseJSON.message)
    //
    //   this.setState({loading: false})
    //
    //   return false
    // }
  }

  removeFolder(src) {
    // console.log('remove ', src);
    // this.updateConfig({'src-$remove': src})
    this.props.removeField('src', src)
  }

  removeLang(src) {
    // console.log('remove ', src);
    this.updateConfig({'lang-$remove': src})
  }

  async updateProvider(checked, name) {
    // console.log(`update ${name} to ${checked}`);
    let fieldName = checked ? 'providers-$push' : 'providers-$remove'
    this.updateConfig({[fieldName]: name})
  }

  updateSwitchField(fieldName, checked) {
    this.updateConfig({[fieldName]: checked})
  }

  async onMinMovieSizeUpdate(value) {
    await this.updateConfig({'min-movie-size': value * mb})
  }

  async onMaxSubUpdate(value) {
    await this.updateConfig({'max-sub': value})
  }

  back() {
    this.context.router.goBack()
  }

  render() {
    // console.log('render', this.state.formData);
    let loading
    // if (this.state.loading) {
    //   loading = (
    //     <Loading />
    //   )
    // }

    const {
      config: {src: folders, lang, providers, force, remove},
      onReload,
    } = this.props
    // console.log('config', this.props.config);
    const config = this.props.config

    let content = (
      <div>
        <div className="row">
          <div className="col-sm-3"><strong>Movie Folders</strong></div>
          <div className="col-sm-9">
            {folders.map((folder, k) => {
              return (
                <MovieFolder
                  src={folder}
                  key={k}
                >
                  <tb.RemoteButton
                    name="Remove"
                    icon="trash"
                    hideName
                    type="danger"
                    url="Config/update"
                    params={{"src-$remove": folder}}
                    onComplete={onReload}
                    />
                </MovieFolder>
              )
            })}
            <SimpleForm
              url="Config/update"
              field={`src-$push`}
              onComplete={onReload}
            />
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3"><strong>Languages</strong></div>
          <div className="col-sm-9">
            {lang.map((item, k) => {
              return (
                <MovieFolder
                  src={item}
                  key={k}
                >
                  <tb.RemoteButton
                    name="Remove"
                    icon="trash"
                    hideName
                    type="danger"
                    url="Config/update"
                    params={{"lang-$remove": item}}
                    onComplete={onReload}
                    />
                </MovieFolder>
              )
            })}

            <SimpleForm
              url="Config/update"
              field={`lang-$push`}
              onComplete={onReload}
            />
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3"><strong>Providers</strong></div>
          <div className="col-sm-9">
            {this.providers.map((item, k) => {
              let tmp = providers.filter(x => x == item.name)
              let value = tmp.length == 1 ? true : false
              // console.log(item.display_name, value);
              return (
                <div key={k}>
                  <div className="col-sm-3">{item.display_name}</div>
                  <div className="col-sm-9">
                    <Switch checked={value} onChange={(checked) => this.updateProvider(checked, item.name)}/>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3"><strong>Force download subtitle</strong></div>
          <div className="col-sm-9">
            <Switch checked={force}
              onChange={(checked) => this.updateSwitchField('force', checked)}/>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3">
            <strong>Remove old subtitles if not found new subtitle</strong>
          </div>
          <div className="col-sm-9">
            <Switch checked={remove}
              onChange={(checked) => this.updateSwitchField('remove', checked)}/>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3">
            <strong>Min movie size (MB)</strong>
            <div>(to ignore sample videos)</div>
          </div>
          <div className="col-sm-9">
            <InputEditable name="min-movie-size" defaultValue={config['min-movie-size'] / mb}
              onUpdate={this.onMinMovieSizeUpdate.bind(this)} />
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3">
            <strong>Number subtitles</strong>
          </div>
          <div className="col-sm-9">
            <InputEditable name="max-sub" defaultValue={config['max-sub']}
              onUpdate={this.onMaxSubUpdate.bind(this)} />
          </div>
        </div>
      </div>
    )

    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">
            <button className="btn btn-default" onClick={this.back.bind(this)}><i className="fa fa-arrow-left"></i> Back</button>
            &nbsp;
            Setup {loading}
          </h3>
        </div>
        <div className="box-body">
          {content}
        </div>
      </div>
    )
  }
}

SFConfigIndex.contextTypes = {
    router: React.PropTypes.object
}

export default tb.connect2({
  start: (dispatch) => {
    dispatch(configActions.load)
  },
  props: ({config}, ownProps, dispatch) => ({
    config,
    onReload: (data) => dispatch(configActions.load)
    // onPushField: (field, value) => dispatch(configActions.pushField, field, value),
    // removeField: (field, value) => dispatch(configActions.removeField, field, value),
  })
})(SFConfigIndex)
