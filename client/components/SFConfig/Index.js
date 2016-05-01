import React from 'react'
import Loading from '../Loading'
import RestService from '../RestService'
import update from 'react-addons-update'
import MovieFolder from './MovieFolder'
import Switch from '../Switch'

class SimpleForm extends React.Component {
  constructor(props) {
    super(props)

    this.state = {formData: {}}
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

export default class SFConfigIndex extends React.Component {
  constructor(props) {
    super(props)

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
    this.setState({loading: true})

    let data = await RestService.load("config")

    this.setState({data: data, loading: false})
  }

  async addFolder(data) {
    return this.updateConfig({
      'src-$push': data.src
    })
  }

  async addLanguage(data) {
    return this.updateConfig({
      'lang-$push': data.name
    })
  }

  async updateConfig(params) {
    this.setState({loading: true})
    let ret = await RestService.load("config/update", params)
    // console.log(ret);

    if (ret.ok === false) {
      console.warn(ret.message);
      this.setState({loading: false})

      return false
    } else {
      this.setState({data: ret, loading: false})

      return true
    }
  }

  removeFolder(src) {
    // console.log('remove ', src);
    this.updateConfig({'src-$remove': src})
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

  render() {
    // console.log('render', this.state.formData);
    let loading
    if (this.state.loading) {
      loading = (
        <Loading />
      )
    }

    let content
    if (this.state.data) {
      // console.log(this.state.data.providers);
      content = (
        <div>
          <div className="row">
            <div className="col-sm-3"><strong>Movie Folders</strong></div>
            <div className="col-sm-9">
              {this.state.data.src.map((item, k) => {
                return (
                  <MovieFolder src={item} key={k} onRemove={() => this.removeFolder(item)}/>
                )
              })}
              <SimpleForm field="src" onSubmit={this.addFolder.bind(this)} />
            </div>
          </div>
          <div className="row">
            <div className="col-sm-3"><strong>Languages</strong></div>
            <div className="col-sm-9">
              {this.state.data.lang.map((item, k) => {
                return (
                  <MovieFolder src={item} key={k} onRemove={() => this.removeLang(item)}/>
                )
              })}

              <SimpleForm field="name" onSubmit={this.addLanguage.bind(this)} />
            </div>
          </div>
          <div className="row">
            <div className="col-sm-3"><strong>Providers</strong></div>
            <div className="col-sm-9">
              {this.providers.map((item, k) => {
                let tmp = this.state.data.providers.filter(x => x == item.name)
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
              <Switch checked={this.state.data.force}
                onChange={(checked) => this.updateSwitchField('force', checked)}/>
            </div>
          </div>
          <div className="row">
            <div className="col-sm-3">
              <strong>Remove old subtitles if not found new subtitle</strong>
            </div>
            <div className="col-sm-9">
              <Switch checked={this.state.data.remove}
                onChange={(checked) => this.updateSwitchField('remove', checked)}/>
            </div>
          </div>
        </div>
      )
    }

    return (
      <div className="box box-solid">
        <div className="box-header with-border">
          <h3 className="box-title">
            Config {loading}
          </h3>

          <div className="box-tools">
            <button type="button" className="btn btn-box-tool" data-widget="collapse"><i className="fa fa-minus"></i>
            </button>
          </div>
        </div>
        <div className="box-body">
          {content}
        </div>
      </div>
    )
  }
}
